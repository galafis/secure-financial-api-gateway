"""
Circuit Breaker Middleware
Author: Gabriel Demetrios Lafis

Prevents cascading failures by breaking the circuit when error rate is high.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from enum import Enum
from typing import Dict
import time


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Circuit is open, rejecting requests
    HALF_OPEN = "half_open" # Testing if service recovered


class CircuitBreaker:
    """Circuit breaker implementation"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func):
        """Execute function with circuit breaker"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "error": "Service Unavailable",
                        "message": "Circuit breaker is OPEN. Service is temporarily unavailable.",
                        "retry_after": self.timeout
                    }
                )
        
        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful request"""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
        self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return False
        
        return (time.time() - self.last_failure_time) >= self.timeout
    
    def get_state(self) -> str:
        """Get current circuit state"""
        return self.state.value


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    """
    Circuit breaker middleware
    
    Features:
    - Automatic circuit breaking on high error rates
    - Per-endpoint circuit breakers
    - Configurable thresholds and timeouts
    - Half-open state for testing recovery
    """
    
    def __init__(self, app, failure_threshold: int = 5, timeout: int = 60):
        super().__init__(app)
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.breakers: Dict[str, CircuitBreaker] = {}
    
    async def dispatch(self, request: Request, call_next):
        # Skip circuit breaker for health checks
        if request.url.path in ["/health", "/", "/api/docs", "/api/redoc", "/api/openapi.json"]:
            return await call_next(request)
        
        # Get endpoint identifier
        endpoint = f"{request.method}:{request.url.path}"
        
        # Get or create circuit breaker
        if endpoint not in self.breakers:
            self.breakers[endpoint] = CircuitBreaker(
                failure_threshold=self.failure_threshold,
                timeout=self.timeout
            )
        
        breaker = self.breakers[endpoint]
        
        # Execute request with circuit breaker
        def execute_request():
            return call_next(request)
        
        try:
            response = await breaker.call(lambda: call_next(request))
            
            # Mark as failure if status code >= 500
            if response.status_code >= 500:
                breaker._on_failure()
            else:
                breaker._on_success()
            
            # Add circuit breaker state header
            response.headers["X-Circuit-Breaker-State"] = breaker.get_state()
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            breaker._on_failure()
            raise e
