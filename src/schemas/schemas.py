# src/schemas/schemas.py
import pydantic
from pydantic import BaseModel
from typing import Literal
from enum import Enum
from uuid import UUID


class NewUser(BaseModel):
    name: pydantic.constr(min_length=3)


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseModel):
    id: UUID
    name: str
    role: UserRole
    api_key: UUID


class TaskImportance(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(BaseModel):
    id: UUID
    name: str
    description: str
    importance: TaskImportance


class Ok(BaseModel):
    success: Literal[True] = True
