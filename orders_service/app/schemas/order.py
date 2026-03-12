from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OrderBase(BaseModel):
    name: str = Field(min_length=2)
    product: str = Field(min_length=2)
    count: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    total: float

    model_config = ConfigDict(
        from_attributes=True
    )

class OrderListResponse(BaseModel):
    items: list[OrderResponse]

class OrderUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2)
    product: str | None = Field(default=None, min_length=2)
    count: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
        