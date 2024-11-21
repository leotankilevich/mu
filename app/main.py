import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.routes import utils
from app.core.db import db_session
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if db_session.engine is not None:
        await db_session.close()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api", tags=["api"])
