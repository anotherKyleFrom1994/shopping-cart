from pydantic import BaseModel


class CartIn(BaseModel):
    product_id: int
