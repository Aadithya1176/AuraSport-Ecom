from fastapi import APIRouter, Depends
from typing import List

try:
    from ..database import get_db
    from ..models import Categories
    from ..schemas import CategoryCreate, CategoryResponse
except ImportError:
    from database import get_db
    from models import Categories
    from schemas import CategoryCreate, CategoryResponse

category_router = APIRouter()

@category_router.post("/categories",response_model=CategoryResponse)
def create_categories(a:CategoryCreate,db = Depends(get_db)):
    category = Categories(
        name = a.name
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@category_router.get("/categories",response_model=List[CategoryResponse])
def get_categories(db=Depends(get_db)):
    all_categories = db.query(Categories).all()
    return all_categories



