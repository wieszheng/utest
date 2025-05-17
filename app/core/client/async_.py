# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/15 21:46
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Optional, Dict, Any, Union
import aiohttp
import json

from app.enums.test import HTTPMethod


class HTTPClient:
    def __init__(self, timeout: int = 30):
        """
        初始化HTTP客户端
        :param timeout: 请求超时时间（秒）
        """
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self._session:
            await self._session.close()
            self._session = None

    async def _ensure_session(self):
        """确保session存在"""
        if not self._session:
            self._session = aiohttp.ClientSession(timeout=self.timeout)

    async def request(
        self,
        method: Union[str, HTTPMethod],
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        allow_redirects: bool = True,
        verify_ssl: bool = True,
    ) -> Dict[str, Any]:
        """
        发送HTTP请求
        :param method: 请求方法
        :param url: 请求URL
        :param headers: 请求头
        :param params: URL参数
        :param json_data: JSON请求体
        :param data: 表单数据
        :param cookies: Cookie
        :param timeout: 超时时间（秒）
        :param allow_redirects: 是否允许重定向
        :param verify_ssl: 是否验证SSL证书
        :return: 响应数据字典
        """
        await self._ensure_session()

        if isinstance(method, HTTPMethod):
            method = method.value

        try:
            async with self._session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                cookies=cookies,
                timeout=timeout or self.timeout,
                allow_redirects=allow_redirects,
                ssl=verify_ssl,
            ) as response:
                # 获取响应头
                headers = dict(response.headers)

                # 获取响应体
                try:
                    body = await response.json()
                except json.JSONDecodeError:
                    body = await response.text()

                # 获取cookies
                cookies = {cookie.key: cookie.value for cookie in response.cookies}

                return {
                    "status_code": response.status,
                    "headers": headers,
                    "cookies": cookies,
                    "body": body,
                    "elapsed_ms": int(response.elapsed.total_seconds() * 1000),
                }

        except aiohttp.ClientError as e:
            raise Exception(f"HTTP请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"请求发生未知错误: {str(e)}")

    async def get(
        self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """发送GET请求"""
        return await self.request(HTTPMethod.GET, url, params=params, **kwargs)

    async def post(
        self,
        url: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """发送POST请求"""
        return await self.request(
            HTTPMethod.POST, url, json_data=json_data, data=data, **kwargs
        )

    async def put(
        self,
        url: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """发送PUT请求"""
        return await self.request(
            HTTPMethod.PUT, url, json_data=json_data, data=data, **kwargs
        )

    async def delete(self, url: str, **kwargs) -> Dict[str, Any]:
        """发送DELETE请求"""
        return await self.request(HTTPMethod.DELETE, url, **kwargs)

    async def patch(
        self,
        url: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """发送PATCH请求"""
        return await self.request(
            HTTPMethod.PATCH, url, json_data=json_data, data=data, **kwargs
        )
