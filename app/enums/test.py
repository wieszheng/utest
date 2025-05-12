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
