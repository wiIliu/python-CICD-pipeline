import pytest
from pydantic import ValidationError
from analytics_service.app.schemas import analytics


### SummaryResponse ###

def test_valid_summary():
    summary = analytics.SummaryResponse(
        total_orders=5,
        total_revenue=12.7,
        avg_order_value=12.7 / 5,
    )
    assert summary.total_orders == 5
    assert summary.total_revenue == 12.7
    assert summary.avg_order_value == 2.54

def test_zero_order_summary():
    summary = analytics.SummaryResponse(
        total_orders=0,
        total_revenue=0,
        avg_order_value=0.0,
    )
    assert summary.total_orders == 0
    assert summary.total_revenue == 0.0
    assert summary.avg_order_value == 0.0

def test_summary_serializer():
    summary = analytics.SummaryResponse(
        total_orders=2,
        total_revenue=5.998,
        avg_order_value=5.998 / 2,
    )
    dumped = summary.model_dump()
    assert dumped["total_revenue"] == 6.00
    assert dumped["avg_order_value"] == 3.00

def test_summary_missing_field_raises():
    with pytest.raises(ValidationError):
        analytics.SummaryResponse(total_orders=1, total_revenue=10.0) 

def test_summary_wrong_type_raises():
    with pytest.raises(ValidationError):
        analytics.SummaryResponse(
            total_orders="not-a-number",
            total_revenue=10.0,
            avg_order_value=10.0,
        )


### RevenueResponse ###

def test_valid_revenue_response():
    revenue = analytics.RevenueResponse(
        total_revenue=150.0,
        per_day={"2025-01-15": 50.0, "2025-01-16": 100.0},
        per_week={"2025-W03": 150.0},
        per_month={"2025-01": 150.0},
        growth_rate=25.0,
    )
    assert revenue.total_revenue == 150.0
    assert revenue.per_day["2025-01-15"] == 50.0

def test_revenue_response_empty():
    revenue = analytics.RevenueResponse(
        total_revenue=0.0,
        per_day={},
        per_week={},
        per_month={},
        growth_rate=None,
    )
    assert revenue.growth_rate is None

def test_revenue_response_missing_field_raises():
    with pytest.raises(ValidationError):
        analytics.RevenueResponse(
            total_revenue=100.0,
            per_day={},
            per_week={},
        )


### OrderStatsResponse ###

def test_valid_order_stats_response():
    stats = analytics.OrderStatsResponse(
        total_orders=10,
        per_day={"2025-01-15": 4, "2025-01-16": 6},
        per_week={"2025-W03": 10},
        per_month={"2025-01": 10},
        growth_rate=-10.0,
    )
    assert stats.total_orders == 10
    assert stats.per_month["2025-01"] == 10

def test_order_stats_null_growth_rate():
    stats = analytics.OrderStatsResponse(
        total_orders=0,
        per_day={},
        per_week={},
        per_month={},
        growth_rate=None,
    )
    assert stats.growth_rate is None

def test_order_stats_missing_field_raises():
    with pytest.raises(ValidationError):
        analytics.OrderStatsResponse(
            total_orders=5,
            per_day={},
        )


### DistributionResponse ###

def test_valid_distribution_response():
    dist = analytics.DistributionResponse(
        largest=100.0,
        smallest=5.0,
        median=20.0,
        avg_order_value=42.5,
    )
    assert dist.largest == 100.0
    assert dist.smallest == 5.0
    assert dist.median == 20.0

def test_distribution_zeros():
    dist = analytics.DistributionResponse(
        largest=0.0,
        smallest=0.0,
        median=0.0,
        avg_order_value=0.0,
    )
    assert dist.largest == 0.0

def test_distribution_missing_field_raises():
    with pytest.raises(ValidationError):
        analytics.DistributionResponse(largest=100.0, smallest=5.0, median=20.0)


### DashboardResponse ###

def _make_summary(**overrides):
    defaults = {"total_orders": 4, "total_revenue": 170.0, "avg_order_value": 42.5}
    return analytics.SummaryResponse(**{**defaults, **overrides})

def _make_revenue(**overrides):
    defaults = {
        "total_revenue": 170.0,
        "per_day": {},
        "per_week": {},
        "per_month": {"2025-01": 25.0},
        "growth_rate": None,
    }
    return analytics.RevenueResponse(**{**defaults, **overrides})

def _make_order_stats(**overrides):
    defaults = {
        "total_orders": 4,
        "per_day": {},
        "per_week": {},
        "per_month": {"2025-01": 2},
        "growth_rate": None,
    }
    return analytics.OrderStatsResponse(**{**defaults, **overrides})

def _make_distribution(**overrides):
    defaults = {"largest": 100.0, "smallest": 5.0, "median": 32.5, "avg_order_value": 42.5}
    return analytics.DistributionResponse(**{**defaults, **overrides})

def test_valid_dashboard_response():
    dashboard = analytics.DashboardResponse(
        summary=_make_summary(),
        revenue=_make_revenue(),
        orders=_make_order_stats(),
        distribution=_make_distribution(),
    )
    assert dashboard.summary.total_orders == 4
    assert dashboard.revenue.total_revenue == 170.0
    assert dashboard.distribution.largest == 100.0

def test_dashboard_missing_nested_field_raises():
    with pytest.raises(ValidationError):
        analytics.DashboardResponse(
            summary=_make_summary(),
            revenue=_make_revenue(),
        )

def test_dashboard_wrong_nested_type_raises():
    with pytest.raises(ValidationError):
        analytics.DashboardResponse(
            summary={"not": "a SummaryResponse"},
            revenue=_make_revenue(),
            orders=_make_order_stats(),
            distribution=_make_distribution(),
        )