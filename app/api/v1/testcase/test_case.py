# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:03
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.crud.crud_testcase import crud_testcase
from app.schemas.test_case import TestCaseCreate
from app.schemas.user import CurrentUser

router = APIRouter()


def get_current_user(): ...


@router.post("/", summary="创建接口用例")
async def create_interface_case(
    testcase: TestCaseCreate, user: Annotated[CurrentUser, Depends(get_current_user)]
):
    """
    创建接口用例
    """

    await crud_testcase.create(obj=testcase)
