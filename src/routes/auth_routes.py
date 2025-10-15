"""
Authentication Routes
Author: Gabriel Demetrios Lafis

Routes for user authentication and authorization.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from src.auth.jwt_handler import JWTHandler, get_current_user

router = APIRouter()

# In-memory user database (for demo purposes)
users_db = {
    "admin@example.com": {
        "user_id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": JWTHandler.hash_password("admin123"),
        "is_admin": True,
        "is_active": True,
    },
    "user@example.com": {
        "user_id": 2,
        "username": "user",
        "email": "user@example.com",
        "password_hash": JWTHandler.hash_password("user123"),
        "is_admin": False,
        "is_active": True,
    },
}


# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login endpoint

    Returns JWT access and refresh tokens.
    """
    # Find user
    user = users_db.get(request.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Verify password
    if not JWTHandler.verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Check if user is active
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    # Create tokens
    token_data = {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"],
        "is_admin": user["is_admin"],
    }

    access_token = JWTHandler.create_access_token(token_data)
    refresh_token = JWTHandler.create_refresh_token({"user_id": user["user_id"]})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(request: RegisterRequest):
    """
    Register new user

    Creates a new user account and returns tokens.
    """
    # Check if email already exists
    if request.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    # Create new user
    new_user_id = max([u["user_id"] for u in users_db.values()]) + 1 if users_db else 1

    new_user = {
        "user_id": new_user_id,
        "username": request.username,
        "email": request.email,
        "password_hash": JWTHandler.hash_password(request.password),
        "is_admin": False,
        "is_active": True,
    }

    users_db[request.email] = new_user

    # Create tokens
    token_data = {
        "user_id": new_user["user_id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "is_admin": new_user["is_admin"],
    }

    access_token = JWTHandler.create_access_token(token_data)
    refresh_token = JWTHandler.create_refresh_token({"user_id": new_user["user_id"]})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token

    Uses refresh token to generate a new access token.
    """
    # Verify refresh token
    payload = JWTHandler.verify_token(request.refresh_token)

    # Verify token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
        )

    # Find user
    user_id = payload.get("user_id")
    user = next((u for u in users_db.values() if u["user_id"] == user_id), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    # Create new access token
    token_data = {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"],
        "is_admin": user["is_admin"],
    }

    access_token = JWTHandler.create_access_token(token_data)

    return TokenResponse(access_token=access_token, refresh_token=request.refresh_token)


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information

    Returns information about the authenticated user.
    """
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "email": current_user["email"],
        "is_admin": current_user["is_admin"],
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout endpoint

    In a production system, this would invalidate the token.
    """
    return {"message": "Successfully logged out", "user_id": current_user["user_id"]}
