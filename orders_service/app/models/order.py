from sqlalchemy import Column, Integer, String, Float
from ..core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    product = Column(String)
    count = Column(Integer)
    price = Column(Float)
