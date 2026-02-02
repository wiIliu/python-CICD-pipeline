from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...schemas.order import Order
from ...dependencies.db import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/")
def create_order(order : Order, db: Session = Depends(get_db)):
    if order.id not in db:
        db[order.id] = order
        return {"message": "Order placed successfully"}
    raise HTTPException(status_code=400, detail="Order already exists")

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = De[Depends(get_db)]):
    if order_id not in db:
        raise HTTPException(status_code=404, detail="Order not found")
    return db[order_id]
