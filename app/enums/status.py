# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/4/17 21:31
@Author   : shwezheng
@Software : PyCharm
"""

from enum import Enum


class ErrorShowType(Enum):
    SILENT = 0
    WARN_MESSAGE = 1
    ERROR_MESSAGE = 2
    NOTIFICATION = 3
    REDIRECT = 9


class QrLevel(str, Enum):
    L = "L"
    M = "M"
    Q = "Q"
    H = "H"


class OrderEnum(str, Enum):
    ascent = "ascent"
    decline = "decline"


class OperationType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    QUERY = "query"
    LOGIN = "login"
    LOGOUT = "logout"
    OTHER = "other"


class ProjectRoleEnum(str, Enum):
    CREATOR = "creator"  # 创建人
    LEADER = "leader"  # 组长
    MEMBER = "member"  # 组员


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
