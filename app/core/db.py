from contextlib import asynccontextmanager

from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from sqlmodel import SQLModel

from app.core.config import settings


class DatabaseSession:
    def __init__(self, url: str = str(settings.SQLALCHEMY_DATABASE_URI)):
        self.engine = create_async_engine(url, echo=True)
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
        )

    async def close(self):
        if self.engine is None:
            raise Exception("DatabaseSession engine is not initialized")

        await self.engine.dispose()

        self.engine = None
        self.sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("DatabaseSession engine is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.sessionmaker is None:
            raise Exception("DatabaseSession session is not initialized")

        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


db_session = DatabaseSession()


async def get_db_session():
    async with db_session.session() as session:
        yield session
