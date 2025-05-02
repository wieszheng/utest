# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 14:18
@Author   : shwezheng
@Software : PyCharm
"""

from sqlalchemy import String, Enum as SqlEnum, INT
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.test import State
from app.models import UTestModel


class TestPlan(UTestModel):
    project_id: Mapped[int] = mapped_column(INT, nullable=False)
    environment: Mapped[str] = mapped_column(String(64), nullable=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    priority: Mapped[str] = mapped_column(String(3), nullable=True)
    cron: Mapped[str] = mapped_column(String(24), nullable=False)
    state: Mapped[State] = mapped_column(
        SqlEnum(State), nullable=True, default=State.NOT_STARTED
    )
