# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 21:49
@Author   : shwezheng
@Software : PyCharm
"""

from sqlalchemy import String, Text, CHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.status import ProjectRoleEnum
from app.models import UTestModel


class Projects(UTestModel):
    """
    项目模型
    """

    title: Mapped[str] = mapped_column(String(64), nullable=False, comment="项目名称")
    private: Mapped[bool] = mapped_column(default=False, comment="项目私密性")
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="项目描述"
    )
    avatar: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="项目头像"
    )
    notice: Mapped[str | None] = mapped_column(Text, nullable=True, comment="项目公告")
    owner: Mapped[str] = mapped_column(CHAR(64), comment="项目拥有者ID")


class ProjectMembers(UTestModel):
    """
    项目成员模型
    """

    role: Mapped[ProjectRoleEnum] = mapped_column(
        Enum(ProjectRoleEnum), default=ProjectRoleEnum.MEMBER, comment="项目成员角色"
    )
    project_id: Mapped[str] = mapped_column(CHAR(64), comment="项目ID")
    user_id: Mapped[str] = mapped_column(CHAR(64), comment="用户ID")
