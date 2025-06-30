# src/config/settings.py
from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    ADMIN_PASSWORD: str

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"


settings = Settings()
