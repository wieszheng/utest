# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:03
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from fastapi import APIRouter, Depends

from app.api.v1 import Authentication
from app.core.exceptions.errors import ApiError
from app.core.executor import TestExecutor
from app.crud.crud_testcase import crud_testcase
from app.enums.code import ApiErrorCode
from app.schemas.common import ResponseModel
from app.schemas.test_case import TestCaseCreate, TestCaseBase, TestCaseDetail

router = APIRouter()
executor = TestExecutor()


@router.post("/", summary="创建接口用例", response_model=ResponseModel[TestCaseBase])
async def create_interface_case(
    testcase: TestCaseCreate, user=Depends(Authentication())
) -> ResponseModel[TestCaseBase]:
    """
    创建接口用例
    """
    if await crud_testcase.exists(
        title=testcase.title, directory_id=testcase.directory_id
    ):
        raise ApiError(ApiErrorCode.TEST_CASE_ALREADY_EXISTS)

    case = await crud_testcase.create(
        obj={**testcase.model_dump(), "create_user": user.uid}
    )
    return ResponseModel(data=case)


@router.get(
    "/", summary="获取接口用例列表", response_model=ResponseModel[List[TestCaseDetail]]
)
async def read_interface_cases(
    limit: int = 100, offset: int = 0
) -> ResponseModel[List[TestCaseDetail]]:
    """
    获取接口用例列表
    """
    cases = await crud_testcase.get_multiple(limit=limit, offset=offset)
    return ResponseModel(data=cases)


@router.get(
    "/{case_id}",
    summary="获取接口用例详情",
    response_model=ResponseModel[TestCaseDetail],
)
async def read_interface_case(case_id: str) -> ResponseModel[TestCaseDetail]:
    """
    获取接口用例详情
    """
    case = await crud_testcase.get(uid=case_id)
    return ResponseModel(data=case)


@router.post("/{case_id}/run", summary="运行接口用例", response_model=ResponseModel)
async def run_interface_case(case_id: str) -> ResponseModel:
    """
    运行单接口用例
    """
    res = await executor.run_single_case(case_id)

    return ResponseModel(data=res)


@router.post("/run_multiple", summary="运行所有接口用例")
async def run_all_interface_case(case_id: List[str], user=Depends(Authentication())):
    """
    运行所有接口用例
    """
    res = await executor.run_multiple_case(user.uid, case_id)

    return ResponseModel(data=res)
