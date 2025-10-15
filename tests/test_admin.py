"""Test admin routes"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestAdminRoutes:
    """Test admin-related endpoints"""

    def test_list_users_without_auth(self):
        """Test accessing admin endpoint without authentication"""
        response = client.get("/api/v1/admin/users")
        assert response.status_code == 403

    def test_list_users_with_non_admin_token(self):
        """Test accessing admin endpoint with non-admin token"""
        # Register a regular user
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "regularuser",
                "email": "regular@example.com",
                "password": "Test@12345",
            },
        )
        token = register_response.json().get("access_token")

        # Try to access admin endpoint
        response = client.get(
            "/api/v1/admin/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert "Admin access required" in response.json().get("detail", "")

    def test_list_users_with_admin_token(self):
        """Test accessing admin endpoint with admin token"""
        # Use the pre-existing admin credentials
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "admin123"},
        )
        token = login_response.json().get("access_token")

        # Access admin endpoint
        response = client.get(
            "/api/v1/admin/users", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "users" in response.json()
