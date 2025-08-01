# src/api/__init__.py
from fastapi import APIRouter

from src.api.admin import router as admin_router
from src.api.public import router as public_router
from src.api.task import router as task_router
from src.api.user import router as user_router


main_router = APIRouter()

main_router.include_router(admin_router)
main_router.include_router(public_router)
main_router.include_router(task_router)
main_router.include_router(user_router)
