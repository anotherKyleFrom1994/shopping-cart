from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class CreateProductIn(BaseModel):
    name: str
    price: int
    inventory: int


class AddItemIn(BaseModel):
    cart_id: Optional[int]
    product_id: int


class CheckOutIn(BaseModel):
    pass
