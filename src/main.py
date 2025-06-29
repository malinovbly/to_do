# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path

from src.api import main_router
from src.database.database import Base, engine


GLOBAL_TAGS = [
    {"name": "admin"},
    {"name": "task"},
    {"name": "user"}
]
FAVICON_PATH = './static/favicon.ico'

app = FastAPI(openapi_tags=GLOBAL_TAGS)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(main_router)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")


Base.metadata.create_all(bind=engine)
