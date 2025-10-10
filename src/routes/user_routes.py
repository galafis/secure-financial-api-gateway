"""User Routes"""
from fastapi import APIRouter, Depends
from src.auth.jwt_handler import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
