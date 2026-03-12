from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ...dependencies.db import get_db


router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/")
def get_health():
    return {"status": "OK"}

@router.get("/db")
def get_health_db(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))
        print("✅ DB connection OK")
    finally:
        db.close()
    return {"status": "OK"}

@router.get("/db/orders")
def get_health_orders(db: Annotated[Session, Depends(get_db)]):
    try:
        r = db.execute(text("SELECT * FROM orders")).fetchall()
        print("Data output: ", r)
    finally:
        db.close()
    return {"status": "OK"}
