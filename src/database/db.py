from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import settings
from .base import BaseSQLModel

engine = create_async_engine(settings.database_uri, echo=True, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

SQLModel = declarative_base(cls=BaseSQLModel)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)  # TODO Not for production, just for convenience
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
