# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:44
@Author   : shwezheng
@Software : PyCharm
"""

from typing import List

from fastapi import APIRouter

from app.crud.crud_user import crud_user
from app.database.db import currentSession
from app.schemas.common import ResponseModel
from app.schemas.user import UserCreate, User

router = APIRouter()


@router.post("/users/", response_model=ResponseModel[User])
async def create_user(user: UserCreate, session: currentSession) -> ResponseModel[User]:
    created_user: User = await crud_user.create_user(session, obj=user)
    return ResponseModel(data=created_user)


@router.get("/users/", response_model=ResponseModel[List[User]])
async def read_users(
    session: currentSession, limit: int = 100, offset: int = 0
) -> ResponseModel[List[User]]:
    users: List[User] = await crud_user.get_multiple(session, offset, limit)

    return ResponseModel(data=users)


@router.get("/count")
async def read_user(session: currentSession):
    count = await crud_user.count(session)
    return ResponseModel(data={"count": count})
