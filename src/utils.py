# src/utils.py
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from uuid import uuid4
from os import urandom
from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from src.config.settings import settings
from src.models.user import UserModel
from src.security import security
from src.database.database import get_db
from src.schemas.schemas import NewUser, UserRole, LoginData, Token, MAX_PASSWORD_LENGTH


SALT_LENGTH = 10


# user
def create_user(user: NewUser, db: Session):
    try:
        check_username(user, db)

        db_password, db_salt = hash_password(user.password)

        db_user = UserModel(
            id=uuid4(),
            name=user.name,
            role=UserRole.USER,
            password=db_password,
            salt=db_salt
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def check_username(user: NewUser, db: Session):
    if len(user.name) < 5:
        raise HTTPException(status_code=400, detail="Username must be longer than 4")

    db_username = db.execute(
        select(UserModel).filter_by(name=user.name)
    ).scalar_one_or_none()

    if db_username is not None:
        raise HTTPException(status_code=409, detail="Username already exists")


def login_user(data: LoginData, db: Session):
    db_user = get_user_by_name(data.username, db)
    if not verify_password(db_user, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(db_user.id)
    return Token(access_token=token, token_type="bearer")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        return get_user_by_id(user_id, db)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_by_name(name: str, db: Session):
    db_user = db.execute(
        select(UserModel).filter_by(name=name)
    ).scalar_one_or_none()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


def get_user_by_id(user_id: str, db: Session):
    db_user = db.execute(
        select(UserModel).filter_by(id=user_id)
    ).scalar_one_or_none()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return db_user


# admin
def user_is_admin(api_key: str, db: Session):
    ...


def delete_user_by_id(user_id: str, db: Session):
    ...


# task


# password
def hash_password(password: str):
    if len(password) > MAX_PASSWORD_LENGTH:
        raise HTTPException(status_code=400, detail="Password too long. Maximum allowed length is 256 characters")

    salt = urandom(SALT_LENGTH)
    key = pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100_000
    )

    encoded_key = b64encode(key).decode("utf-8")
    encoded_salt = b64encode(salt).decode("utf-8")

    return encoded_key, encoded_salt


def verify_password(db_user: UserModel, raw_password: str):
    decoded = decode_password(db_user.password, db_user.salt)
    real_key = decoded[0]
    salt = decoded[1]

    test_key = pbkdf2_hmac(
        hash_name='sha256',
        password=raw_password.encode(),
        salt=salt,
        iterations=100_000
    )

    return test_key == real_key


def decode_password(password: str, salt: str):
    decoded_password = b64decode(password)
    decoded_salt = b64decode(salt)
    return decoded_password, decoded_salt


# JWT
def create_jwt_token(user_id: str) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token
