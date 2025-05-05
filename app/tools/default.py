# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/5 15:11
@Author   : shwezheng
@Software : PyCharm
"""

import hashlib
import time
from functools import wraps
from dataclasses import dataclass
from typing import Callable

from fastapi import Request, HTTPException


@dataclass
class RateLimit:
    max_calls: int
    period: int


api_key_limits: dict[str, RateLimit] = {
    "code": RateLimit(max_calls=100, period=60),
    "another_api_key": RateLimit(max_calls=50, period=60),
}


def rate_limit(max_calls: int, period: int):
    """
    Rate limit 装饰器。

    :param max_calls：给定时间段内允许的最大请求数。
    :param period：以秒为单位的时间段。
    """

    def decorator(func: Callable) -> Callable:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if not request.client:
                raise ValueError("无法获取客户端信息")

            ip_address: str = request.client.host

            unique_id: str = hashlib.sha256(ip_address.encode()).hexdigest()
            now = time.time()

            if unique_id not in usage:
                usage[unique_id] = []
            timestamps = usage[unique_id]
            timestamps[:] = [t for t in timestamps if now - t < period]
            if len(timestamps) < max_calls:
                timestamps.append(now)
                return await func(request, *args, **kwargs)

            wail = period - (now - timestamps[0])
            raise HTTPException(
                status_code=429, detail=f"请求太频繁，请等待 {wail:.2f} 秒后再试"
            )

        return wrapper

    return decorator
