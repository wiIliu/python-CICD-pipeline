from sqlalchemy.orm import Session
from orders_service.app.models.order import Order
from orders_service.app.schemas import order


def create_order(db: Session, new_order : order.OrderCreate):
    db_order = Order(**new_order.model_dump())
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        print("EXCEPTION:", repr(e))
        raise
    return db_order


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session,
               name: str | None = None,
               product: str | None = None,
               offset=0,
               limit=10):
    query = db.query(Order)

    if name:
        query = query.filter(Order.name == name)
    if product:
        query = query.filter(Order.product == product)

    orders = query.offset(offset).limit(limit).all()
    total = query.count()
    return orders, total


def delete_by_id(db: Session, order_id: int):
    try:
        result = get_order_by_id(db, order_id)
        if not result:
            return None
        db.delete(result)
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        print("EXCEPTION:", repr(e))
        raise


def update_order(db: Session, order_id: int, data: order.OrderUpdate):
    result = get_order_by_id(db, order_id)
    if not result:
        return None
    try:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(result, field, value)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        db.rollback()
        print("EXCEPTION:", repr(e))
        raise
