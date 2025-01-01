import asyncio
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable
from typing import TypeVar, Generic
import logging

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.settings import Settings

DomainKey = TypeVar("DomainKey")
Domain = TypeVar("Domain")

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, DeclarativeBase, Generic[DomainKey, Domain]):
    __abstract__ = True

    @staticmethod
    def from_domain(domain: Domain):
        raise NotImplementedError("from_domain method is not implemented")

    def to_domain(self) -> Domain:
        raise NotImplementedError("to_domain method is not implemented")

    def update(self, domain: Domain):
        raise NotImplementedError("update method is not implemented")

    def primary_key(self) -> DomainKey:
        raise NotImplementedError("primary_key method is not implemented")


class SessionManager:
    """비동기 데이터베이스 클래스"""

    def __init__(self, settings: Settings):
        url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
        self._engine = create_async_engine(url)
        
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as e:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
            await self._session_factory.remove()

    async def connect(self):
        return await self._engine.connect()