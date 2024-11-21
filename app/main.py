from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.routes import utils
from app.routes.graphql import graphql_app
from app.core.db import get_session, engine, create_db_and_tables
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if engine is not None:
        await get_session().close()


app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.on_event("startup")
async def startup():
    await create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(graphql_app, prefix="/graphql", tags=["utils"])
app.include_router(api_router, prefix="/api", tags=["api"])
