"""
User Routes
Author: Gabriel Demetrios Lafis

Endpoints for user profile management.
"""

from fastapi import APIRouter, Depends

from src.auth.jwt_handler import get_current_user

router = APIRouter()


@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile.

    Returns user-relevant fields from the JWT payload (excludes
    internal claims like token type and expiry).
    """
    return {
        "user_id": current_user.get("user_id"),
        "username": current_user.get("username"),
        "email": current_user.get("email"),
        "is_admin": current_user.get("is_admin", False),
    }
