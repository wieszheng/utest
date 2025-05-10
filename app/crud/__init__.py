# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:53
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime, timezone
from functools import wraps
from typing import Generic, Any, TypeVar, Type, Union, Optional, Iterable, List

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import (
    select,
    Row,
    update,
    func,
    delete,
    inspect,
    desc,
    asc,
    BinaryExpression,
    Select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session_maker
from app.enums.status import OrderEnum

ModelType = TypeVar("ModelType", bound=Any)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def compute_offset(page: int, items_per_page: int) -> int:
    return (page - 1) * items_per_page


def with_session(func):
    """
    一个装饰器，用于在没有提供有效的数据库会话时自动创建一个。
    这个装饰器会检查函数的参数中是否已经提供了一个名为'session'的数据库会话，
    如果没有或者不是一个有效的AsyncSession实例，它会自动创建一个新的会话，并在该会话中执行被装饰的函数。
    如果在执行过程中发生任何异常，它会记录错误信息，并重新抛出异常。

    :param func: 被装饰的异步函数，通常是一个与数据库操作相关的函数.
    :return:
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            existing_session = kwargs.get("session")
            if existing_session and isinstance(existing_session, AsyncSession):
                return await func(self, *args, **kwargs)
            else:
                async with async_session_maker() as session:
                    # async with session.begin():
                    kwargs["session"] = session
                    return await func(self, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"操作Model：{self.model.__name__}\n"
                f"方法：{func.__name__}\n"
                f"参数：args：{[*args]}, kwargs：{kwargs}\n"
                f"错误：{e}\n"
            )
            raise

    return wrapper


class BaseCRUD(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        updated_at_column: str = "updated_at",
        deleted_at_column: str = "deleted_at",
        is_deleted_column: str = "is_deleted",
    ) -> None:
        self.model = model
        self.updated_at_column = updated_at_column
        self.deleted_at_column = deleted_at_column
        self.is_deleted_column = is_deleted_column
        self.model_col_names = [col.key for col in model.__table__.columns]
        # self.model_col_names = {_column.name for _column in inspect(model).c}

    def _parse_filters(self, **kwargs: Any) -> list[BinaryExpression]:
        """
        解析过滤器
            直接传值：id=1
            操作符传参：age={"gt": 18}, name={"like": "%john%"}
            支持的操作符：eq, ne, gt, lt, ge, le, like, in

        :param kwargs:
        :return:
        """
        filters = []
        for key, value in kwargs.items():
            if key in self.model_col_names:
                if isinstance(value, dict):
                    for op, val in value.items():
                        if op == "eq":
                            filters.append(getattr(self.model, key) == val)
                        elif op == "ne":
                            filters.append(getattr(self.model, key) != val)
                        elif op == "gt":
                            filters.append(getattr(self.model, key) > val)
                        elif op == "lt":
                            filters.append(getattr(self.model, key) < val)
                        elif op == "ge":
                            filters.append(getattr(self.model, key) >= val)
                        elif op == "le":
                            filters.append(getattr(self.model, key) <= val)
                        elif op == "like":
                            filters.append(getattr(self.model, key).like(val))
                        elif op == "in":
                            filters.append(getattr(self.model, key).in_(val))
                        else:
                            raise ValueError(f"Unsupported operator: {op}")
                else:
                    filters.append(getattr(self.model, key) == value)
            else:
                raise ValueError(f"Invalid column name: {key}")
        return filters

    def _apply_order_by(
        self,
        query: Select,
        order_bys: Union[str, list[str]],
        orders: Union[OrderEnum, list[OrderEnum]],
    ) -> Select:
        """
        应用排序条件

        :param query: SQLAlchemy 查询对象
        :param order_bys: 排序字段列表，例如 ["name", "age"] 或单个字段字符串
        :param orders: 对应每个字段的排序方式列表，例如 [OrderEnum.ascent, OrderEnum.desc]
        :return:
        """
        if isinstance(order_bys, str):
            order_bys = [order_bys]

        if isinstance(orders, OrderEnum):
            orders = [orders] * len(order_bys)

        if len(order_bys) != len(orders):
            raise ValueError("Length of 'order_bys' and 'orders' must be the same.")

        for field in order_bys:
            if field not in self.model_col_names:
                raise ValueError(f"Invalid column name for order_by: {field}")

        for order_by, order in zip(order_bys, orders):
            query = query.order_by(
                asc(getattr(self.model, order_by))
                if order == OrderEnum.ascent
                else desc(getattr(self.model, order_by))
            )

        return query

    @with_session
    async def create(
        self,
        obj: Union[CreateSchemaType, dict[str, Any]],
        commit: bool = True,
        session: AsyncSession = None,
    ) -> ModelType:
        """
        创建模型的新实例

        :param session：异步数据库会话.
        :param obj: 包含要保存的数据的 Pydantic 模式或字典.
        :param commit: 如果为 'True'，则立即提交事务。默认值为 'True'.
        :return:
        """
        if isinstance(obj, dict):
            ins: ModelType = self.model(**obj)
        else:
            ins: ModelType = self.model(**obj.model_dump())

        session.add(ins)
        if commit:
            await session.commit()
        return ins

    @with_session
    async def create_multiple(
        self,
        objs: Iterable[Union[CreateSchemaType, dict[str, Any]]],
        commit: bool = True,
        session: AsyncSession = None,
    ) -> List[ModelType]:
        """
        创建多个模型的新示例

        :param session：异步数据库会话.
        :param objs: 包含要保存的多个数据的 Pydantic 模式或字典的列表.
        :param commit: 如果为 'True'，则立即提交事务。默认值为 'True'.
        :return:
        """
        ins_list: list[ModelType] = []
        for obj in objs:
            if isinstance(obj, dict):
                ins_list.append(self.model(**obj))
            else:
                ins_list.append(self.model(**obj.model_dump()))

        session.add_all(ins_list)

        if commit:
            await session.commit()

        return ins_list

    @with_session
    async def get(
        self,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> ModelType | None:
        """
        获取模型实例
        :param session: 异步数据库会话.
        :param kwargs: 用于构建查询过滤条件的任意关键字参数.
        :return:
        """
        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters)
        row = await session.execute(query)
        result: Optional[Row] = row.scalar_one_or_none()
        if result is None:
            return None
        return result

    @with_session
    async def exists(self, session: AsyncSession = None, **kwargs: Any) -> bool:
        """
        检查模型实例是否存在
        :param session: 异步数据库会话.
        :param kwargs: 用于构建查询过滤条件的任意关键字参数.
        :return:
        """
        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters).limit(1)

        row = await session.execute(query)
        return row.first() is not None

    @with_session
    async def get_multiple(
        self,
        *,
        session: AsyncSession = None,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> list[ModelType]:
        """
        获取模型实例列表
        :param session: 异步数据库会话
        :param offset: 查询偏移量，必须为非负整数
        :param limit: 查询条目上限，必须为非负整数，None 表示无上限（慎用）
        :param kwargs: 过滤条件，传递给 _parse_filters 方法
        :return: 模型实例列表
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters).offset(offset).limit(limit)
        result = await session.execute(query)

        return list(result.scalars().all())

    @with_session
    async def get_multiple_ordered(
        self,
        session: AsyncSession = None,
        order_bys: Union[str, list[str]] = "uid",
        orders: Union[str, list[OrderEnum]] = OrderEnum.ascent,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> list[ModelType]:
        """
        获取模型实例列表，并按多个字段排序

        :param session: 异步数据库会话
        :param order_bys: 排序字段列表，例如 ["name", "age"] 或单个字段字符串
        :param orders: 对应每个字段的排序方式列表，例如 [OrderEnum.ascent, OrderEnum.desc]
        :param offset: 起始偏移量
        :param limit: 查询数量限制
        :param kwargs: 用于构建查询过滤条件的任意关键字参数
        :return: 按照指定字段排序后的模型实例列表
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters)

        query = (
            self._apply_order_by(query, order_bys, orders).offset(offset).limit(limit)
        )

        result = await session.execute(query)

        return list(result.scalars().all())

    @with_session
    async def count(
        self,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> int:
        """
        获取模型实例的数量
        :param session: 异步数据库会话
        :param kwargs:
        :return: 符合条件的记录总数，若无结果则返回 0
        """
        filters = self._parse_filters(**kwargs)
        count_query = select(func.count()).select_from(self.model)

        if filters:
            count_query = count_query.where(*filters)
        total_count: Optional[int] = await session.scalar(count_query)

        return total_count or 0

    @with_session
    async def update(
        self,
        obj_new: Union[UpdateSchemaType, dict[str, Any]],
        allow_multiple: bool = False,
        commit: bool = True,
        session: AsyncSession = None,
        **kwargs: Any,
    ) -> None:
        """
        更新模型实例
        :param session: 异步数据库会话
        :param obj_new: 新的对象数据，可以是更新模式类型的实例或字典
        :param allow_multiple: 是否允许更新多个记录，默认为False
        :param commit: 是否提交事务，默认为True
        :param kwargs: 额外的关键字参数，用于查询需要更新的记录
        :return:
        """
        total_count = await self.count(session, **kwargs)
        if total_count == 0:
            raise ValueError("No record found to update.")
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"Expected exactly one record to update, found {total_count}."
            )

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(exclude_unset=True)

        updated_at_col = getattr(self.model, self.updated_at_column, None)
        if updated_at_col:
            update_data[self.updated_at_column] = datetime.now(timezone.utc)

        update_data_keys = set(update_data.keys())
        model_columns = {_column.name for _column in inspect(self.model).c}
        extra_fields = update_data_keys - model_columns
        if extra_fields:
            raise ValueError(f"Extra fields provided: {extra_fields}")

        filters = self._parse_filters(**kwargs)
        query = update(self.model).filter(*filters).values(update_data)

        if commit:
            await session.execute(query)
            await session.commit()

    @with_session
    async def delete_data(
        self,
        session: AsyncSession = None,
        allow_multiple: bool = False,
        commit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        删除模型实例
        :param session: 异步数据库会话
        :param allow_multiple: 是否允许删除多条记录
        :param commit:
        :param kwargs:
        :return:
        """
        if (
            not allow_multiple
            and (total_count := await self.count(session, **kwargs)) > 1
        ):
            raise ValueError(
                f"Expected exactly one record to delete, found {total_count}."
            )

        filters = self._parse_filters(**kwargs)
        query = delete(self.model).filter(*filters)

        if commit:
            await session.execute(query)
            await session.commit()

    @with_session
    async def delete(
        self,
        session: AsyncSession = None,
        allow_multiple: bool = False,
        commit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        删除模型实例
        :param session: 异步数据库会话
        :param allow_multiple: 是否允许删除多条记录
        :param commit:
        :param kwargs:
        :return:
        """
        filters = self._parse_filters(**kwargs)

        total_count = await self.count(session, **kwargs)
        if total_count == 0:
            raise ValueError("No record found to delete.")
        if not allow_multiple and total_count > 1:
            raise ValueError(
                f"Expected exactly one record to delete, found {total_count}."
            )

        update_values: dict[str, Union[bool, datetime]] = {}
        if self.deleted_at_column in self.model_col_names:
            update_values[self.deleted_at_column] = datetime.now(timezone.utc)
        if self.is_deleted_column in self.model_col_names:
            update_values[self.is_deleted_column] = True

        if update_values:
            update_stmt = update(self.model).filter(*filters).values(**update_values)
            await session.execute(update_stmt)
        else:
            delete_stmt = self.model.__table__.delete().where(*filters)
            await session.execute(delete_stmt)

        if commit:
            await session.commit()
