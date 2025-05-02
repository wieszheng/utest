# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:34
@Author   : shwezheng
@Software : PyCharm
"""

import inspect
from datetime import datetime, date, time
import decimal
import json
from functools import wraps
from typing import TypeVar, Generic, Optional, Any, Dict, Callable
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeMeta
from starlette.responses import JSONResponse

T = TypeVar("T")


def unified_resp(func: Callable[..., T]):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        if inspect.iscoroutinefunction(func):
            resp = await func(*args, **kwargs) or []
        else:
            resp = func(*args, **kwargs) or []

        return Success(data=resp)

    return wrapper


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""

    success: bool = True
    code: int = 200
    message: str = "ok"
    data: Optional[T] = None


class ResponsePageModel(BaseModel, Generic[T]):
    """分页响应模型"""

    success: bool = True
    code: int = 200
    message: str = "ok"
    data: Optional[T] = None
    total: int = 0
    page: int = 1
    size: int = 10


class UTestModel(BaseModel):
    uid: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
    )


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 如果对象具有keys和__getitem__属性，则返回对象的字典表示
        if hasattr(obj, "keys") and hasattr(obj, "__getitem__"):
            return dict(obj)
        # 如果对象是datetime.datetime类型，则将其转换为字符串格式
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        # 如果对象是datetime.date类型，则将其转换为字符串格式
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        # 如果对象是datetime.time类型，则将其转换为ISO格式字符串
        elif isinstance(obj, time):
            return obj.isoformat()
        # 如果对象是decimal.Decimal类型，则将其转换为浮点数
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        # 如果对象是bytes类型，则将其转换为UTF-8编码的字符串
        elif isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        # 如果对象的类是DeclarativeMeta类型，则将其序列化为JSON
        elif isinstance(obj.__class__, DeclarativeMeta):
            # 如果是查询返回所有的那种models类型的，需要处理些
            # 将SqlAlchemy结果序列化为JSON--查询全部的时候的处理返回
            return self.default(
                {i.name: getattr(obj, i.name) for i in obj.__table__.columns}
            )
        # 如果对象是字典类型，则递归处理其中的值
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    if isinstance(obj[k], (datetime, date, DeclarativeMeta)):
                        obj[k] = self.default(obj[k])
                    else:
                        obj[k] = obj[k]
                except TypeError:
                    obj[k] = None
            return obj

        # 默认情况下，使用JSONEncoder的默认处理方式
        return json.JSONEncoder.default(self, obj)


class ApiResponse(JSONResponse):
    http_status_code = 200
    code = 200
    success = False
    message = "ok"
    data: Optional[Dict[str, Any]] = None  # 结果可以是{} 或 []

    def __init__(
        self,
        success=None,
        http_status_code=None,
        code=None,
        data=None,
        message=None,
        **kwargs,
    ):
        self.message = message or self.message
        self.code = code or self.code
        self.success = success or self.success
        self.http_status_code = http_status_code or self.http_status_code
        self.data = data or self.data

        # 返回内容体
        content = dict(
            message=self.message,
            code=self.code,
            success=self.success,
            data=self.data,
        )
        content.update(kwargs)
        super(ApiResponse, self).__init__(
            status_code=self.http_status_code,
            content=content,
            media_type="application/json;charset=utf-8",
        )

    # 这个render会自动调用，如果这里需要特殊的处理的话，可以重写这个地方
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CJsonEncoder,
        ).encode("utf-8")


class Success(ApiResponse):
    http_status_code = 200
    code = 200
    data = None  # 结果可以是{} 或 []
    message = "ok"
    success = True


class Fail(ApiResponse):
    http_status_code = 200
    code = -1
    data = None  # 结果可以是{} 或 []
    message = "err"
    success = False
