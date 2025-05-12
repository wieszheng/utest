# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/12 21:55
@Author   : shwezheng
@Software : PyCharm
"""

import time
from typing import Dict, Any

import aiohttp

from app.models.case.test_case import TestCase


class TestExecutor:
    async def execute_test_case(self, test_case: TestCase):
        """
        执行测试用例
        :return:
        """
        start_time = time.time()
        try:
            headers = test_case.headers or {}
            data = test_case.body
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=test_case.method,
                    url=test_case.url,
                    headers=headers,
                    json=data,
                ) as response:
                    response_time = int((time.time() - start_time) * 1000)
                    response_body = (
                        await response.json()
                        if response.headers.get("content-type") == "application/json"
                        else None
                    )
                    status = "pass"
                    test_result = {
                        "test_case_id": test_case.uid,
                        "status": status,
                        "response_time": response_time,
                        "response_status_code": response.status,
                        "response_body": response_body,
                    }
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            test_result = {
                "test_case_id": test_case.uid,
                "status": "error",
                "response_time": response_time,
                "error_message": str(e),
            }

        return test_result

    async def _verify_response(
        self, response: aiohttp.ClientResponse, expected_response: Dict[str, Any] | None
    ) -> str:
        if not expected_response:
            return "passed"

        # 验证状态码
        if (
            "status_code" in expected_response
            and response.status != expected_response["status_code"]
        ):
            return "failed"

        # 验证响应体
        if "body" in expected_response:
            try:
                response_json = await response.json()
                for key, value in expected_response["body"].items():
                    if key not in response_json or response_json[key] != value:
                        return "failed"
            except ValueError:
                return "failed"

        return "passed"
