# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 14:28
@Author   : shwezheng
@Software : PyCharm
"""

from enum import Enum


class CaseStatusEnum(str, Enum):
    DEBUG = "debug"  # 调试中
    TEMPORARILY_CLOSED = "temporarily_closed"  # 暂时关闭
    NORMAL_OPERATION = "normal_operation"  # 正常运作


class CaseTypeEnum(str, Enum):
    FUNCTIONAL_TEST = "functional_test"  # 功能测试
    PERFORMANCE_TEST = "performance_test"  # 性能测试
    SECURITY_TEST = "security_test"  # 安全测试
    OTHER = "other"  # 其他


class CaseExecStatus(int, Enum):
    success = 0
    fail = 1
    skip = 2
    error = 3


class CaseTagEnum(str, Enum):
    FUNCTIONAL_TEST = "functional_test"  # 功能测试
    PERFORMANCE_TEST = "performance_test"  # 性能测试
    SECURITY_TEST = "security_test"  # 安全测试
    OTHER = "other"  # 其他


class CasePriorityEnum(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class State(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class AssertType(str, Enum):
    """断言类型"""

    STATUS_CODE = "status_code"  # HTTP状态码
    HEADER = "header"  # 响应头
    COOKIE = "cookie"  # Cookie
    JSON = "json"  # JSON响应体
    TEXT = "text"  # 文本响应体
    RESPONSE_TIME = "response_time"  # 响应时间


class AssertOperator(str, Enum):
    """断言操作符"""

    EQUALS = "equals"  # 等于
    NOT_EQUALS = "not_equals"  # 不等于
    CONTAINS = "contains"  # 包含
    NOT_CONTAINS = "not_contains"  # 不包含
    GREATER_THAN = "greater_than"  # 大于
    LESS_THAN = "less_than"  # 小于
    GREATER_THAN_OR_EQUALS = "gte"  # 大于等于
    LESS_THAN_OR_EQUALS = "lte"  # 小于等于
    REGEX_MATCH = "regex_match"  # 正则匹配
    IS_NULL = "is_null"  # 为空
    IS_NOT_NULL = "is_not_null"  # 不为空
