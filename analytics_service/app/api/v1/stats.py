from datetime import date
from fastapi import APIRouter
from analytics_service.app.service import analytics_service
from analytics_service.app.schemas.analytics import (
    SummaryResponse, RevenueResponse, OrderStatsResponse,
    DistributionResponse, DashboardResponse,
)

router = APIRouter(
    prefix="/analytics",
    tags=["stats"],
)


@router.get("/summary", response_model=SummaryResponse)
def get_summary(start_date: date | None = None, end_date: date | None = None):
    return analytics_service.get_summary(start_date, end_date)


@router.get("/orders", response_model=OrderStatsResponse)
def get_order_stats(start_date: date | None = None, end_date: date | None = None):
    return analytics_service.get_order_stats(start_date, end_date)


@router.get("/revenue", response_model=RevenueResponse)
def get_revenue_stats(start_date: date | None = None, end_date: date | None = None):
    return analytics_service.get_revenue_stats(start_date, end_date)


@router.get("/distribution", response_model=DistributionResponse)
def get_distribution(start_date: date | None = None, end_date: date | None = None):
    return analytics_service.get_distribution(start_date, end_date)


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(start_date: date | None = None, end_date: date | None = None):
    return analytics_service.get_dashboard(start_date, end_date)
