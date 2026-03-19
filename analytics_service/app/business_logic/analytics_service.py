from analytics_service.app.clients import orders_client
from analytics_service.app.business_logic import metrics_util


def get_summary():

    orders = orders_client.get_orders()

    revenue = metrics_util.calc_total_revenue(orders=orders)
    total = metrics_util.calc_total_order_count(orders=orders)

    avg_value = 0
    if total > 0:
        avg_value = revenue / total

    return {'total_orders': total,
            'total_revenue': revenue,
            "avg_value": avg_value}


