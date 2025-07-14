# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
from pathlib import Path

from src import models
from src.api import main_router
from src.database.database import Base, engine
from src.database.init_data import run_db_creation_sync


GLOBAL_TAGS = [
    {"name": "admin"},
    {"name": "task"},
    {"name": "user"}
]
FAVICON_PATH = './static/favicon.ico'


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(run_db_creation_sync)
    yield


app = FastAPI(openapi_tags=GLOBAL_TAGS, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(main_router)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")


Base.metadata.create_all(bind=engine)
