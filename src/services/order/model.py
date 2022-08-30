from pydantic import BaseModel


class OrderIn(BaseModel):
    user_id: int
    cart_id: int
