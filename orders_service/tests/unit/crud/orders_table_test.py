from sqlalchemy.orm import Session 

from orders_service.app.db_logic import crud
from orders_service.app.models.order import Order
from orders_service.app.schemas.order import OrderCreate, OrderUpdate
from orders_service.tests.factories.order_factory import OrderFactory


### CREATE TESTS ### 
def test_create_order(db: Session) -> None:
    data: Order = OrderFactory.build()
    new_order = OrderCreate(
        name=data.name,
        product=data.product,
        count=data.count,
        price=data.price,
    )

    result = crud.create_order(db=db, new_order=new_order)
    assert result.id is not None
    assert result.name == data.name

def test_created_order_persists_correctly(db: Session) -> None:
    data: Order = OrderFactory.build()
    new_order = OrderCreate(
        name=data.name,
        product=data.product,
        count=data.count,
        price=data.price,
    )

    result = crud.create_order(db=db, new_order=new_order)
    stored = db.query(Order).filter(Order.id == result.id).first()
    
    assert stored is not None
    assert stored.name == data.name
    assert stored.product == data.product
    assert stored.count == data.count
    assert stored.price == data.price

    orders = db.query(Order).all()
    assert len(orders) == 1



### RETRIEVE TESTS ###
def test_get_order_by_id(db: Session, fixture_order: Order) -> None:
    stored_order = crud.get_order_by_id(db=db, order_id=fixture_order.id)
    assert stored_order
    assert fixture_order.id == stored_order.id
    assert fixture_order.name == stored_order.name

def test_get_order_by_id_not_found(db: Session) -> None:
    OrderFactory.create_batch(5)
    order = crud.get_order_by_id(db=db, order_id=9999)
    assert order is None

def test_get_orders_all(db: Session) -> None:
    OrderFactory.create_batch(50)
    retrieved_orders = crud.get_orders(db=db)
    assert len(retrieved_orders) == 50

def test_get_orders_empty_db(db: Session) -> None:
    retrieved_orders = crud.get_orders(db=db)
    assert retrieved_orders == []

def test_get_orders_by_name(db: Session) -> None:
    target = "target_customer"
    OrderFactory.create_batch(15, name="buffer customer")
    OrderFactory.create_batch(10, name=target)

    retrieved_orders = crud.get_orders(db=db, name=target)
    assert len(retrieved_orders) == 10
    assert all(order.name == target for order in retrieved_orders)

def test_get_orders_by_product(db: Session) -> None:
    target = "target_product"
    OrderFactory.create_batch(15, product="buffer product")
    OrderFactory.create_batch(10, product=target)

    retrieved_orders = crud.get_orders(db=db, product=target)
    assert len(retrieved_orders) == 10
    assert all(order.product == target for order in retrieved_orders)

def test_get_orders_by_all_filters(db: Session) -> None:
    target_name = "target_customer"
    target_product = "target_product"
    
    OrderFactory.create_batch(5, name="temp customer", product="temp product")
    OrderFactory.create_batch(10, name=target_name, product="temp product 2")
    OrderFactory.create_batch(12, name="temp customer 2", product=target_product)
    OrderFactory.create_batch(6, name=target_name, product=target_product)

    retrieved_orders = crud.get_orders(db=db, name=target_name, product=target_product)
    assert len(retrieved_orders) == 6
    assert all(order.name == target_name for order in retrieved_orders)
    assert all(order.product == target_product for order in retrieved_orders)

def test_get_orders_by_filters_no_match(db: Session) -> None:
    target_name = "target_customer"
    target_product = "target_product"
    
    OrderFactory.create_batch(5, name="temp customer", product="temp product")
    OrderFactory.create_batch(10, name=target_name, product="temp product 2")
    OrderFactory.create_batch(12, name="temp customer 2", product=target_product)

    retrieved_orders = crud.get_orders(db=db, name=target_name, product=target_product)
    assert retrieved_orders == []



### UPDATE TESTS ###
def test_update_order(db: Session) -> None:
    db_list = OrderFactory.create_batch(5, name="old name")
    old_order = db_list[0]
    old_name = old_order.name
    old_count = old_order.count
    old_price = old_order.price
    old_product = old_order.product
    order_id = old_order.id

    updated_data = OrderUpdate(name="new name", count=old_count + 1)
    result = crud.update_order(db, order_id=order_id, data=updated_data)

    assert result
    assert result.id == order_id
    assert result.name != old_name
    assert result.name == "new name"
    assert result.count == old_count + 1
    assert result.price == old_price
    assert result.product == old_product


def test_update_order_no_changes(db: Session) -> None:
    db_list = OrderFactory.create_batch(5)
    old_order = db_list[0]
    old_name = old_order.name
    old_count = old_order.count
    old_price = old_order.price
    old_product = old_order.product
    order_id = old_order.id

    updated_data = OrderUpdate()
    result = crud.update_order(db, order_id=order_id, data=updated_data)

    assert result
    assert result.id == order_id
    assert result.name == old_name
    assert result.count == old_count
    assert result.price == old_price
    assert result.product == old_product

def test_update_order_invalid_id(db: Session) -> None:
    OrderFactory.create_batch(5)
    data = OrderUpdate()
    result = crud.update_order(db, order_id=9999, data=data)
    assert not result

def test_update_order_row_count_unchanged(db: Session):
    db_list = OrderFactory.create_batch(5, name="old name")
    updated_data = OrderUpdate(name="updated")
    result = crud.update_order(db, order_id=db_list[0].id, data=updated_data)

    assert result
    count = db.query(Order).count()
    assert count == 5



### DELETE TESTS ###
def test_delete_by_id(db: Session, fixture_order: Order) -> None:
    result = crud.delete_by_id(db, order_id=fixture_order.id)
    assert result
    assert result.id == fixture_order.id
    
    deleted = db.query(Order).filter(Order.id == fixture_order.id).first()
    assert deleted is None

def test_delete_by_id_not_found(db: Session) -> None:
    OrderFactory.create_batch(5)
    order = crud.delete_by_id(db=db, order_id=9999)
    assert order is None

def test_delete_reduces_row_count(db: Session):
    OrderFactory.create_batch(5)
    order = db.query(Order).first()
    crud.delete_by_id(db, order.id)

    remaining = db.query(Order).count()
    assert remaining == 4

def test_delete_same_id_twice(db: Session, fixture_order: Order):
    crud.delete_by_id(db, fixture_order.id)
    result = crud.delete_by_id(db, fixture_order.id)

    assert result is None
