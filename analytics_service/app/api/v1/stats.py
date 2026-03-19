# from typing import Annotated, List
from fastapi import APIRouter, HTTPException
from analytics_service.app.business_logic import analytics_service


router = APIRouter(
    prefix="/analytics",
    tags=["stats"],
)


# could also get summary per user/customer
@router.get("/summary")
def get_summary():
    return analytics_service.get_summary()




# @router.get("/orders")

# @router.get("/revenue")

# @router.get("/distribution")

# @router.get("/dashboard") # return everything



