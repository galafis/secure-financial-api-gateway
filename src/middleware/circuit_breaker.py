"""
Circuit Breaker Middleware
Author: Gabriel Demetrios Lafis

Prevents cascading failures by breaking the circuit when error rate is high.
Includes automatic eviction of stale breakers to prevent memory leaks.
"""

import time
from enum import Enum
from typing import Dict

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Circuit is open, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """Circuit breaker implementation."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.last_access = time.time()
        self.state = CircuitState.CLOSED

    def check_state(self):
        """
        Check the circuit state before a request. Raises HTTPException
        if the circuit is OPEN and the timeout hasn't elapsed yet.
        Transitions to HALF_OPEN if timeout has passed.
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "error": "Service Unavailable",
                        "message": (
                            "Circuit breaker is OPEN. "
                            "Service is temporarily unavailable."
                        ),
                        "retry_after": self.timeout,
                    },
                )

    def on_success(self):
        """Handle successful request."""
        self.last_access = time.time()
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
        self.failure_count = 0

    def on_failure(self):
        """Handle failed request."""
        self.last_access = time.time()
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return False
        return (time.time() - self.last_failure_time) >= self.timeout

    def get_state(self) -> str:
        """Get current circuit state."""
        return self.state.value

    def is_stale(self, ttl_seconds: float) -> bool:
        """Check if this breaker has not been accessed within the TTL."""
        return (time.time() - self.last_access) > ttl_seconds


# Maximum breakers before triggering eviction
_MAX_BREAKERS = 5_000
# Time-to-live for idle breakers (30 minutes)
_BREAKER_TTL_SECONDS = 1800.0


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    """
    Circuit breaker middleware.

    Features:
    - Automatic circuit breaking on high error rates
    - Per-endpoint circuit breakers
    - Configurable thresholds and timeouts
    - Half-open state for testing recovery
    - Automatic eviction of stale breakers
    """

    def __init__(self, app, failure_threshold: int = 5, timeout: int = 60):
        super().__init__(app)
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.breakers: Dict[str, CircuitBreaker] = {}
        self._last_eviction = time.time()

    def _evict_stale_breakers(self):
        """Remove breakers that have not been accessed recently."""
        now = time.time()
        if now - self._last_eviction < 60:
            return
        self._last_eviction = now

        stale_keys = [
            key
            for key, breaker in self.breakers.items()
            if breaker.is_stale(_BREAKER_TTL_SECONDS)
        ]
        for key in stale_keys:
            del self.breakers[key]

    async def dispatch(self, request: Request, call_next):
        # Skip circuit breaker for health checks and docs
        if request.url.path in [
            "/health",
            "/",
            "/api/docs",
            "/api/redoc",
            "/api/openapi.json",
        ]:
            return await call_next(request)

        # Periodically evict stale breakers
        if len(self.breakers) > _MAX_BREAKERS // 2:
            self._evict_stale_breakers()

        # Get endpoint identifier
        endpoint = f"{request.method}:{request.url.path}"

        # Get or create circuit breaker
        if endpoint not in self.breakers:
            self.breakers[endpoint] = CircuitBreaker(
                failure_threshold=self.failure_threshold, timeout=self.timeout
            )

        breaker = self.breakers[endpoint]

        # Check if circuit allows the request (raises 503 if OPEN)
        breaker.check_state()

        try:
            response = await call_next(request)

            # Mark as failure if status code >= 500
            if response.status_code >= 500:
                breaker.on_failure()
            else:
                breaker.on_success()

            # Add circuit breaker state header
            response.headers["X-Circuit-Breaker-State"] = breaker.get_state()
            return response

        except HTTPException:
            raise
        except Exception as e:
            breaker.on_failure()
            raise e
