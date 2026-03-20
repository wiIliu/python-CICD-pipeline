from datetime import date, datetime
from analytics_service.app.clients import orders_client
from analytics_service.app.business_logic import metrics_util
from analytics_service.app.schemas.analytics import (
    SummaryResponse, RevenueResponse, OrderStatsResponse,
    DistributionResponse, DashboardResponse,
)


def _filter_orders(orders: dict, start_date: date | None, end_date: date | None) -> dict:
    """Returns a new dict with items filtered by date range. Does not mutate the cache."""
    if not start_date and not end_date:
        return orders
    filtered = [
        o for o in orders['items']
        if (start_date is None or datetime.fromisoformat(o['created_at']).date() >= start_date)
        and (end_date is None or datetime.fromisoformat(o['created_at']).date() <= end_date)
    ]
    return {'items': filtered, 'total': len(filtered)}


def get_summary(start_date: date | None = None, end_date: date | None = None) -> SummaryResponse:
    orders = _filter_orders(orders_client.get_orders(), start_date, end_date)
    total = metrics_util.calc_total_order_count(orders)
    revenue = metrics_util.calc_total_revenue(orders)
    return SummaryResponse(
        total_orders=total,
        total_revenue=revenue,
        avg_order_value=revenue / total if total > 0 else 0.0,
    )


def get_revenue_stats(start_date: date | None = None, end_date: date | None = None) -> RevenueResponse:
    orders = _filter_orders(orders_client.get_orders(), start_date, end_date)
    per_month = metrics_util.calc_revenue_per_month(orders)
    return RevenueResponse(
        total_revenue=metrics_util.calc_total_revenue(orders),
        per_day=metrics_util.calc_revenue_per_day(orders),
        per_week=metrics_util.calc_revenue_per_week(orders),
        per_month=per_month,
        growth_rate=metrics_util.calc_growth_rate(per_month),
    )


def get_order_stats(start_date: date | None = None, end_date: date | None = None) -> OrderStatsResponse:
    orders = _filter_orders(orders_client.get_orders(), start_date, end_date)
    per_month = metrics_util.calc_orders_per_month(orders)
    return OrderStatsResponse(
        total_orders=metrics_util.calc_total_order_count(orders),
        per_day=metrics_util.calc_orders_per_day(orders),
        per_week=metrics_util.calc_orders_per_week(orders),
        per_month=per_month,
        growth_rate=metrics_util.calc_growth_rate(per_month),
    )


def get_distribution(start_date: date | None = None, end_date: date | None = None) -> DistributionResponse:
    orders = _filter_orders(orders_client.get_orders(), start_date, end_date)
    largest = metrics_util.largest_order_by_revenue(orders)
    smallest = metrics_util.smallest_order_by_revenue(orders)
    return DistributionResponse(
        largest=largest['total'] if largest else 0.0,
        smallest=smallest['total'] if smallest else 0.0,
        median=metrics_util.median_order_total(orders),
        avg_order_value=metrics_util.avg_order_value(orders),
    )


def get_dashboard(start_date: date | None = None, end_date: date | None = None) -> DashboardResponse:
    orders = _filter_orders(orders_client.get_orders(), start_date, end_date)

    # pre-compute shared values so metrics_util isn't called redundantly
    total_orders = metrics_util.calc_total_order_count(orders)
    total_revenue = metrics_util.calc_total_revenue(orders)
    aov = metrics_util.avg_order_value(orders)
    per_revenue_month = metrics_util.calc_revenue_per_month(orders)
    per_orders_month = metrics_util.calc_orders_per_month(orders)
    largest = metrics_util.largest_order_by_revenue(orders)
    smallest = metrics_util.smallest_order_by_revenue(orders)

    return DashboardResponse(
        summary=SummaryResponse(
            total_orders=total_orders,
            total_revenue=total_revenue,
            avg_order_value=aov,
        ),
        revenue=RevenueResponse(
            total_revenue=total_revenue,
            per_day=metrics_util.calc_revenue_per_day(orders),
            per_week=metrics_util.calc_revenue_per_week(orders),
            per_month=per_revenue_month,
            growth_rate=metrics_util.calc_growth_rate(per_revenue_month),
        ),
        orders=OrderStatsResponse(
            total_orders=total_orders,
            per_day=metrics_util.calc_orders_per_day(orders),
            per_week=metrics_util.calc_orders_per_week(orders),
            per_month=per_orders_month,
            growth_rate=metrics_util.calc_growth_rate(per_orders_month),
        ),
        distribution=DistributionResponse(
            largest=largest['total'] if largest else 0.0,
            smallest=smallest['total'] if smallest else 0.0,
            median=metrics_util.median_order_total(orders),
            avg_order_value=aov,
        ),
    )