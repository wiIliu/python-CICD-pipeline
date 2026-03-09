from sqlalchemy.orm import Session  # type: ignore

from faker import Faker

from orders_service.app.db_logic import crud
from orders_service.app.models.order import Order
from orders_service.app.schemas.order import OrderCreate
from orders_service.tests.factories.order_factory import OrderFactory

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


def test_get_order_by_id(db: Session, fixture_order: Order) -> None:
    stored_order = crud.get_order_by_id(db=db, order_id=fixture_order.id)
    assert stored_order
    assert fixture_order.id == stored_order.id


# def test_delete_todo(db: Session, todo: Todo) -> None:
#     todo2 = crud.todo.remove(db=db, id=todo.id)
#     todo3 = crud.todo.get(db=db, id=todo.id)
#     assert todo3 is None
#     assert todo2.id == todo.id
#     assert todo2.title == todo.title
#     assert todo2.owner_id == todo.owner_id