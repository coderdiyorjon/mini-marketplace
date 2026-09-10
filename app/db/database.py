from typing import Optional
import asyncpg
from app.core.config import settings

class Database:
    pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls):
        cls.pool = await asyncpg.create_pool(settings.DATABASE_URL)

    @classmethod
    async def disconnect(cls):
        if cls.pool is not None:
            await cls.pool.close()

    @classmethod
    async def fetch(cls, query: str, *args):
        if cls.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    @classmethod
    async def execute(cls, query: str, *args):
        if cls.pool is None:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            return await connection.execute(query, *args)