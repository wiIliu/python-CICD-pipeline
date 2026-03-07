from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderListResponse
from ...dependencies.db import get_db
from ...db_logic import crud
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=OrderResponse, status_code=201)
def post_order(order : OrderCreate, db: Annotated[Session, Depends(get_db)]):
    return crud.create_order(db, order)


@router.get("/", response_model=OrderListResponse)
def get_orders(db: Annotated[Session, Depends(get_db)],
                        name: str | None = None,
                        product: str | None = None):
    orders = crud.get_orders(db ,name, product)
    return {"items": orders}

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_from_id(order_id: int, db: Annotated[Session, Depends(get_db)]) -> OrderResponse:
    order = crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order


@router.delete("/{order_id}", status_code=204)
def delete_by_id(order_id: int, db: Annotated[Session, Depends(get_db)]):
    result = crud.delete_by_id(db, order_id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    # return result


@router.put("/{order_id}", response_model=OrderResponse, status_code=200)
def update_order(order_id: int, data: OrderUpdate, db: Annotated[Session, Depends(get_db)]):
    result = crud.update_order(db, order_id, data)
    if not result: 
        raise HTTPException(status_code=404, detail="Order not found")
    return result
