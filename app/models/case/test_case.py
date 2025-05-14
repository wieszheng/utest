# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/27 23:02
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime

from sqlalchemy import String, JSON, Integer, CHAR, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.test import (
    CaseStatusEnum,
    CasePriorityEnum,
    HTTPMethod,
    AssertOperator,
    CaseExecStatus,
)
from app.models import UTestModel


class TestCase(UTestModel):
    """
    接口模型
    """

    title: Mapped[str] = mapped_column(String(64), nullable=False, comment="用例标题")

    url: Mapped[str] = mapped_column(String(500), comment="请求地址")
    method: Mapped[HTTPMethod] = mapped_column(SQLEnum(HTTPMethod), comment="请求方法")
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
    directory_id: Mapped[str] = mapped_column(CHAR(64), comment="目录ID")


class TestCaseAssert(UTestModel):
    """
    接口断言模型
    """

    name: Mapped[str] = mapped_column(String(100))
    test_case_id: Mapped[str] = mapped_column(CHAR(64), comment="用例ID")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    assert_type: Mapped[AssertOperator] = mapped_column(
        SQLEnum(AssertOperator), comment="断言类型"
    )
    assert_actually: Mapped[str] = mapped_column(String(64), comment="断言实际值")
    assert_expected: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="断言期望值"
    )


class TestCaseStep(UTestModel):
    """
    接口步骤模型
    """

    name: Mapped[str] = mapped_column(String(100))
    test_case_id: Mapped[str] = mapped_column(CHAR(64), comment="用例ID")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    step_type: Mapped[int] = mapped_column(Integer, comment="步骤类型")
    step_id: Mapped[str] = mapped_column(CHAR(64), comment="步骤ID")


class TestResult(UTestModel):
    """
    接口结果模型
    """

    report_id: Mapped[str] = mapped_column(CHAR(64), comment="报告ID")
    test_case_id: Mapped[str] = mapped_column(CHAR(64), comment="用例ID")
    test_case_name: Mapped[str] = mapped_column(String(64), comment="用例名称")
    status: Mapped[CaseExecStatus] = mapped_column(
        SQLEnum(CaseExecStatus), comment="状态"
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="开始时间"
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, comment="结束时间"
    )
    cost: Mapped[str] = mapped_column(String(8), comment="耗时")

    test_Case_log: Mapped[str] = mapped_column(Text, comment="日志")

    status_code: Mapped[int] = mapped_column(Integer, comment="状态码")
    url: Mapped[str] = mapped_column(String(500), comment="请求地址")
    body: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="请求体")
    request_params: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="请求参数"
    )

    request_headers: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="请求头"
    )
    request_method: Mapped[HTTPMethod] = mapped_column(
        SQLEnum(HTTPMethod), comment="请求方法"
    )

    response: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="响应体")
    response_headers: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="响应头"
    )
    cookies: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="cookies")

    asserts: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="断言")


class TestReport(UTestModel):
    """
    接口报告模型
    """

    executor: Mapped[str] = mapped_column(String(64), comment="执行者")
    env_id: Mapped[str] = mapped_column(CHAR(64), comment="环境ID")
    cost: Mapped[str] = mapped_column(String(8), comment="耗时")
    plan_id: Mapped[str] = mapped_column(
        CHAR(64), index=True, nullable=True, comment="计划ID"
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="开始时间"
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, comment="结束时间"
    )
    success_count: Mapped[int] = mapped_column(Integer, comment="成功数")
    fail_count: Mapped[int] = mapped_column(Integer, comment="失败数")
    skip_count: Mapped[int] = mapped_column(Integer, comment="跳过数")
    error_count: Mapped[int] = mapped_column(Integer, comment="错误数")
    status: Mapped[str] = mapped_column(comment="状态")
