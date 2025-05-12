# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/27 23:16
@Author   : shwezheng
@Software : PyCharm
"""

from sqlalchemy import String, Text, Integer, CHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.models import UTestModel


class Directory(UTestModel):
    """
    目录模型
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(CHAR(64))
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
