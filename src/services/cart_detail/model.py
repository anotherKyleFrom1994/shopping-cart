from pydantic import BaseModel


class CartDetailIn(BaseModel):
    cart_id: int
    product_id: int
