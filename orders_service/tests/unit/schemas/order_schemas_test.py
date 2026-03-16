import pytest
from pydantic import ValidationError
from orders_service.app.schemas import order


def test_order_create_invalid_name():
    with pytest.raises(ValidationError):
        order.OrderCreate(
            name="",
            product="apple",
            count=1,
            price=5.0,
        )

def test_order_create_invalid_product():
    with pytest.raises(ValidationError):
        order.OrderCreate(
            name="test1",
            product="a",
            count=1,
            price=5.0,
        )

def test_order_create_invalid_count():
    with pytest.raises(ValidationError):
        order.OrderCreate(
            name="test1",
            product="a",
            count=0,
            price=5.0,
        )

def test_order_create_invalid_price():
    with pytest.raises(ValidationError):
        order.OrderCreate(
            name="test1",
            product="a",
            count=1,
            price=-5.0,
        )
