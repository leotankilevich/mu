from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routes import utils
from app.routes.graphql import graphql_app
from app.core.db import get_session, engine, create_db_and_tables, drop_db_and_tables
from app.core.config import settings

api_router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    if engine is not None:
        await get_session().close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(utils.router, prefix="/utils", tags=["utils"])
app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])
