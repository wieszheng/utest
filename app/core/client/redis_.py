# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/5 11:26
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Optional

from redis import asyncio as aioredis
from redis.asyncio.client import Redis

from config import settings


class RedisClient:
    def __init__(self):
        self.redis: Optional[Redis] = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            encoding=settings.REDIS_ENCODING,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            db=settings.REDIS_DB,
        )

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        if self.redis:
            return await self.redis.get(key)

    async def client(self) -> Redis:
        return self.redis


redis_client = RedisClient()
__all__ = ["redis_client"]
