"""
Trading Routes
Author: Gabriel Demetrios Lafis

Placeholder endpoints for trading operations (orders).
In a real system these would integrate with an order management service.
"""

from fastapi import APIRouter, Depends

from src.auth.jwt_handler import get_current_user

router = APIRouter()


@router.get("/orders")
async def get_orders(current_user: dict = Depends(get_current_user)):
    """
    List orders for the authenticated user.

    This is a demo endpoint; in production it would query a
    database or downstream order management service.
    """
    return {
        "orders": [],
        "total": 0,
        "user_id": current_user["user_id"],
        "message": "No orders found. This is a demo endpoint.",
    }
