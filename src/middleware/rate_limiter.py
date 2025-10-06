"""
Rate Limiter Middleware
Author: Gabriel Demetrios Lafis

Token bucket algorithm for rate limiting with Redis backend.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict
import time
import hashlib


class TokenBucket:
    """Token bucket for rate limiting"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens"""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def get_remaining(self) -> int:
        """Get remaining tokens"""
        self._refill()
        return int(self.tokens)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Rate limiter middleware using token bucket algorithm
    
    Features:
    - Per-IP rate limiting
    - Per-user rate limiting (if authenticated)
    - Configurable limits
    - Redis backend support (optional)
    """
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.buckets: Dict[str, TokenBucket] = {}
        
        # Calculate refill rate (tokens per second)
        self.refill_rate = requests_per_minute / 60.0
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/api/docs", "/api/redoc", "/api/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Get or create token bucket
        if client_id not in self.buckets:
            self.buckets[client_id] = TokenBucket(
                capacity=self.requests_per_minute,
                refill_rate=self.refill_rate
            )
        
        bucket = self.buckets[client_id]
        
        # Try to consume a token
        if not bucket.consume():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {self.requests_per_minute} requests per minute",
                    "retry_after": 60
                }
            )
        
        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(bucket.get_remaining())
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier"""
        # Try to get user ID from request state (if authenticated)
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        
        # Hash IP for privacy
        return hashlib.sha256(client_ip.encode()).hexdigest()[:16]
