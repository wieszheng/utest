# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/12 19:57
@Author   : shwezheng
@Software : PyCharm
"""

from contextlib import asynccontextmanager
import redis.asyncio as aioredis
from redis import Redis

from config import settings

pool = aioredis.ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=settings.REDIS_MAX_CONNECTIONS,
    encoding=settings.REDIS_ENCODING,
    decode_responses=settings.REDIS_DECODE_RESPONSES,
    db=settings.REDIS_DB,
)


@asynccontextmanager
async def create_redis_client() -> Redis:
    client = aioredis.Redis.from_pool(pool)
    try:
        yield client
    finally:
        await client.close


async def get_redis_db() -> Redis:
    async with create_redis_client() as db:
        yield db
