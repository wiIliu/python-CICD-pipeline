from pydantic import BaseModel

class Order(BaseModel):
    name: str
    product: str
    count: int
    price: float
