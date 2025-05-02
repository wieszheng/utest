# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:53
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime, timezone
from typing import Generic, Any, TypeVar, Type, Union, Optional

from pydantic import BaseModel
from sqlalchemy import select, Row, update, func, delete, inspect, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.status import OrderEnum

ModelType = TypeVar("ModelType", bound=Any)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def compute_offset(page: int, items_per_page: int) -> int:
    return (page - 1) * items_per_page


class BaseCRUD(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        is_deleted_column: str = "is_deleted",
        deleted_at_column: str = "deleted_at",
        updated_at_column: str = "updated_at",
    ) -> None:
        self.model = model
        self.model_col_names = [col.key for col in model.__table__.columns]
        self.is_deleted_column = is_deleted_column
        self.deleted_at_column = deleted_at_column
        self.updated_at_column = updated_at_column

    def _parse_filters(self, **kwargs: Any) -> list[Any]:
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

    async def create(
        self,
        session: AsyncSession,
        obj: Union[CreateSchemaType, dict[str, Any]],
        commit: bool = True,
    ) -> ModelType:
        """
        创建模型的新实例

        :param session：SQLAlchemy 异步会话.
        :param obj: 包含要保存的数据的 Pydantic 模式或字典.
        :param commit: 如果为 'True'，则立即提交事务。默认值为 'True'.
        :return:
        """
        if isinstance(obj, dict):
            data: ModelType = self.model(**obj)
        else:
            data: ModelType = self.model(**obj.model_dump())

        session.add(data)
        if commit:
            await session.commit()
        return data

    async def get(
        self,
        session: AsyncSession,
        **kwargs: Any,
    ) -> ModelType | None:
        """
        获取模型实例
        :param session: 用于执行数据库操作的异步会话对象
        :param kwargs: 用于构建查询过滤条件的任意关键字参数
        :return:
        """
        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters)
        row = await session.execute(query)
        result: Optional[Row] = row.scalar_one_or_none()
        if result is None:
            return None
        return result

    async def get_multiple(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> list[ModelType]:
        """
        获取模型实例列表
        :param session:
        :param offset:
        :param limit:
        :param kwargs:
        :return:
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters).offset(offset).limit(limit)
        rows = await session.execute(query)

        return [row for row in rows]

    async def get_multiple_ordered(
        self,
        session: AsyncSession,
        order_bys: list[str] | str = "uid",
        orders: list[OrderEnum] | OrderEnum = OrderEnum.ascent,
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> list[ModelType]:
        """
        获取模型实例列表，并按多个字段排序

        :param session: SQLAlchemy 异步会话对象
        :param order_bys: 排序字段列表，例如 ["name", "age"] 或单个字段字符串
        :param orders: 对应每个字段的排序方式列表，例如 [OrderEnum.ascent, OrderEnum.desc]
        :param offset: 起始偏移量
        :param limit: 查询数量限制
        :param kwargs: 用于构建查询过滤条件的任意关键字参数
        :return: 按照指定字段排序后的模型实例列表
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise ValueError("Limit and offset must be non-negative.")

        if isinstance(order_bys, str):
            order_bys = [order_bys]
        if isinstance(orders, OrderEnum):
            orders = [orders] * len(order_bys)

        if len(order_bys) != len(orders):
            raise ValueError("Length of 'order_bys' and 'orders' must be the same.")

        for field in order_bys:
            if field not in self.model_col_names:
                raise ValueError(f"Invalid column name for order_by: {field}")

        filters = self._parse_filters(**kwargs)
        query = select(self.model).filter(*filters)
        for order_by, order in zip(order_bys, orders):
            query = query.order_by(
                asc(getattr(self.model, order_by))
                if order == OrderEnum.ascent
                else desc(getattr(self.model, order_by))
            )

        query = query.offset(offset).limit(limit)

        rows = await session.execute(query)

        return [row for row in rows]

    async def count(
        self,
        session: AsyncSession,
        **kwargs: Any,
    ) -> int:
        """
        获取模型实例的数量
        :param session:
        :param kwargs:
        :return:
        """
        count_query = select(func.count()).select_from(self.model)
        count_query = count_query.filter_by(**kwargs)
        total_count: Optional[int] = await session.scalar(count_query)
        if total_count is None:
            raise ValueError("Could not find the count.")

        return total_count

    async def update(
        self,
        session: AsyncSession,
        obj_new: Union[UpdateSchemaType, dict[str, Any]],
        allow_multiple: bool = False,
        commit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        更新模型实例
        :param session:
        :param obj_new:
        :param allow_multiple:
        :param commit:
        :param kwargs:
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

    async def delete_data(
        self,
        session: AsyncSession,
        allow_multiple: bool = False,
        commit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        删除模型实例
        :param session:
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

    async def delete(
        self,
        session: AsyncSession,
        allow_multiple: bool = False,
        commit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        删除模型实例
        :param session:
        :param allow_multiple:
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
