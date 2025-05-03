# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:44
@Author   : shwezheng
@Software : PyCharm
"""

import re
from typing import List

from fastapi import APIRouter
from faker import Faker
from app.core.exceptions.errors import ApiError
from app.core.security import psw_hash
from app.crud.crud_user import crud_user
from app.database.db import currentSession
from app.enums.code import ApiErrorCode
from app.schemas.common import ResponseModel
from app.schemas.user import UserCreate, User, UserEmailCreate

router = APIRouter()
fake = Faker()


@router.post("/user", summary="账户密码创建用户", response_model=ResponseModel[User])
async def create_user(user: UserCreate) -> ResponseModel[User]:
    if not user.password_hash:
        raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
    if await crud_user.exists(username=user.username):
        raise ApiError(ApiErrorCode.USERNAME_ALREADY_EXISTS)
    if await crud_user.exists(nickname=user.nickname):
        raise ApiError(ApiErrorCode.NICKNAME_ALREADY_EXISTS)
    if await crud_user.exists(email=user.email):
        raise ApiError(ApiErrorCode.EMAIL_ALREADY_EXISTS)
    user.password_hash = psw_hash(user.password_hash)
    user = await crud_user.create(obj=user)
    return ResponseModel(data=user)


@router.post("/email", summary="邮箱号创建用户", response_model=ResponseModel[User])
async def create_user_by_email(user: UserEmailCreate) -> ResponseModel[User]:
    if not user.password_hash:
        raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
    if await crud_user.exists(email=user.email):
        raise ApiError(ApiErrorCode.EMAIL_ALREADY_EXISTS)

    text = re.sub(r"[^\w]", "", str(user.email).split("@")[0])
    suffix = ""
    count = 0
    nickname = fake.name() + text + suffix
    while True:
        if not await crud_user.exists(nickname=nickname):
            break
        count += 1
        suffix = str(count)
        nickname = fake.name() + text + suffix

    user = await crud_user.create(
        obj={
            "username": user.email,
            "nickname": nickname,
            "email": user.email,
            "password_hash": psw_hash(user.password_hash),
        }
    )
    return ResponseModel(data=user)


@router.get("/users/", response_model=ResponseModel[List[User]])
async def read_users(
    session: currentSession, limit: int = 100, offset: int = 0
) -> ResponseModel[List[User]]:
    users: List[User] = await crud_user.get_multiple(session, offset, limit)

    return ResponseModel(data=users)
