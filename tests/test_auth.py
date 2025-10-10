import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "Secure Financial API Gateway", "version": "1.0.0", "status": "healthy", "docs": "/api/docs"}

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Test@12345"
        }
    )
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_login_user():
    # First, register a user if not already registered
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "Login@12345"
        }
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "Login@12345"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

