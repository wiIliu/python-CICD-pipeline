from sqlalchemy.orm import Session  # type: ignore

from faker import Faker

from orders_service.app.db_logic import crud
from orders_service.app.models.order import Order
from orders_service.app.schemas.order import OrderCreate
from orders_service.tests.factories.order_factory import OrderFactory


### CREATE TESTS ### 
def test_create_order(db: Session) -> None:
    data: Order = OrderFactory.build(name="testFactory")
    new_order = OrderCreate(**{
        "name": data.name,
        "product": data.product,
        "count": data.count,
        "price": data.price,
    })
    result = crud.create_order(db=db, new_order=new_order)
    
    # Assertions
    orders = db.query(Order).all()
    assert len(orders) == 1
    assert result.id is not None
    assert result.name == data.name

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



### DELETE TESTS ###


# def test_delete_todo(db: Session, todo: Todo) -> None:
#     todo2 = crud.todo.remove(db=db, id=todo.id)
#     todo3 = crud.todo.get(db=db, id=todo.id)
#     assert todo3 is None
#     assert todo2.id == todo.id
#     assert todo2.title == todo.title
#     assert todo2.owner_id == todo.owner_id



# orders = [
#     OrderFactory(name=f"user{i}", product="widget")
#     for i in range(100)
# ]

