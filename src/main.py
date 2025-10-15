import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.auth.jwt_handler import JWTHandler
from src.middleware.circuit_breaker import CircuitBreakerMiddleware
from src.middleware.rate_limiter import RateLimiterMiddleware
from src.middleware.request_logger import RequestLoggerMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.routes import admin_routes, auth_routes, trading_routes, user_routes
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Secure Financial API Gateway")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    yield
    logger.info("Shutting down Secure Financial API Gateway")


# Create FastAPI app
app = FastAPI(
    title="Secure Financial API Gateway",
    description="Production-ready API Gateway with advanced security features",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"],
)

# Add custom middleware (order matters!)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(RateLimiterMiddleware, requests_per_minute=60)
app.add_middleware(CircuitBreakerMiddleware, failure_threshold=5, timeout=60)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(trading_routes.router, prefix="/api/v1/trading", tags=["Trading"])
app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "service": "Secure Financial API Gateway",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/api/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    from datetime import datetime, timezone

    return {
        "status": "healthy",
        "service": "api-gateway",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "request_id": (
                request.state.request_id
                if hasattr(request.state, "request_id")
                else None
            ),
        },
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info",
    )
