from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str
    price: str
    inventory: int
