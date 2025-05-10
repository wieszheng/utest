#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:53
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime

from sqlalchemy import CHAR, DateTime, String, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.status import OperationType
from app.models import UTestModel


class Log(UTestModel):
    """
    系统操作日志模型
    """

    user_id: Mapped[str] = mapped_column(
        CHAR(64), nullable=False, index=True, comment="操作用户ID"
    )
    operation_type: Mapped[OperationType] = mapped_column(
        SQLEnum(OperationType), nullable=False, index=True, comment="操作类型"
    )
    title: Mapped[str] = mapped_column(String(128), nullable=False, comment="操作标题")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="操作描述"
    )
    tag: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True, comment="操作标签"
    )

    old_data: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="旧数据")
    new_data: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="新数据")
    diff_data: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="数据差异"
    )
    duration: Mapped[float | None] = mapped_column(
        nullable=True, comment="操作耗时(ms)"
    )
    operate_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="操作时间"
    )
