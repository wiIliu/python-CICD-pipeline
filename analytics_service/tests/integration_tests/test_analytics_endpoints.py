import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from analytics_service.app.main import app
from analytics_service.app.clients import orders_client


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_orders(monkeypatch, sample_orders):
    monkeypatch.setattr(orders_client, "get_orders", lambda: sample_orders)


@pytest.fixture
def mock_empty(monkeypatch, empty_orders):
    monkeypatch.setattr(orders_client, "get_orders", lambda: empty_orders)


# ---------------------------------------------------------------------------
# /analytics/summary
# ---------------------------------------------------------------------------

def test_summary_200(client, mock_orders):
    assert client.get("/analytics/summary").status_code == 200


def test_summary_totals(client, mock_orders):
    # sample_orders: 4 orders, totals 20+5+45+100 = 170, avg = 42.5
    data = client.get("/analytics/summary").json()
    assert data["total_orders"] == 4
    assert data["total_revenue"] == 170.0
    assert data["avg_order_value"] == 42.5


def test_summary_empty_orders(client, mock_empty):
    data = client.get("/analytics/summary").json()
    assert data["total_orders"] == 0
    assert data["total_revenue"] == 0.0
    assert data["avg_order_value"] == 0.0


def test_summary_start_date_filter(client, mock_orders):
    # Feb + Mar only: 2 orders, 45 + 100 = 145
    data = client.get("/analytics/summary?start_date=2025-02-01").json()
    assert data["total_orders"] == 2
    assert data["total_revenue"] == 145.0


def test_summary_end_date_filter(client, mock_orders):
    # Jan only: 2 orders, 20 + 5 = 25
    data = client.get("/analytics/summary?end_date=2025-01-31").json()
    assert data["total_orders"] == 2
    assert data["total_revenue"] == 25.0


def test_summary_date_range_filter(client, mock_orders):
    # Jan + Feb: 3 orders, 20 + 5 + 45 = 70
    data = client.get("/analytics/summary?start_date=2025-01-01&end_date=2025-02-28").json()
    assert data["total_orders"] == 3
    assert data["total_revenue"] == 70.0


def test_summary_date_range_no_match(client, mock_orders):
    data = client.get("/analytics/summary?start_date=2024-01-01&end_date=2024-12-31").json()
    assert data["total_orders"] == 0
    assert data["total_revenue"] == 0.0


def test_summary_invalid_date_422(client, mock_orders):
    assert client.get("/analytics/summary?start_date=not-a-date").status_code == 422


# ---------------------------------------------------------------------------
# /analytics/orders
# ---------------------------------------------------------------------------

def test_orders_200(client, mock_orders):
    assert client.get("/analytics/orders").status_code == 200


def test_orders_response_shape(client, mock_orders):
    data = client.get("/analytics/orders").json()
    assert {"total_orders", "per_day", "per_week", "per_month", "growth_rate"} <= data.keys()


def test_orders_total(client, mock_orders):
    assert client.get("/analytics/orders").json()["total_orders"] == 4


def test_orders_per_month(client, mock_orders):
    data = client.get("/analytics/orders").json()
    assert data["per_month"] == {"2025-01": 2, "2025-02": 1, "2025-03": 1}


def test_orders_growth_rate_multiple_months(client, mock_orders):
    # last two months: Feb=1, Mar=1 → 0% growth
    assert client.get("/analytics/orders").json()["growth_rate"] == 0.0


def test_orders_growth_rate_null_single_month(client, monkeypatch):
    monkeypatch.setattr(orders_client, "get_orders", lambda: {
        "items": [{"id": 1, "name": "A", "product": "X", "count": 1,
                   "price": 10.0, "total": 10.0, "created_at": "2025-01-15T00:00:00"}],
        "total": 1,
    })
    assert client.get("/analytics/orders").json()["growth_rate"] is None


def test_orders_date_filter(client, mock_orders):
    # Feb onward: 2 orders
    data = client.get("/analytics/orders?start_date=2025-02-01").json()
    assert data["total_orders"] == 2
    assert "2025-01" not in data["per_month"]


def test_orders_invalid_date_422(client, mock_orders):
    assert client.get("/analytics/orders?end_date=baddate").status_code == 422


# ---------------------------------------------------------------------------
# /analytics/revenue
# ---------------------------------------------------------------------------

def test_revenue_200(client, mock_orders):
    assert client.get("/analytics/revenue").status_code == 200


def test_revenue_response_shape(client, mock_orders):
    data = client.get("/analytics/revenue").json()
    assert {"total_revenue", "per_day", "per_week", "per_month", "growth_rate"} <= data.keys()


def test_revenue_total(client, mock_orders):
    assert client.get("/analytics/revenue").json()["total_revenue"] == 170.0


def test_revenue_per_month(client, mock_orders):
    data = client.get("/analytics/revenue").json()
    assert data["per_month"]["2025-01"] == 25.0
    assert data["per_month"]["2025-02"] == 45.0
    assert data["per_month"]["2025-03"] == 100.0


def test_revenue_growth_rate(client, mock_orders):
    # last two months: Feb=45, Mar=100 → ((100-45)/45)*100 = 122.22
    assert client.get("/analytics/revenue").json()["growth_rate"] == 122.22


def test_revenue_date_filter(client, mock_orders):
    data = client.get("/analytics/revenue?start_date=2025-01-01&end_date=2025-01-31").json()
    assert data["total_revenue"] == 25.0
    assert list(data["per_month"].keys()) == ["2025-01"]


def test_revenue_invalid_date_422(client, mock_orders):
    assert client.get("/analytics/revenue?start_date=2025-13-01").status_code == 422


# ---------------------------------------------------------------------------
# /analytics/distribution
# ---------------------------------------------------------------------------

def test_distribution_200(client, mock_orders):
    assert client.get("/analytics/distribution").status_code == 200


def test_distribution_values(client, mock_orders):
    # totals: [5, 20, 45, 100] — sorted median = (20+45)/2 = 32.5
    data = client.get("/analytics/distribution").json()
    assert data["largest"] == 100.0
    assert data["smallest"] == 5.0
    assert data["median"] == 32.5
    assert data["avg_order_value"] == 42.5


def test_distribution_empty_orders(client, mock_empty):
    data = client.get("/analytics/distribution").json()
    assert data["largest"] == 0.0
    assert data["smallest"] == 0.0
    assert data["median"] == 0.0
    assert data["avg_order_value"] == 0.0


def test_distribution_date_filter(client, mock_orders):
    # Jan only: totals [5, 20]
    data = client.get("/analytics/distribution?start_date=2025-01-01&end_date=2025-01-31").json()
    assert data["largest"] == 20.0
    assert data["smallest"] == 5.0
    assert data["median"] == 12.5
    assert data["avg_order_value"] == 12.5


# ---------------------------------------------------------------------------
# /analytics/dashboard
# ---------------------------------------------------------------------------

def test_dashboard_200(client, mock_orders):
    assert client.get("/analytics/dashboard").status_code == 200


def test_dashboard_top_level_keys(client, mock_orders):
    data = client.get("/analytics/dashboard").json()
    assert set(data.keys()) == {"summary", "revenue", "orders", "distribution"}


def test_dashboard_summary_consistent(client, mock_orders):
    # dashboard summary must match the dedicated summary endpoint
    dashboard = client.get("/analytics/dashboard").json()
    summary = client.get("/analytics/summary").json()
    assert dashboard["summary"] == summary


def test_dashboard_revenue_consistent(client, mock_orders):
    dashboard = client.get("/analytics/dashboard").json()
    revenue = client.get("/analytics/revenue").json()
    assert dashboard["revenue"] == revenue


def test_dashboard_date_filter(client, mock_orders):
    data = client.get("/analytics/dashboard?start_date=2025-01-01&end_date=2025-01-31").json()
    assert data["summary"]["total_orders"] == 2
    assert data["summary"]["total_revenue"] == 25.0
    assert data["distribution"]["largest"] == 20.0


def test_dashboard_invalid_date_422(client, mock_orders):
    assert client.get("/analytics/dashboard?start_date=2025-99-99").status_code == 422


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_orders_service_unavailable_503(client, monkeypatch):
    def raise_503():
        raise HTTPException(status_code=503, detail="Orders service unavailable")
    monkeypatch.setattr(orders_client, "get_orders", raise_503)
    assert client.get("/analytics/summary").status_code == 503


def test_orders_service_unavailable_all_endpoints(client, monkeypatch):
    def raise_503():
        raise HTTPException(status_code=503, detail="Orders service unavailable")
    monkeypatch.setattr(orders_client, "get_orders", raise_503)
    for endpoint in ["/analytics/summary", "/analytics/orders",
                     "/analytics/revenue", "/analytics/distribution", "/analytics/dashboard"]:
        assert client.get(endpoint).status_code == 503, f"Expected 503 for {endpoint}"
