# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 14:18
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from sqlalchemy import String, Enum as SqlEnum, INT, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.test import State
from app.models import UTestModel


class TestPlan(UTestModel):
    project_id: Mapped[int] = mapped_column(INT, nullable=False)
    env_id: Mapped[str] = mapped_column(CHAR(64), nullable=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    priority: Mapped[str] = mapped_column(String(3), nullable=True)
    cron: Mapped[str] = mapped_column(String(24), nullable=False)
    test_case_ids: Mapped[List[str]] = mapped_column(String(64), nullable=True)

    receivers: Mapped[List[str]] = mapped_column(String(64), nullable=True)
    message_type: Mapped[str] = mapped_column(String(64), nullable=True)

    state: Mapped[State] = mapped_column(
        SqlEnum(State), nullable=True, default=State.NOT_STARTED
    )
