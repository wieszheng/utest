#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:53
@Author   : shwezheng
@Software : PyCharm
"""

import functools
import time
from datetime import datetime
from typing import Any, Callable, TypeVar, cast, Dict

from app.crud import BaseCRUD
from app.models.log import Log, OperationType
from app.schemas.log import LogCreate


def get_model_diff(
    old_data: Dict[str, Any] | None, new_data: Dict[str, Any] | None
) -> Dict[str, Any]:
    """
    获取新旧数据的差异

    :param old_data: 旧数据
    :param new_data: 新数据
    :return: 差异数据
    """
    if not old_data or not new_data:
        return {}

    diff = {}
    all_keys = set(old_data.keys()) | set(new_data.keys())

    for key in all_keys:
        old_value = old_data.get(key)
        new_value = new_data.get(key)

        if old_value != new_value:
            diff[key] = {"old": old_value, "new": new_value}

    return diff


T = TypeVar("T", bound=BaseCRUD)


def log_changes(
    title: str,
    operation_type: OperationType,
    description: str | None = None,
):
    """
    数据库操作日志记录装饰器

    :param title: 操作标题
    :param operation_type: 操作类型
    :param description: 操作描述
    :return: 装饰器函数
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            start_time = time.time()
            old_data = None
            new_data = None

            try:
                if operation_type == OperationType.UPDATE and len(args) > 0:
                    obj_new = args[0]
                    if hasattr(obj_new, "model_dump"):
                        new_data = obj_new.model_dump(exclude_unset=True)
                    elif isinstance(obj_new, dict):
                        new_data = obj_new

                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                raise e
            finally:
                duration = (time.time() - start_time) * 1000  # 转换为毫秒
                diff_data = get_model_diff(old_data, new_data)
                log_data = LogCreate(
                    user_id="user_id",
                    operation_type=operation_type,
                    title=title,
                    description=description,
                    old_data=old_data,
                    new_data=new_data,
                    diff_data=diff_data,
                    tag="tag",
                    duration=duration,
                    operate_time=datetime.now(),
                )
                log_crud = BaseCRUD(Log)
                await log_crud.create(obj=log_data)

        return cast(Callable[..., Any], wrapper)

    return decorator
