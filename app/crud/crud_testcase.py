# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/10 23:01
@Author   : shwezheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.case.test_case import TestCase, TestReport, TestResult, TestCaseAssert


class CRUDTestCase(BaseCRUD): ...


crud_testcase: CRUDTestCase = CRUDTestCase(TestCase)


class CRUDTestReport(BaseCRUD): ...


crud_test_report: CRUDTestReport = CRUDTestReport(TestReport)


class CRUDTestResult(BaseCRUD): ...


crud_test_result: CRUDTestResult = CRUDTestResult(TestResult)


class CRUDTestAsserts(BaseCRUD): ...


crud_test_asserts: CRUDTestAsserts = CRUDTestAsserts(TestCaseAssert)
