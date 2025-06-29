# src/main.py
from fastapi import FastAPI

from src.api import main_router
from src.database.database import Base, engine


global_tags = [
    {"name": "admin"},
    {"name": "task"},
    {"name": "user"}
]

app = FastAPI(openapi_tags=global_tags)
app.include_router(main_router)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
