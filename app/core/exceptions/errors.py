# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:34
@Author   : shwezheng
@Software : PyCharm
"""

from app.enums.code import ApiErrorCode


class ApiException(Exception):
    def __init__(
        self,
        api_error_code: ApiErrorCode = None,
        err_code: int = 0,
        err_code_des: str = "",
    ):
        if api_error_code:
            self.err_code = api_error_code.code
            self.err_code_des = err_code_des or api_error_code.msg
        else:
            self.err_code = err_code
            self.err_code_des = err_code_des


class ApiError(ApiException):
    def __init__(self, api_error_code: ApiErrorCode):
        super().__init__(api_error_code)


class TestExecutionError(Exception):
    """测试执行基础异常类"""

    pass


class HTTPRequestError(TestExecutionError):
    """HTTP请求异常"""

    pass


class AssertionError(TestExecutionError):
    """断言异常"""

    pass


class VariableNotFoundError(TestExecutionError):
    """变量未找到异常"""

    pass


class ExtractError(TestExecutionError):
    """提取值异常"""

    pass
