# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/12 21:55
@Author   : shwezheng
@Software : PyCharm
"""

import asyncio
import json

import time
from typing import Dict, Any
from datetime import datetime
import aiohttp

from app.core.exceptions.errors import ApiError
from app.core.extractor import Extractor
from app.core.handler.assertion import AssertionHandler
from app.crud.crud_testcase import (
    crud_testcase,
    crud_test_report,
    crud_test_result,
    crud_test_asserts,
)
from app.enums.code import ApiErrorCode
from app.enums.test import CaseExecStatus, HTTPMethod
from app.models.case.test_case import TestCase


class TestExecutor:
    def __init__(self):
        self.assertion_handler = AssertionHandler()
        self.extractor = Extractor()

    @staticmethod
    async def run_single_case(report_id: str, test_case_id: str):
        """
        执行测试用例
        :return:
        """
        result = {}
        start_time = datetime.now()
        test_case = await crud_testcase.get(uid=test_case_id)
        if not test_case:
            raise ApiError(ApiErrorCode.TEST_CASE_NOT_FOUND)
        try:
            headers = test_case.headers or {}
            body = test_case.body
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=test_case.method,
                    url=test_case.url,
                    headers=headers,
                    json=body,
                ) as response:
                    end_time = datetime.now()
                    cost = "{}s".format((end_time - start_time).seconds)
                    response_body = (
                        await response.json()
                        if response.headers.get("content-type") == "application/json"
                        else None
                    )

                    result = {
                        "test_case_id": test_case.uid,
                        "test_case_name": test_case.title,
                        "url": test_case.url,
                        "body": body,
                        "status_code": response.status,
                        "request_method": test_case.method,
                        "request_headers": headers,
                        "response": response_body,
                        # "response_headers ": response.headers,
                        "cookies": response.cookies,
                        "cost": cost,
                        "status": CaseExecStatus.success,
                        "test_case_log": "",
                        "start_at": start_time,
                        "end_at": end_time,
                        "report_id": report_id,
                    }
                    await crud_test_result.create(obj=result)
                    return result
        except Exception as e:
            cost = "{}s".format((datetime.now() - start_time).seconds)
            print(e)

        return result

    async def verify_response(
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

    async def run_multiple_case(self, executor: str, test_cases: list[str]):
        """
        执行多个测试用例
        :param executor:
        :param test_cases: e45777d2-2e6a-484c-8ed7-8ba2564737b8
        :return:
        """
        st = time.perf_counter()
        report = await crud_test_report.create(
            obj={"executor": executor, "env_id": executor}
        )
        await crud_test_report.update(uid=report.uid, obj_new={"status": 1})

        res = await asyncio.gather(
            *[
                TestExecutor.run_single_case(report.uid, test_case)
                for test_case in test_cases
            ]
        )
        success, fail, skip, error = 0, 0, 0, 0
        for i in res:
            if i["status"] == 0:
                success += 1
            elif i["status"] == 1:
                fail += 1
            elif i["status"] == 2:
                skip += 1
            elif i["status"] == 3:
                error += 1

        cost = time.perf_counter() - st
        cost = "%.2f" % cost
        report = await crud_test_report.update(
            uid=report.uid,
            obj_new={
                "status": 2,
                "success_count": success,
                "fail_count": fail,
                "skip_count": skip,
                "error_count": error,
                "cost": cost,
                "end_at": datetime.now(),
            },
        )
        return report

    def _preprocess_request(self, test_case: TestCase) -> Dict[str, Any]:
        """请求预处理"""
        # 合并测试用例变量和传入变量
        variables = {**(test_case.variables or {}), **self.variables}

        # 替换URL和请求参数中的变量
        url = self.extractor.replace_variables(test_case.request_url, variables)
        headers = (
            self.extractor.replace_variables(test_case.request_headers, variables)
            if test_case.request_headers
            else {}
        )
        body = (
            self.extractor.replace_variables(test_case.request_body, variables)
            if test_case.request_body
            else None
        )

        return {"url": url, "headers": headers, "body": body}

    async def run(
        self,
        env_id: str,
        test_case_id: str,
        params_pool: dict = None,
        request_param: dict = None,
    ):
        case_params = params_pool
        if case_params is None:
            case_params = dict()

        req_params = request_param
        if req_params is None:
            req_params = dict()

        # 加载全局变量
        glb = {"name": "global"}
        case_params.update(glb)
        request_param.update(glb)

        response_info = dict()

        try:
            test_case: TestCase = await crud_testcase.get(uid=test_case_id)

            # 获取断言
            asserts_list = await crud_test_asserts.get_multiple(
                test_case_id=test_case.uid
            )

            # 替换请求参数
            request_data = self._preprocess_request(test_case)

            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=test_case.method,
                    url=request_data["url"],
                    headers=request_data["headers"],
                    json_data=request_data["body"]
                    if test_case.method
                    in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]
                    else None,
                    data=request_data["body"]
                    if test_case.method == HTTPMethod.GET
                    else None,
                ) as response:
                    response_status = response.status
                    response_headers = dict(response.headers)
                    response_cookies = {
                        cookie.key: cookie.value for cookie in response.cookies.values()
                    }

                    try:
                        response_body = await response.json()
                        response_body_type = "json"
                    except json.JSONDecodeError:
                        response_body = await response.text()
                        response_body_type = "text"

                    response_info.update(
                        {
                            "status": response_status,
                            "headers": response_headers,
                            "cookies": response_cookies,
                            "body": response_body,
                            "body_type": response_body_type,
                        }
                    )

            response_info["test_case_id"] = test_case.uid
            response_info["case_name"] = test_case.title
            response_info["request_method"] = test_case.method
            response_info["url"] = request_data["url"]
            response_info["request_data"] = request_data["body"]

            for assertion in asserts_list:
                actual_value = self.extractor.extract_value(
                    response={
                        "body": response_info["body"],
                        "body_type": "json"
                        if isinstance(response_info["body"], dict)
                        else "text",
                        "headers": response_info["headers"],
                        "cookies": response_info["cookies"],
                        "status": response_info["status_code"],
                    },
                    assert_type=assertion.assert_type,
                    extract_key=assertion.extract_key,
                    json_path=assertion.json_path,
                )

                # 执行断言
                success = self.assertion_handler.assert_value(
                    actual_value=actual_value,
                    operator=assertion.operator,
                    expected_value=assertion.expected_value.get("value")
                    if assertion.expected_value
                    else None,
                )
                if not success:
                    response_info["status"] = "failed"

        except Exception as e:
            print(e)
