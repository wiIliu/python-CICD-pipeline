from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from ...schemas.order import Order


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

order_db={}

@router.post("/")
def create_order(order : Order):
    if order.id not in order_db:
        order_db[order.id] = order
        return {"message": "Order placed successfully"}
    raise HTTPException(status_code=400, detail="Order already exists")

@router.get("/{order_id}")
def get_order(order_id: int):
    if order_id not in order_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_db[order_id]
