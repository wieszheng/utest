# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 14:28
@Author   : shwezheng
@Software : PyCharm
"""

from enum import Enum


class State(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    FINISHED = 2
