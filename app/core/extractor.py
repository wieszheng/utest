# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/15 22:50
@Author   : shwezheng
@Software : PyCharm
"""

import re
from typing import Any, Dict, Optional

from app.core.exceptions.errors import VariableNotFoundError, ExtractError
from app.enums.test import AssertType


class Extractor:
    def __init__(self):
        self.variable_pattern = re.compile(r"\${([^}]+)}")

    def replace_variables(self, template: Any, variables: Dict[str, Any]) -> Any:
        """
        替换模板中的变量
        :param template: 包含变量的模板（可以是字符串、字典或列表）
        :param variables: 变量字典
        :return: 替换后的值
        """
        if isinstance(template, str):
            return self._replace_variables_in_string(template, variables)
        elif isinstance(template, dict):
            return {
                k: self.replace_variables(v, variables) for k, v in template.items()
            }
        elif isinstance(template, list):
            return [self.replace_variables(item, variables) for item in template]
        return template

    def _replace_variables_in_string(
        self, template: str, variables: Dict[str, Any]
    ) -> str:
        """
        替换字符串中的变量
        :param template: 包含变量的字符串
        :param variables: 变量字典
        :return: 替换后的字符串
        """

        def replace_var(match):
            var_name = match.group(1)
            if var_name not in variables:
                raise VariableNotFoundError(f"变量未找到: {var_name}")
            return str(variables[var_name])

        return self.variable_pattern.sub(replace_var, template)

    def extract_value(
        self,
        response: Dict[str, Any],
        assert_type: AssertType,
        extract_key: Optional[str] = None,
        json_path: Optional[str] = None,
    ) -> Any:
        """
        从响应中提取值
        :param response: HTTP响应字典
        :param assert_type: 断言类型
        :param extract_key: 提取键名（用于header、cookie等）
        :param json_path: JSONPath表达式
        :return: 提取的值
        """
        try:
            if assert_type == AssertType.STATUS_CODE:
                return response["status_code"]

            elif assert_type == AssertType.HEADER:
                if not extract_key:
                    raise ExtractError("提取header值需要指定extract_key")
                return response["headers"].get(extract_key)

            elif assert_type == AssertType.COOKIE:
                if not extract_key:
                    raise ExtractError("提取cookie值需要指定extract_key")
                return response["cookies"].get(extract_key)

            elif assert_type == AssertType.JSON:
                if not json_path:
                    raise ExtractError("提取JSON值需要指定json_path")
                return self._extract_json_value(response["body"], json_path)

            elif assert_type == AssertType.TEXT:
                if not isinstance(response["body"], str):
                    raise ExtractError("响应体不是文本格式")
                return response["body"]

            else:
                raise ExtractError(f"不支持的断言类型: {assert_type}")

        except Exception as e:
            if isinstance(e, ExtractError):
                raise
            raise ExtractError(f"提取值失败: {str(e)}")

    def _extract_json_value(self, body: Any, json_path: str) -> Any:
        """
        使用JSONPath提取JSON值
        :param body: JSON响应体
        :param json_path: JSONPath表达式
        :return: 提取的值
        """
        try:
            # 这里使用简单的点号分隔的路径，可以根据需要使用更复杂的JSONPath库
            if not isinstance(body, dict):
                raise ExtractError("响应体不是JSON格式")

            current = body
            for key in json_path.strip("$.").split("."):
                if isinstance(current, dict):
                    if key not in current:
                        raise ExtractError(f"JSON路径不存在: {key}")
                    current = current[key]
                else:
                    raise ExtractError(f"无法在非对象类型中查找键: {key}")

            return current

        except Exception as e:
            if isinstance(e, ExtractError):
                raise
            raise ExtractError(f"JSON提取失败: {str(e)}")


if __name__ == "__main__":
    extractor = Extractor()
    variables = {"name": "张三", "age": 25}
    template = "用户${name}的年龄是${age}"
    result = extractor.replace_variables(template, variables)
    print(result)
