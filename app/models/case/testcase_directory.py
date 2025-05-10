# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/27 23:16
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from sqlalchemy import String, Text, Integer, ForeignKey, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import UTestModel
from app.models.case.test_case import TestCase
from app.models.project import Project


class Directory(UTestModel):
    """
    目录模型
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(CHAR(64), ForeignKey("projects.uid"))
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("directories.id"), nullable=True
    )

    project: Mapped[Project] = relationship("Project", back_populates="directories")
    parent: Mapped["Directory" | None] = relationship(
        "Directory", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["Directory"]] = relationship(
        "Directory", back_populates="parent"
    )
    test_cases: Mapped[List[TestCase]] = relationship(
        "TestCase", back_populates="directory"
    )
