from analytics_service.app.service.metrics_util import (
    avg_order_value,
    largest_order_by_revenue,
    largest_order_by_size,
    smallest_order_by_revenue,
    median_order_total,
    calc_total_order_count,
    calc_orders_per_day,
    calc_orders_per_week,
    calc_orders_per_month,
    calc_orders_per_product,
    calc_total_revenue,
    calc_revenue_per_day,
    calc_revenue_per_week,
    calc_revenue_per_month,
    calc_revenue_per_product,
    calc_growth_rate,
)
from analytics_service.tests.factories.order_dict_factory import make_order, make_orders


### Order counts ###

def test_calc_total_order_count():
    assert calc_total_order_count(make_orders(7)) == 7

def test_calc_total_order_count_empty(empty_orders):
    assert calc_total_order_count(empty_orders) == 0


def test_calc_orders_per_day():
    orders = {"items": [
        make_order(created_at="2025-01-15T10:06:00"),
        make_order(created_at="2025-01-15T11:59:59"),
        make_order(created_at="2025-01-16T09:00:00"),
        make_order(created_at="2026-01-14T09:00:00"),

    ], "total": 4}
    result = calc_orders_per_day(orders)
    assert  result == {"2025-01-15": 2, "2025-01-16": 1, "2026-01-14": 1}
    keys = list(result.keys())
    assert keys == sorted(keys)

def test_calc_orders_per_day_empty():
    orders = {"items": [], "total": 0}
    result = calc_orders_per_day(orders)
    assert not result


def test_calc_orders_per_week_count():
    orders = {"items": [
        make_order(created_at="2025-01-04T00:00:00"),  # week 1 - Jan. 4 is always week 1
        make_order(created_at="2025-01-06T00:00:00"),  # week 2
        make_order(created_at="2025-01-07T00:00:00"),  # week 2
        make_order(created_at="2025-01-13T00:00:00"),  # week 3
    ], "total": 4}
    result = calc_orders_per_week(orders)
    assert result["2025-W01"] == 1
    assert result["2025-W02"] == 2
    assert result["2025-W03"] == 1
    key = list(result.keys())[0]
    assert key == "2025-W01"

def test_calc_orders_per_week_empty():
    orders = {"items": [], "total": 0}
    result = calc_orders_per_week(orders)
    assert not result

def test_calc_orders_per_week_year_boundary():
    # 2024-12-30 is ISO week 2025-W01 (Monday of the week containing Jan 2 Thu)
    # using dt.year would incorrectly produce "2024-W01"
    orders = {"items": [make_order(created_at="2024-12-30T00:00:00")], "total": 1}
    result = calc_orders_per_week(orders)
    assert "2025-W01" in result


def test_calc_orders_per_month():
    orders = {"items": [
        make_order(created_at="2025-01-15T00:00:00"),
        make_order(created_at="2025-01-20T00:00:00"),
        make_order(created_at="2025-02-05T00:00:00"),
    ], "total": 3}
    result = calc_orders_per_month(orders)
    assert result == {"2025-01": 2, "2025-02": 1}
    keys = list(result.keys())
    assert keys == sorted(keys)

def test_calc_orders_per_month_empty():
    orders = {"items": [], "total": 0}
    assert not calc_orders_per_month(orders)


def test_calc_orders_per_product_counts():
    orders = {"items": [
        make_order(product="Widget"),
        make_order(product="Widget"),
        make_order(product="Gadget"),
    ], "total": 3}
    result = calc_orders_per_product(orders)
    assert result["Widget"] == 2
    assert result["Gadget"] == 1
    keys = list(result.keys())
    assert keys[0] == "Widget"

def test_calc_orders_per_product_empty(empty_orders):
    assert not calc_orders_per_product(empty_orders)


### Revenue ###

def test_calc_total_revenue(sample_orders):
    assert calc_total_revenue(sample_orders) == 170.0

def test_calc_total_revenue_single():
    orders = {"items": [make_order(total=99.99)], "total": 1}
    assert calc_total_revenue(orders) == 99.99

def test_calc_total_revenue_empty(empty_orders):
    assert calc_total_revenue(empty_orders) == 0.0


def test_calc_revenue_per_day():
    orders = {"items": [
        make_order(created_at="2025-01-15T10:00:00", total=10.0),
        make_order(created_at="2025-01-15T14:00:00", total=20.0),
        make_order(created_at="2025-01-16T09:00:00", total=5.0),
    ], "total": 3}
    assert calc_revenue_per_day(orders) == {"2025-01-15": 30.0, "2025-01-16": 5.0}

def test_calc_revenue_per_day_is_sorted():
    orders = {"items": [
        make_order(created_at="2025-01-16T00:00:00", total=10.0),
        make_order(created_at="2025-01-15T00:00:00", total=10.0),
    ], "total": 2}
    keys = list(calc_revenue_per_day(orders).keys())
    assert keys == sorted(keys)


def test_calc_revenue_per_week():
    orders = {"items": [
        make_order(created_at="2025-01-06T00:00:00", total=40.0),  # week 2
        make_order(created_at="2025-01-07T00:00:00", total=60.0),  # week 2
        make_order(created_at="2025-01-13T00:00:00", total=25.0),  # week 3
    ], "total": 3}
    result = calc_revenue_per_week(orders)
    assert result["2025-W02"] == 100.0
    assert result["2025-W03"] == 25.0

def test_calc_revenue_per_week_year_boundary():
    # 2024-12-30 is ISO week 2025-W01 — year from dt.year would be wrong
    orders = {"items": [make_order(created_at="2024-12-30T00:00:00", total=50.0)], "total": 1}
    result = calc_revenue_per_week(orders)
    assert "2025-W01" in result
    assert result["2025-W01"] == 50.0

def test_calc_revenue_per_week_is_sorted():
    orders = {"items": [
        make_order(created_at="2025-01-13T00:00:00", total=10.0),  # week 3
        make_order(created_at="2025-01-06T00:00:00", total=10.0),  # week 2
    ], "total": 2}
    keys = list(calc_revenue_per_week(orders).keys())
    assert keys == sorted(keys)


def test_calc_revenue_per_month(sample_orders):
    result = calc_revenue_per_month(sample_orders)
    assert result["2025-01"] == 25.0   # 20 + 5
    assert result["2025-02"] == 45.0
    assert result["2025-03"] == 100.0

def test_calc_revenue_per_month_is_sorted():
    orders = {"items": [
        make_order(created_at="2025-03-01T00:00:00", total=10.0),
        make_order(created_at="2025-01-01T00:00:00", total=10.0),
        make_order(created_at="2025-02-01T00:00:00", total=10.0),
    ], "total": 3}
    keys = list(calc_revenue_per_month(orders).keys())
    assert keys == sorted(keys)


def test_calc_revenue_per_product(sample_orders):
    result = calc_revenue_per_product(sample_orders)
    assert result["Widget"] == 25.0
    assert result["Gadget"] == 145.0

def test_calc_revenue_per_product_sorted_descending(sample_orders):
    keys = list(calc_revenue_per_product(sample_orders).keys())
    assert keys[0] == "Gadget"  # 145 > 25

def test_calc_revenue_per_product_empty(empty_orders):
    assert calc_revenue_per_product(empty_orders) == {}


# --- Growth ---

def test_calc_growth_rate_positive():
    assert calc_growth_rate({"2025-01": 100.0, "2025-02": 120.0}) == 20.0

def test_calc_growth_rate_negative():
    assert calc_growth_rate({"2025-01": 100.0, "2025-02": 80.0}) == -20.0

def test_calc_growth_rate_single_period():
    assert calc_growth_rate({"2025-01": 100.0}) is None

def test_calc_growth_rate_empty():
    assert calc_growth_rate({}) is None

def test_calc_growth_rate_zero_previous():
    assert calc_growth_rate({"2025-01": 0.0, "2025-02": 100.0}) is None

def test_calc_growth_rate_no_change():
    assert calc_growth_rate({"2025-01": 100.0, "2025-02": 100.0}) == 0.0

def test_calc_growth_rate_rounding():
    assert calc_growth_rate({"2025-01": 3.0, "2025-02": 4.0}) == 33.33

def test_calc_growth_rate_uses_last_two_periods():
    # only the last two values should be compared, regardless of earlier history
    result = calc_growth_rate({"2024-11": 999.0, "2024-12": 999.0, "2025-01": 100.0, "2025-02": 200.0})
    assert result == 100.0


    

# --- Distribution ---

def test_avg_order_value(sample_orders):
    # totals: 20 + 5 + 45 + 100 = 170, count = 4, avg = 42.5
    assert avg_order_value(sample_orders) == 42.5

def test_avg_order_value_single():
    orders = {"items": [make_order(total=37.5)], "total": 1}
    assert avg_order_value(orders) == 37.5

def test_avg_order_value_empty(empty_orders):
    assert avg_order_value(empty_orders) == 0.0


def test_largest_order_by_revenue():
    orders = {"items": [make_order(total=5.0), make_order(total=100.0), make_order(total=20.0)], "total": 3}
    assert largest_order_by_revenue(orders)["total"] == 100.0

def test_largest_order_by_revenue_empty(empty_orders):
    assert largest_order_by_revenue(empty_orders) is None


def test_largest_order_by_size():
    orders = {"items": [make_order(count=1), make_order(count=10), make_order(count=5)], "total": 3}
    assert largest_order_by_size(orders)["count"] == 10

def test_largest_order_by_size_empty(empty_orders):
    assert largest_order_by_size(empty_orders) is None


def test_smallest_order_by_revenue():
    orders = {"items": [make_order(total=5.0), make_order(total=100.0), make_order(total=20.0)], "total": 3}
    assert smallest_order_by_revenue(orders)["total"] == 5.0

def test_smallest_order_by_revenue_empty(empty_orders):
    assert smallest_order_by_revenue(empty_orders) is None


def test_median_order_total():
    orders = {"items": [make_order(total=10.0), make_order(total=30.0), make_order(total=20.0)], "total": 3}
    assert median_order_total(orders) == 20.0

def test_median_order_total_even_count():
    orders = {"items": [make_order(total=10.0), make_order(total=20.0)], "total": 2}
    assert median_order_total(orders) == 15.0

def test_median_order_total_single():
    orders = {"items": [make_order(total=42.0)], "total": 1}
    assert median_order_total(orders) == 42.0

def test_median_order_total_empty(empty_orders):
    assert median_order_total(empty_orders) == 0.0

