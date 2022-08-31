from enum import unique
from ..database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Boolean


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    inventory = Column(Integer, nullable=False)


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)


class CartDetail(Base):
    __tablename__ = "cart_detail"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(String, nullable=False)
