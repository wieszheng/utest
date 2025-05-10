# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/19 23:58
@Author   : shwezheng
@Software : PyCharm
"""

from fastapi import APIRouter

from app.api.v1.auth import users
from app.api.v1.testcase import test_plan
from app.api.v1.common import qrcode

api_router_v1 = APIRouter()
[
    api_router_v1.include_router(router, prefix=prefix, tags=[tag])
    for router, prefix, tag in [
        (users.router, "/system/users", "System users"),
        (test_plan.router, "/testplan", "Testplan"),
        (qrcode.router, "/qrcode", "Qrcode"),
    ]
]
