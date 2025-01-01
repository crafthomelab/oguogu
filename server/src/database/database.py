import asyncio
from contextlib import AbstractContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable
import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.settings import Settings
from src.database.entity import ChallengeEntity, ChallengeProofEntity


logger = logging.getLogger(__name__)


class SessionManager:
    """비동기 데이터베이스 클래스"""

    def __init__(self, settings: Settings):
        url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        self._engine = create_async_engine(url)
        
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )
    
    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._engine.begin() as conn:
            yield conn

    async def create_database(self) -> None:
        async with self.connect() as conn:
            await conn.run_sync(ChallengeEntity.metadata.create_all)
            await conn.run_sync(ChallengeProofEntity.metadata.create_all)

    async def drop_database(self) -> None:
        async with self.connect() as conn:
            await conn.run_sync(ChallengeEntity.metadata.drop_all)
            await conn.run_sync(ChallengeProofEntity.metadata.drop_all)


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
