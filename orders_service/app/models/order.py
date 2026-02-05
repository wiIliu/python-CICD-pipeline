from sqlalchemy import Column, Integer, String, Float
from orders_service.app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    product = Column(String)
    count = Column(Integer)
    price = Column(Float)
    def __repr__(self) -> str:
        return f"Order(id={self.id})"
