from enum import Enum
from typing import Optional
from pydantic import BaseModel


class OrderStatus(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    EXPIRED = "EXPIRED"


class OrderIn(BaseModel):
    user_id: int
    cart_id: int
    status: str


class OrderUpdateIn(OrderIn):
    id: int
