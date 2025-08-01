# src/api/public.py
from fastapi import APIRouter, Request

from src.config.templates import templates


router = APIRouter()


@router.get(path='/', tags=["user"])
def get_index_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})
