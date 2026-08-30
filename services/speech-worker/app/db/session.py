from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from sqlalchemy.pool import NullPool

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}"
    f"/{settings.database_name}"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)


async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
