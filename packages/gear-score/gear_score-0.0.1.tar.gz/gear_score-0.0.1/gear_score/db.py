import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from gear_score.config import settings

Base = declarative_base()
Engine = create_async_engine(settings.db_dsn, echo=False)


# Ensuring that all tables are created
async def ensure_tables_created():
    async with Engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

