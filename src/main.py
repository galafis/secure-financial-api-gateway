"""
Secure Financial API Gateway
Author: Gabriel Demetrios Lafis

A production-ready API Gateway with advanced security features for financial services.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

from middleware.rate_limiter import RateLimiterMiddleware
from middleware.circuit_breaker import CircuitBreakerMiddleware
from middleware.request_logger import RequestLoggerMiddleware
from middleware.security_headers import SecurityHeadersMiddleware
from auth.jwt_handler import JWTHandler
from routes import auth_routes, user_routes, trading_routes, admin_routes
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Secure Financial API Gateway",
    description="Production-ready API Gateway with advanced security features",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-RateLimit-Remaining"]
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


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Secure Financial API Gateway")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Secure Financial API Gateway")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "service": "Secure Financial API Gateway",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/api/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "timestamp": "2025-10-06T12:00:00Z"
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
            "request_id": request.state.request_id if hasattr(request.state, "request_id") else None
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )
