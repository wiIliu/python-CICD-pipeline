import requests as r
from typing import Annotated, List
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/analytics",
    tags=["stats"],
)

@router.get("/")
def get_total_orders():
    orders = r.get("http://orders_service:8000/orders",timeout=10)
    total = len(orders.json()['items'])
    return total
