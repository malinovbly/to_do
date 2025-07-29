# src/schemas/schemas.py
from pydantic import BaseModel, constr
from typing import Literal, Optional
from enum import Enum
from uuid import UUID


MIN_USERNAME_LENGTH = 5
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 256


class NewUser(BaseModel):
    name: constr(min_length=MIN_USERNAME_LENGTH)
    password: constr(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseModel):
    id: UUID
    name: str
    role: UserRole
    salt: str
    password: str


class LoginData(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskImportance(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class NewTask(BaseModel):
    name: str
    description: Optional[str] = None
    importance: TaskImportance = TaskImportance.LOW


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    importance: Optional[TaskImportance] = None
    is_completed: Optional[bool] = None


class Task(BaseModel):
    id: UUID
    name: str
    description: str
    importance: TaskImportance
    is_completed: bool


class Ok(BaseModel):
    success: Literal[True] = True
