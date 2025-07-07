# src/api/user.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.security import create_jwt_token
from src.utils import create_user, authenticate_user, get_current_user
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
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    login_data = LoginData(name=data.username, password=data.password)
    user = authenticate_user(login_data, db)
    access_token = create_jwt_token(user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.get(path="/me")
def get_profile(
        current_user: User = Depends(get_current_user)
):
    return {
        "current_user": current_user
    }
