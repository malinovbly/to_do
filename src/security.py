# src/security.py
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta, timezone

from src.config.settings import settings


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
