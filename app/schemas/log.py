#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:53
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field

from app.models.log import OperationType


class LogBase(BaseModel):
    user_id: str = Field(..., description="操作用户ID")
    operation_type: OperationType = Field(..., description="操作类型")
    title: str = Field(..., description="操作标题")
    description: str | None = Field(None, description="操作描述")
    tag: str | None = Field(None, description="操作标签")
    old_data: Dict[str, Any] | None = Field(None, description="旧数据")
    new_data: Dict[str, Any] | None = Field(None, description="新数据")
    diff_data: Dict[str, Any] | None = Field(None, description="数据差异")
    duration: float | None = Field(None, description="操作耗时(ms)")
    operate_time: datetime = Field(..., description="操作时间")


class LogCreate(LogBase):
    pass


class LogUpdate(BaseModel):
    description: str | None = None
    tag: str | None = None
    old_data: Dict[str, Any] | None = None
    new_data: Dict[str, Any] | None = None
    diff_data: Dict[str, Any] | None = None
    duration: float | None = None


class LogResponse(LogBase):
    uid: str

    class Config:
        from_attributes = True
