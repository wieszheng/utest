# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 21:49
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from sqlalchemy import String, Text, ForeignKey, CHAR, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.status import ProjectRoleEnum
from app.models import UTestModel
from app.models.user import User


class Project(UTestModel):
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
    owner_id: Mapped[str] = mapped_column(
        CHAR(64), ForeignKey("users.uid"), comment="项目拥有者ID"
    )
    owner: Mapped[User] = relationship("User", back_populates="projects")
    roles: Mapped[List["ProjectRole"]] = relationship(
        "ProjectRole", back_populates="project"
    )


class ProjectRole(UTestModel):
    """
    项目角色模型
    """

    role: Mapped[ProjectRoleEnum] = mapped_column(Enum(ProjectRoleEnum))
    project_id: Mapped[str] = mapped_column(
        CHAR(64), ForeignKey("projects.uid"), comment="项目ID"
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(64), ForeignKey("users.uid"), comment="用户ID"
    )
    project: Mapped[Project] = relationship("Project", back_populates="roles")
    user: Mapped[User] = relationship("User", back_populates="project_roles")
