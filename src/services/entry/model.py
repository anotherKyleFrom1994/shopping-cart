from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class CreateProductIn(BaseModel):
    name: str
    price: int
    inventory: int


class CreateUserIn(BaseModel):
    name: str


class AddItemIn(BaseModel):
    cart_id: Optional[int]
    product_id: int


class CheckOutIn(BaseModel):
    order_id: Optional[int]
    cart_id: int
    user_id: int
