# src/api/user.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.security import create_jwt_token, authenticate_user
from src.schemas import NewUser, User, Token, LoginData
from src.utils import create_user_in_db


router = APIRouter()


@router.post(path="/user/register", tags=["user"], response_model=User)
def register(
        user: NewUser,
        db: Session = Depends(get_db)
):
    return create_user_in_db(db, user)


@router.post(path="/user/login", tags=["user"], response_model=Token)
def login(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    login_data = LoginData(name=data.username, password=data.password)
    user = authenticate_user(db, login_data)
    access_token = create_jwt_token(user.id)
    return Token(access_token=access_token, token_type="bearer")
