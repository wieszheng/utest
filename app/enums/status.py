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
