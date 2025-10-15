"""Test trading routes"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestTradingRoutes:
    """Test trading-related endpoints"""

    def test_get_orders_without_auth(self):
        """Test accessing orders without authentication"""
        response = client.get("/api/v1/trading/orders")
        assert response.status_code == 403

    def test_get_orders_with_valid_token(self):
        """Test accessing orders with valid token"""
        # Register and get token
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "traderuser",
                "email": "trader@example.com",
                "password": "Test@12345"
            }
        )
        token = register_response.json().get("access_token")
        
        # Access orders
        response = client.get(
            "/api/v1/trading/orders",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "orders" in response.json()
        assert "user_id" in response.json()
