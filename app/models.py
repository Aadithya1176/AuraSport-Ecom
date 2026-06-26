from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String, Column, Float
from sqlalchemy import ForeignKey

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    orders = relationship("Orders",
                          back_populates="user")
class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship("Users",
                        back_populates="orders")
    
class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    products = relationship("Products",back_populates="category")

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    category_id = Column(Integer,
                         ForeignKey("categories.id"))
    
    category = relationship("Categories",back_populates="products")



    