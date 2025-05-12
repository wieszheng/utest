# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/11 20:58
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from fastapi import APIRouter

from app.crud.crud_project import crud_project
from app.schemas.common import ResponseModel
from app.schemas.project import Project

router = APIRouter()


@router.get("/", response_model=ResponseModel[List[Project]])
async def get_projects():
    """
    获取项目列表
    """
    project_list: List[Project] = await crud_project.get_multiple()
    return ResponseModel(data=project_list, message="获取项目列表成功")
