from pydantic import BaseModel, field_serializer


class SummaryResponse(BaseModel):
    total_orders: int
    total_revenue: float
    avg_order_value: float

    @field_serializer('total_revenue', 'avg_order_value')
    def round_currency(self, v: float) -> float:
        return round(v, 2)


class RevenueResponse(BaseModel):
    total_revenue: float
    per_day: dict[str, float]
    per_week: dict[str, float]
    per_month: dict[str, float]
    growth_rate: float | None


class OrderStatsResponse(BaseModel):
    total_orders: int
    per_day: dict[str, int]
    per_week: dict[str, int]
    per_month: dict[str, int]
    growth_rate: float | None


class DistributionResponse(BaseModel):
    largest: float
    smallest: float
    median: float
    avg_order_value: float


class DashboardResponse(BaseModel):
    summary: SummaryResponse
    revenue: RevenueResponse
    orders: OrderStatsResponse
    distribution: DistributionResponse
    