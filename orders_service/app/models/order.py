import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from orders_service.app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), CheckConstraint('char_length(name) > 1', name='val_name_len'), nullable=False)
    product = Column(String(150), CheckConstraint('char_length(product) > 1', name='val_product_len'), nullable=False)
    count = Column(Integer, CheckConstraint("count>0"), nullable=False,)
    price = Column(Float, CheckConstraint("price>0"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    @property
    def total(self):
        return round((self.price * self.count), 2)

    def __repr__(self) -> str:
        return f"Order(id={self.id})"
    