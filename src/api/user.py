# src/api/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.utils import create_user, login_user, get_current_user
from src.schemas.schemas import NewUser, User, Token, LoginData


router = APIRouter()


@router.post(path="/user/register", tags=["user"], response_model=User)
def register(
        user: NewUser,
        db: Session = Depends(get_db)
):
    return create_user(user, db)


@router.post(path="/user/login", tags=["user"], response_model=Token)
def login(
        data: LoginData,
        db: Session = Depends(get_db)
):
    return login_user(data, db)


@router.get("/me")
def get_profile(current_user=Depends(get_current_user)):
    return {"user_id": current_user.id}
