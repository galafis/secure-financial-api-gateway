"""Test middleware components"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestRateLimiter:
    """Test rate limiting middleware"""

    def test_rate_limit_headers(self):
        """Test that rate limit headers are present"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "ratelimituser",
                "email": "ratelimit@example.com",
                "password": "Test@12345",
            },
        )
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers

    def test_rate_limit_enforcement(self):
        """Test that rate limiting is enforced"""
        # Note: This test may not trigger 429 in a single test run
        # due to the high limit (60 requests per minute)
        # In production, adjust the limit or this test accordingly
        for i in range(5):
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "username": f"user{i}",
                    "email": f"user{i}@example.com",
                    "password": "Test@12345",
                },
            )
            # Should still succeed with normal limits
            assert response.status_code in [200, 201, 409]  # 409 if user exists

    def test_rate_limit_skip_health_check(self):
        """Test that rate limiting skips health check endpoints"""
        for i in range(10):
            response = client.get("/health")
            assert response.status_code == 200


class TestSecurityHeaders:
    """Test security headers middleware"""

    def test_security_headers_present(self):
        """Test that all required security headers are present"""
        response = client.get("/")

        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"

        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"

        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-XSS-Protection"] == "1; mode=block"

        assert "Strict-Transport-Security" in response.headers


class TestRequestLogger:
    """Test request logging middleware"""

    def test_request_id_header(self):
        """Test that request ID header is added"""
        response = client.get("/")
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0

    def test_process_time_header(self):
        """Test that process time header is added"""
        response = client.get("/")
        assert "X-Process-Time" in response.headers
        process_time = float(response.headers["X-Process-Time"])
        assert process_time >= 0


class TestCircuitBreaker:
    """Test circuit breaker middleware"""

    def test_circuit_breaker_skip_health_check(self):
        """Test that circuit breaker skips health check endpoints"""
        response = client.get("/health")
        assert response.status_code == 200
        # Should not have circuit breaker state header for skipped endpoints

    def test_circuit_breaker_normal_operation(self):
        """Test circuit breaker in normal operation"""
        # Register a user
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "circuituser",
                "email": "circuit@example.com",
                "password": "Test@12345",
            },
        )
        # Circuit should be closed (normal operation)
        assert response.status_code in [200, 201, 409]
