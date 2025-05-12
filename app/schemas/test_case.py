# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:05
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Dict, Any

from pydantic import BaseModel, field_validator

from app.enums.test import CaseStatusEnum, CasePriorityEnum, HTTPMethod
from app.schemas.common import UTestModel


class TestCaseBase(BaseModel):
    title: str
    method: HTTPMethod
    url: str
    headers: Dict[str, str] | None = None
    body: Dict[str, Any] | None = None
    body_type: int | None = None
    tag: str | None = None
    status: CaseStatusEnum = CaseStatusEnum.DEBUG
    priority: CasePriorityEnum = CasePriorityEnum.P0

    @field_validator("url")
    def validate_url(cls, v):
        if v is not None and not v.startswith(("http://", "https://")):
            raise ValueError("URL 必须以 http:// 或 https:// 开头")
        return v


class TestCaseCreate(TestCaseBase):
    case_type: int = 0
    directory_id: int


class TestCaseDetail(TestCaseCreate, UTestModel): ...
