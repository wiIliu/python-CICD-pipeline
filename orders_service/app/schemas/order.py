from pydantic import BaseModel

class OrderCreate(BaseModel):
    name: str
    product: str
    count: int
    price: float

class OrderResponse(BaseModel):
    id: int
    name: str
    product: str
    count: int
    price: float
    class Config:
        from_attributes = True
        