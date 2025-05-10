# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/27 23:02
@Author   : shwezheng
@Software : PyCharm
"""

from sqlalchemy import String, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.status import CaseStatusEnum, CasePriorityEnum
from app.models import UTestModel
from app.models.case.testcase_directory import Directory


class TestCase(UTestModel):
    """
    接口模型
    """

    title: Mapped[str] = mapped_column(String(64), nullable=False, comment="用例标题")

    url: Mapped[str] = mapped_column(String(500), comment="请求地址")
    method: Mapped[str] = mapped_column(String(10), comment="请求方法")
    headers: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="请求头")
    body: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="请求体")
    body_type: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="请求体类型:0 none 1 json 2 form 3 x-form"
    )
    tag: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="用例标签"
    )
    status: Mapped[CaseStatusEnum] = mapped_column(comment="用例状态")
    priority: Mapped[CasePriorityEnum] = mapped_column(comment="用例优先级")
    case_type: Mapped[int] = mapped_column(Integer, nullable=True, comment="用例类型")
    directory_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("directories.id"), nullable=True
    )
    directory: Mapped[Directory | None] = relationship(
        "Directory", back_populates="test_cases"
    )
