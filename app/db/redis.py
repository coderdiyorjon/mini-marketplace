import redis.asyncio as redis

from app.core.config import settings


class RedisCache:
    client: redis.Redis | None = None

    @classmethod
    async def connect(cls):
        cls.client = redis.from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )

    @classmethod
    async def disconect(cls):
        if cls.client:
            await cls.client.close()

    @classmethod
    async def get(cls, key: str):
        if cls.client is None:
            raise Exception("Redis is not connected")
        return await cls.client.get(key)

    @classmethod
    async def set(cls, key: str, value: str, ex: int):
        if cls.client is None:
            raise Exception("Redis is not connected")
        return await cls.client.set(key, value, ex=ex)


# 89b8108b-71b9-4697-a7e9-82e92f9c7327
