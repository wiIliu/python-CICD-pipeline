from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.order import OrderCreate, OrderResponse
from ...dependencies.db import get_db
from ...models.order import Order

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order : OrderCreate, db: Annotated[Session, Depends(get_db)]):
    db_order = Order(name=order.name,product=order.product, price=order.price, count=order.count)
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        print("🔥 EXCEPTION:", repr(e))
        raise
    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Annotated[Session, Depends(get_db)]) -> OrderResponse:
    if order_id not in db:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_id
