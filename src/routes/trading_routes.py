"""Trading Routes"""
from fastapi import APIRouter, Depends
from src.auth.jwt_handler import get_current_user

router = APIRouter()

@router.get("/orders")
async def get_orders(current_user: dict = Depends(get_current_user)):
    return {"orders": [], "user_id": current_user["user_id"]}
