"""Test user routes"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestUserRoutes:
    """Test user-related endpoints"""

    def test_get_profile_without_auth(self):
        """Test accessing profile without authentication"""
        response = client.get("/api/v1/users/profile")
        assert response.status_code == 403  # No auth header

    def test_get_profile_with_invalid_token(self):
        """Test accessing profile with invalid token"""
        response = client.get(
            "/api/v1/users/profile", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_get_profile_with_valid_token(self):
        """Test accessing profile with valid token"""
        # First, register and get token
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "profileuser",
                "email": "profile@example.com",
                "password": "Test@12345",
            },
        )
        token = register_response.json().get("access_token")

        # Now access profile
        response = client.get(
            "/api/v1/users/profile", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "username" in data
        assert data["username"] == "profileuser"
        assert data["email"] == "profile@example.com"
