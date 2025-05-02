# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:56
@Author   : shwezheng
@Software : PyCharm
"""

import sys

from typing import Annotated
from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings
from loguru import logger


def create_database_url(unittest: bool = False) -> URL:
    """
    创建数据库链接

    :param unittest: 是否用于单元测试
    :return:
    """
    url = URL.create(
        drivername=settings.MYSQL_PROTOCOL,
        username=settings.MYSQL_USERNAME,
        password=settings.MYSQL_PASSWORD,
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DATABASE
        if not unittest
        else f"{settings.MYSQL_DATABASE}_test",
        query={"charset": "utf8mb4"},
    )
    return url


def create_async_engine_and_session(
    url: str | URL,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
    创建数据库引擎和 Session

    :param url: create_database_url / str
    :return:
    """

    try:
        engine = create_async_engine(
            url,
            echo=settings.MYSQL_ECHO,
            future=True,
            pool_size=settings.MYSQL_POOL_SIZE,
            max_overflow=settings.MYSQL_MAX_OVERFLOW,
            pool_timeout=settings.MYSQL_POOL_TIMEOUT,
            pool_recycle=settings.MYSQL_POOL_RECYCLE,
            pool_pre_ping=True,
            pool_use_lifo=False,
        )
    except Exception as e:
        logger.error("❌ 数据库链接失败 {}", e)
        sys.exit()
    else:
        session = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )
        return engine, session


async def get_async_session():
    """
    获取数据库 Session
    """
    async with async_session_maker() as session:
        yield session


async_engine, async_session_maker = create_async_engine_and_session(
    create_database_url()
)
currentSession = Annotated[AsyncSession, Depends(get_async_session)]
