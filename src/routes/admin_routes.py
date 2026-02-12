"""
Admin Routes
Author: Gabriel Demetrios Lafis

Administrative endpoints for user management.
"""

from fastapi import APIRouter, Depends

from src.auth.jwt_handler import get_current_admin_user
from src.routes.auth_routes import users_db

router = APIRouter()


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_admin_user)):
    """
    List all registered users (admin only).

    Returns user summaries without sensitive fields like password hashes.
    """
    users = [
        {
            "user_id": u["user_id"],
            "username": u["username"],
            "email": u["email"],
            "is_admin": u["is_admin"],
            "is_active": u["is_active"],
        }
        for u in users_db.values()
    ]
    return {
        "users": users,
        "total": len(users),
        "admin": current_user["username"],
    }
