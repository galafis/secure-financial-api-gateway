"""
Request Logger Middleware
Author: Gabriel Demetrios Lafis

Logs incoming HTTP requests with method, path, status code, and duration.
Adds X-Request-ID and X-Process-Time headers to every response.
"""

import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("api.requests")


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Middleware that logs every request and adds tracing headers."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log the request
        client_ip = request.client.host if request.client else "unknown"
        logger.info(
            "%s %s %s %d %.3fs",
            client_ip,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        return response
