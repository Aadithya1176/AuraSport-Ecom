from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

try:
    from ..auth import create_access_token, get_current_user, hash_password, verify_password
    from ..database import get_db
    from ..models import Users
    from ..schemas import UserCreate, UserLogin, UserResponse
except ImportError:
    from auth import create_access_token, get_current_user, hash_password, verify_password
    from database import get_db
    from models import Users
    from schemas import UserCreate, UserLogin, UserResponse
from typing import List

user_router = APIRouter()

@user_router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db=Depends(get_db)
):
    new_user = Users(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )
    return new_user

@user_router.post("/login")
def login_user(
    user: UserLogin,
    db=Depends(get_db)
):
    existing_user = (
        db.query(Users)
        .filter(Users.email == user.email)
        .first()
    )

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = create_access_token(
        {
            "sub" : existing_user.email
        }
    )
    return {
        "access token" : token
    }

@user_router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "email": current_user.get("sub")
    }

@user_router.get("/users", response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    users = db.query(Users).all()
    return users