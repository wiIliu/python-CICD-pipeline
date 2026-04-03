import pytest
from analytics_service.tests.factories.order_dict_factory import make_order


@pytest.fixture
def empty_orders():
    return {"items": [], "total": 0}


@pytest.fixture
def sample_orders():
    return {
        "items": [
            make_order(product="Widget", count=2, price=10.0,  total=20.0,  created_at="2025-01-15T10:00:00"),
            make_order(product="Widget", count=1, price=5.0,   total=5.0,   created_at="2025-01-15T14:00:00"),
            make_order(product="Gadget", count=3, price=15.0,  total=45.0,  created_at="2025-02-10T09:00:00"),
            make_order(product="Gadget", count=1, price=100.0, total=100.0, created_at="2025-03-01T08:00:00"),
        ],
        "total": 4,
    }
