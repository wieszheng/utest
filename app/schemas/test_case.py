# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:05
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Dict, Any

from pydantic import BaseModel

from app.enums.status import CaseStatusEnum, CasePriorityEnum


class TestCaseCreate(BaseModel):
    title: str
    method: str
    url: str
    headers: Dict[str, str] | None = None
    body: Dict[str, Any] | None = None
    body_type: int | None = None
    tag: str | None = None
    status: CaseStatusEnum = CaseStatusEnum.DEBUG
    priority: CasePriorityEnum = CasePriorityEnum.P0
    case_type: int = 0
    directory_id: int
