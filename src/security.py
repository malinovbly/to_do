# src/security.py
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from src.config.settings import settings
from src.database.database import get_db
from src.schemas.schemas import User, LoginData
from src.models.user import UserModel
from src.utils import get_user
from src.hash_password import HashPassword


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
) -> User:
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
    return User(
        id=db_user.id,
        name=db_user.name,
        role=db_user.role,
        password=db_user.password,
        salt=db_user.salt
    )


def authenticate_user(data: LoginData, db: Session) -> UserModel:
    db_user = get_user(db, name=data.name)
    if (db_user is None) or (not HashPassword.verify(db_user, data.password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user
