# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 14:18
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from sqlalchemy import String, Enum as SqlEnum, CHAR, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.test import State
from app.models import UTestModel


class TestPlan(UTestModel):
    name: Mapped[str] = mapped_column(String(64), comment="计划名称")
    project_id: Mapped[str] = mapped_column(CHAR(64), comment="项目ID")
    env_id: Mapped[str] = mapped_column(CHAR(64), nullable=True, comment="环境ID")
    priority: Mapped[str] = mapped_column(String(3), nullable=True, comment="优先级")

    cron: Mapped[str] = mapped_column(
        String(24), nullable=False, comment="计划执行时间"
    )
    test_case_ids: Mapped[List[int]] = mapped_column(
        JSON, nullable=True, comment="用例ID列表"
    )
    receivers: Mapped[List[str]] = mapped_column(
        JSON, nullable=True, comment="接收人列表"
    )
    message_type: Mapped[str] = mapped_column(String(64), nullable=True)

    state: Mapped[State] = mapped_column(
        SqlEnum(State),
        nullable=True,
        default=State.NOT_STARTED,
        comment="计划状态待执行、执行中、已完成、已取消",
    )
