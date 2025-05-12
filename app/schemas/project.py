# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/11 21:04
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from pydantic import BaseModel

from app.schemas.user import User


class ProjectBase(BaseModel):
    uid: str
    title: str
    description: str | None = None
    avatar: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectRoleBase(BaseModel):
    uid: str
    project_id: str
    user_id: str


class Project(ProjectBase):
    user: List[User] = []
    roles: List[ProjectRoleBase] = []
