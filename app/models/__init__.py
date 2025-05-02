# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/19 23:59
@Author   : shwezheng
@Software : PyCharm
"""

from pydantic.alias_generators import to_snake
from sqlalchemy import DateTime, CHAR, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from datetime import datetime, timezone
from uuid import uuid4
from app.database.db import async_engine


class TimestampMixin(AsyncAttrs, DeclarativeBase):
    """
    时间戳相关列
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        sort_order=9996,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        sort_order=9997,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True, sort_order=9998
    )


class DeleteMixin(AsyncAttrs, DeclarativeBase):
    """
    删除列
    """

    __abstract__ = True
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True, sort_order=9999
    )


class UidMixin(AsyncAttrs, DeclarativeBase):
    """
    uid列
    """

    __abstract__ = True
    uid: Mapped[str] = mapped_column(
        CHAR(64),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        index=True,
        sort_order=1,
    )


class UTestModel(UidMixin, TimestampMixin, DeleteMixin):
    """
    基础模型
    支持异步 ORM 操作 AsyncAttrs 可有可无
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{to_snake(cls.__name__)}"


async def create_table() -> None:
    """
    创建数据库表
    """
    async with async_engine.begin() as coon:
        await coon.run_sync(UTestModel.metadata.create_all)
