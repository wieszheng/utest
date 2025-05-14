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
    error = 0
    success = 1
    skip = 2
    fail = 3


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


class AssertOperator(str, Enum):
    EQUALS = "equals"  # 等于
    NOT_EQUALS = "not_equals"  # 不等于
    CONTAINS = "contains"  # 包含
    NOT_CONTAINS = "not_contains"  # 不包含
    GREATER_THAN = "greater_than"  # 大于
    LESS_THAN = "less_than"  # 小于
    GREATER_EQUAL = "greater_equal"  # 大于等于
    LESS_EQUAL = "less_equal"  # 小于等于
    MATCHES = "matches"  # 正则匹配
    NOT_MATCHES = "not_matches"  # 正则不匹配
    IS_NULL = "is_null"  # 为空
    NOT_NULL = "not_null"  # 不为空
    IS_TRUE = "is_true"  # 为true
    IS_FALSE = "is_false"  # 为false
