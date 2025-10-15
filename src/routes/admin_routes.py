"""Admin Routes"""

from fastapi import APIRouter, Depends

from src.auth.jwt_handler import get_current_admin_user

router = APIRouter()


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_admin_user)):
    return {"users": [], "admin": current_user["username"]}
