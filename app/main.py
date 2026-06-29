from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

try:
    from .database import engine
    from .init_db import init_db
    from .models import Base
    from .routes.cart import cart_router
    from .routes.categories import category_router
    from .routes.products import router as products_router
    from .routes.users import user_router
except ImportError:
    from database import engine
    from init_db import init_db
    from models import Base
    from routes.cart import cart_router
    from routes.categories import category_router
    from routes.products import router as products_router
    from routes.users import user_router

app = FastAPI(title="AuraSport Backend")

@app.on_event("startup")
def create_tables() -> None:
    try:
        init_db()
    except SQLAlchemyError as exc:
        print(f"Database connection warning: {exc}")

app.include_router(user_router)
app.include_router(category_router)
app.include_router(products_router)
app.include_router(cart_router)
