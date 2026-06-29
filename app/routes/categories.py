from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List

try:
    from ..database import get_db
    from ..models import Categories
    from ..schemas import CategoryCreate, CategoryResponse, MessageResponse
except ImportError:
    from database import get_db
    from models import Categories
    from schemas import CategoryCreate, CategoryResponse, MessageResponse

category_router = APIRouter()

@category_router.post("/categories",response_model=CategoryResponse)
def create_categories(a:CategoryCreate,db = Depends(get_db)):
    category = Categories(
        name = a.name
    )
    db.add(category)
    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )
    return category

@category_router.get("/categories",response_model=List[CategoryResponse])
def get_categories(db=Depends(get_db)):
    all_categories = db.query(Categories).all()
    return all_categories

@category_router.get("/categories/{id}",response_model=CategoryResponse)
def get_categories_id(id:int,db=Depends(get_db)):
    category_id = db.query(Categories).filter(Categories.id == id).first()
    if not category_id:
        raise HTTPException (
        status_code = 404,
        detail = "Category not found"
    )
    return category_id

@category_router.put("/categories/{id}",response_model=CategoryResponse)
def update_category(id:int, a:CategoryCreate, db = Depends(get_db)):
    category_update  = db.query(Categories).filter(Categories.id == id).first()
    if not category_update:
        raise HTTPException (
        status_code = 404,
        detail = "Category not found"
    )
    category_update.name = a.name
    try:
        db.commit()
        db.refresh(category_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating category"
        )
    return category_update

@category_router.delete("/categories/{id}", response_model=MessageResponse)
def delete_category(id: int, db=Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    try:
        db.delete(category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category while products are still assigned to it"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting category"
        )

    return {"message": "Category deleted successfully"}



@category_router.get("/categories/{id}/products",response_model=List[CategoryResponse])
def find_category_byid(id:int,db = Depends(get_db)):
    category = db.query(Categories).filter(Categories.id == id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not Found"
        )
    return category.products


