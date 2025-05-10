# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:01
@Author   : shwezheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.case.test_case import TestCase


class CRUDTestCase(BaseCRUD): ...


crud_testcase: CRUDTestCase = CRUDTestCase(TestCase)
