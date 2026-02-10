from pydantic import BaseModel
from pydantic import ConfigDict


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
    
    model_config = ConfigDict(
        from_attributes=True
    )
        