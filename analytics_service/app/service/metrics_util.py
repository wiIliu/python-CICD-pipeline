import statistics
from datetime import datetime
from collections import defaultdict


### ORDER COUNTS ###

def calc_total_order_count(orders: dict) -> int:
    return len(orders['items'])

def calc_orders_per_day(orders: dict) -> dict[str, int]:
    day_totals = defaultdict(int)
    for order in orders['items']:
        date = datetime.fromisoformat(order['created_at']).date().isoformat()
        day_totals[date] += 1
    return dict(sorted(day_totals.items()))

def calc_orders_per_week(orders: dict) -> dict[str, int]:
    week_totals = defaultdict(int)
    for order in orders['items']:
        dt = datetime.fromisoformat(order['created_at'])
        iso = dt.isocalendar()
        week_key = f"{iso.year}-W{iso.week:02d}"
        week_totals[week_key] += 1
    return dict(sorted(week_totals.items()))

def calc_orders_per_month(orders: dict) -> dict[str, int]:
    month_totals = defaultdict(int)
    for order in orders['items']:
        month = datetime.fromisoformat(order['created_at']).strftime("%Y-%m")
        month_totals[month] += 1
    return dict(sorted(month_totals.items()))

def calc_orders_per_product(orders: dict) -> dict[str, int]:
    product_totals = defaultdict(int)
    for order in orders['items']:
        product_totals[order['product']] += 1
    return dict(sorted(product_totals.items(), key=lambda x: x[1], reverse=True))


### REVENUE ###

def calc_total_revenue(orders: dict) -> float:
    return sum(order['total'] for order in orders['items'])

def calc_revenue_per_day(orders: dict) -> dict[str, float]:
    day_totals = defaultdict(float)
    for order in orders['items']:
        date = datetime.fromisoformat(order['created_at']).date().isoformat()
        day_totals[date] += order['total']
    return dict(sorted(day_totals.items()))

def calc_revenue_per_week(orders: dict) -> dict[str, float]:
    week_totals = defaultdict(float)
    for order in orders['items']:
        dt = datetime.fromisoformat(order['created_at'])
        iso = dt.isocalendar()
        week_key = f"{iso.year}-W{iso.week:02d}"
        week_totals[week_key] += order['total']
    return dict(sorted(week_totals.items()))

def calc_revenue_per_month(orders: dict) -> dict[str, float]:
    month_totals = defaultdict(float)
    for order in orders['items']:
        month = datetime.fromisoformat(order['created_at']).strftime("%Y-%m")
        month_totals[month] += order['total']
    return dict(sorted(month_totals.items()))

def calc_revenue_per_product(orders: dict) -> dict[str, float]:
    product_totals = defaultdict(float)
    for order in orders['items']:
        product_totals[order['product']] += order['total']
    return dict(sorted(product_totals.items(), key=lambda x: x[1], reverse=True))


### GROWTH ###

def calc_growth_rate(period_totals: dict[str, float | int]) -> float | None:
    if len(period_totals) < 2:
        return None
    values = list(period_totals.values())
    previous, current = values[-2], values[-1]
    if previous == 0:
        return None
    return round(((current - previous) / previous) * 100, 2)


### DISTRIBUTION ###

def avg_order_value(orders: dict) -> float:
    total = calc_total_order_count(orders)
    if total == 0:
        return 0.0
    return calc_total_revenue(orders=orders) / total

def largest_order_by_revenue(orders: dict) -> dict | None:
    if not orders['items']:
        return None
    return max(orders['items'], key=lambda order: order['total'])

def largest_order_by_size(orders: dict) -> dict | None:
    if not orders['items']:
        return None
    return max(orders['items'], key=lambda order: order['count'])

def smallest_order_by_revenue(orders: dict) -> dict | None:
    if not orders['items']:
        return None
    return min(orders['items'], key=lambda order: order['total'])

def median_order_total(orders: dict) -> float:
    totals = [float(order['total']) for order in orders.get('items', []) if 'total' in order]
    if not totals:
        return 0.0
    return statistics.median(totals)

# calc_order_value_percentiles — p50/p75/p90 via statistics.quantiles


