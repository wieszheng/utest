# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 22:06
@Author   : shwezheng
@Software : PyCharm
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCRUD
from app.core.security import psw_hash
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser(BaseCRUD[User]):
    async def create_user(self, session: AsyncSession, obj: UserCreate) -> User:
        """
        创建用户
        :param session:
        :param obj:
        :return:
        """
        obj.password_hash = psw_hash(obj.password_hash)
        return await self.create(session, obj=obj)


crud_users: CRUDUser = CRUDUser(User)
