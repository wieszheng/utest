# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/15 22:51
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Any

from app.enums.test import AssertOperator


class AssertionHandler:
    def assert_value(
        self, actual_value: Any, operator: AssertOperator, expected_value: Any
    ) -> bool:
        """
        执行断言
        :param actual_value: 实际值
        :param operator: 断言操作符
        :param expected_value: 期望值
        :return: 断言是否成功
        """
        try:
            if operator == AssertOperator.EQUALS:
                return self._assert_equals(actual_value, expected_value)
            elif operator == AssertOperator.NOT_EQUALS:
                return self._assert_not_equals(actual_value, expected_value)
            elif operator == AssertOperator.CONTAINS:
                return self._assert_contains(actual_value, expected_value)
            elif operator == AssertOperator.NOT_CONTAINS:
                return self._assert_not_contains(actual_value, expected_value)
            elif operator == AssertOperator.GREATER_THAN:
                return self._assert_greater_than(actual_value, expected_value)
            elif operator == AssertOperator.LESS_THAN:
                return self._assert_less_than(actual_value, expected_value)
            elif operator == AssertOperator.GREATER_THAN_OR_EQUALS:
                return self._assert_greater_than_or_equals(actual_value, expected_value)
            elif operator == AssertOperator.LESS_THAN_OR_EQUALS:
                return self._assert_less_than_or_equals(actual_value, expected_value)
            elif operator == AssertOperator.REGEX_MATCH:
                return self._assert_regex_match(actual_value, expected_value)
            elif operator == AssertOperator.IS_NULL:
                return self._assert_is_null(actual_value)
            elif operator == AssertOperator.IS_NOT_NULL:
                return self._assert_is_not_null(actual_value)
            else:
                raise AssertionError(f"不支持的断言操作符: {operator}")

        except Exception as e:
            if isinstance(e, AssertionError):
                raise
            raise AssertionError(f"断言执行失败: {str(e)}")

    def _assert_equals(self, actual: Any, expected: Any) -> bool:
        """断言相等"""
        return actual == expected

    def _assert_not_equals(self, actual: Any, expected: Any) -> bool:
        """断言不相等"""
        return actual != expected

    def _assert_contains(self, actual: Any, expected: Any) -> bool:
        """断言包含"""
        if isinstance(actual, (str, list, tuple, dict)):
            return expected in actual
        raise AssertionError("contains操作符只能用于字符串、列表、元组或字典类型")

    def _assert_not_contains(self, actual: Any, expected: Any) -> bool:
        """断言不包含"""
        if isinstance(actual, (str, list, tuple, dict)):
            return expected not in actual
        raise AssertionError("not_contains操作符只能用于字符串、列表、元组或字典类型")

    def _assert_greater_than(self, actual: Any, expected: Any) -> bool:
        """断言大于"""
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return actual > expected
        raise AssertionError("greater_than操作符只能用于数字类型")

    def _assert_less_than(self, actual: Any, expected: Any) -> bool:
        """断言小于"""
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return actual < expected
        raise AssertionError("less_than操作符只能用于数字类型")

    def _assert_greater_than_or_equals(self, actual: Any, expected: Any) -> bool:
        """断言大于等于"""
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return actual >= expected
        raise AssertionError("greater_than_or_equals操作符只能用于数字类型")

    def _assert_less_than_or_equals(self, actual: Any, expected: Any) -> bool:
        """断言小于等于"""
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return actual <= expected
        raise AssertionError("less_than_or_equals操作符只能用于数字类型")

    def _assert_regex_match(self, actual: Any, expected: Any) -> bool:
        """断言正则匹配"""
        if isinstance(actual, str) and isinstance(expected, str):
            import re

            return bool(re.search(expected, actual))
        raise AssertionError("regex_match操作符只能用于字符串类型")

    def _assert_is_null(self, actual: Any) -> bool:
        """断言为空"""
        return actual is None

    def _assert_is_not_null(self, actual: Any) -> bool:
        """断言不为空"""
        return actual is not None


if __name__ == "__main__":
    assert_handler = AssertionHandler()
    # 包含断言
    success = assert_handler.assert_value(
        "Hello World", AssertOperator.CONTAINS, "World"
    )
    print(success)
    # 数值比较
    success = assert_handler.assert_value(100, AssertOperator.GREATER_THAN, 50)
    print(success)
    # 正则匹配
    success = assert_handler.assert_value(
        "test@example.com", AssertOperator.REGEX_MATCH, r"^[\w\.-]+@[\w\.-]+\.\w+$"
    )
    print(success)
