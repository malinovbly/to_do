# src/security.py
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from src.database.database import get_db
from src.config.settings import settings
from src.hash_password import HashPassword
from src.models import UserModel
from src.schemas import LoginData
from src.utils import get_user


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


# JWT
def create_jwt_token(user_id: str) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


# auth
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=400,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise credentials_exception
    return db_user


def authenticate_user(db: Session, data: LoginData) -> UserModel:
    db_user = get_user(db, name=data.name)
    if (db_user is None) or (not HashPassword.verify(db_user, data.password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user
