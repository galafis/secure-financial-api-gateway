"""Test health and root endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Secure Financial API Gateway"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"
        assert data["docs"] == "/api/docs"

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "api-gateway"
        assert "timestamp" in data
        # Verify timestamp is in ISO format
        from datetime import datetime
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))

    def test_openapi_docs_accessible(self):
        """Test that OpenAPI docs are accessible"""
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_redoc_accessible(self):
        """Test that ReDoc is accessible"""
        response = client.get("/api/redoc")
        assert response.status_code == 200
