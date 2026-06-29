from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List

try:
    from ..auth import get_current_user
    from ..database import get_db
    from ..models import Products
    from ..schemas import MessageResponse, ProductCreate, ProductResponse, ProductUpdate
except ImportError:
    from auth import get_current_user
    from database import get_db
    from models import Products
    from schemas import MessageResponse, ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def create_product(a:ProductCreate,
                   db=Depends(get_db),
                   user=Depends(get_current_user)):
    products = Products(
        name = a.name,
        price = a.price,
        category_id = a.category_id
    )

    db.add(products)
    try:
        db.commit()
        db.refresh(products)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category or duplicate product data"
        )
    return products


@router.get("/products",response_model=List[ProductResponse])
def get_products(limit:int=1,
                 offset:int=0,
                 min_price: int | None = None,
                 sort: str | None = None,
                 db=Depends(get_db)):
    query = db.query(Products)
    if sort == "price":
        query = query.order_by(Products.price)
    elif sort == "-price":
        query = query.order_by(Products.price.desc())
    if min_price is not None:
        query = query.filter(Products.price >= min_price)
    products = query.offset(offset).limit(limit).all()
    return products

@router.get("/products/{id}",response_model=ProductResponse)
def get_products_by_id(id:int,db=Depends(get_db)):
    products = db.query(Products).filter(Products.id==id).first()
    if products:
        return products
    else:
        raise HTTPException (
            status_code=404,
            detail="Product not found"
        )
    


@router.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, a: ProductCreate,db=Depends(get_db)):
    product = db.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = a.name
    product.price = a.price
    product.category_id = a.category_id

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category or duplicate product data"
        )

    return product

@router.patch("/products/{id}", response_model=ProductResponse)
def patch_product(id: int, a: ProductUpdate,db=Depends(get_db)):
    product = db.query(Products).filter(Products.id == id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if a.name is not None:
        product.name = a.name

    if a.price is not None:
        product.price = a.price
    
    if a.category_id is not None:
        product.category_id = a.category_id

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid category or duplicate product data"
        )

    return product
    
@router.delete("/products/{id}", response_model=MessageResponse)
def delete_product(id:int,db=Depends(get_db)):
    product = db.query(Products).filter(Products.id == id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
