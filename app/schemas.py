from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class ProductCreate(BaseModel):
    name: str
    price: float
    category_id: int | None = None

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    category_id: int | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category_id: int | None = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CartCreate(BaseModel):
    qty: int
    product_id: int
class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    qty: int

    class Config:
        from_attributes = True
