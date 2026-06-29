from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List

try:
    from ..database import get_db
    from ..models import Cart, Users, Products
    from ..schemas import CartCreate, CartResponse
    from ..auth import get_current_user
except ImportError:
    from database import get_db
    from models import Cart, Users, Products
    from schemas import CartCreate, CartResponse
    from auth import get_current_user

cart_router = APIRouter()

@cart_router.post("/carts", response_model=CartResponse)
def add_to_cart(a:CartCreate,
                db = Depends(get_db),
                current_user = Depends(get_current_user)):
    user = db.query(Users).filter(Users.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.query(Products).filter(
        Products.id == a.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    cart_item = db.query(Cart).filter(
        Cart.user_id == user.id,
        Cart.product_id == a.product_id
        ).first()
    if cart_item:
        cart_item.qty += a.qty
        try:
            db.commit()
            db.refresh(cart_item)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error while updating cart"
            )
        return cart_item
    else:
        cart_item = Cart(
            user_id = user.id,
            product_id = a.product_id,
            qty = a.qty
        )

        db.add(cart_item)
        try:
            db.commit()
            db.refresh(cart_item)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Invalid cart item data"
            )
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error while adding to cart"
            )

        return cart_item

@cart_router.get("/cart",response_model=List[CartResponse])
def get_cart(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
        user = db.query(Users).filter(
            Users.email == current_user["sub"]
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cart_items = db.query(Cart).filter(
            Cart.user_id == user.id
        ).all()
        return cart_items

@cart_router.delete("/cart/{id}")
def delete_cart_item(
     id:int,
     db=Depends(get_db),
     current_user=Depends(get_current_user)
):
        user = db.query(Users).filter(
            Users.email == current_user["sub"]
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        cart_item = db.query(Cart).filter(Cart.id == id,
        Cart.user_id == user.id
        ).first()
        if not cart_item:
             raise HTTPException(
                  status_code=404,
                  detail="Cart item not found"
             )
        db.delete(cart_item)
        db.commit()
        return {
             "message": "Cart item deleted successfully"
             }
