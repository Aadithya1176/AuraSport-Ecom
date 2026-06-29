from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

try:
    from .database import Base
except ImportError:
    from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    orders = relationship("Orders", back_populates="user")
    cart_items = relationship("Cart", back_populates="user")


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship("Users", back_populates="orders")


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    products = relationship("Products", back_populates="category")


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Categories", back_populates="products")
    cart_items = relationship("Cart", back_populates="product")
    

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,
                     ForeignKey("users.id")
    )
    product_id = Column(Integer,
                        ForeignKey("products.id"))
    qty = Column(Integer)
    user = relationship("Users", back_populates="cart_items")
    product = relationship("Products", back_populates="cart_items")

    
