# src/hash_password.py
from fastapi import HTTPException
from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode
from src.schemas.schemas import MAX_PASSWORD_LENGTH
from os import urandom

from src.models.user import UserModel


SALT_LENGTH = 10


class HashPassword:
    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
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

    @staticmethod
    def verify(db_user: UserModel, raw_password: str) -> bool:
        decoded_password = b64decode(db_user.password)
        decoded_salt = b64decode(db_user.salt)
        real_key = decoded_password
        salt = decoded_salt

        test_key = pbkdf2_hmac(
            hash_name='sha256',
            password=raw_password.encode(),
            salt=salt,
            iterations=100_000
        )

        return test_key == real_key
