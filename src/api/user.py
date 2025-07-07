# src/api/user.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from src.database.database import get_db
from src.config.settings import settings
from src.security import oauth2_scheme
from src.utils import create_user, authenticate_user, create_jwt_token
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
        token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
