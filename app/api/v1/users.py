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

from fastapi import APIRouter, Query
from faker import Faker
from pydantic import EmailStr

from app.core.client.mail import render_email_template, send_mail
from app.core.exceptions.errors import ApiError
from app.core.security import psw_hash
from app.crud.crud_user import crud_user
from app.enums.code import ApiErrorCode
from app.schemas.common import ResponseModel
from app.schemas.user import UserCreate, User, UserEmailCreate

router = APIRouter()
fake = Faker()

captcha: str = str(fake.random_int(min=100000, max=999999))


@router.post("/user", summary="账户密码创建用户", response_model=ResponseModel[User])
async def create_user(user: UserCreate) -> ResponseModel[User]:
    if not user.password_hash:
        raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
    if await crud_user.exists(username=user.username):
        raise ApiError(ApiErrorCode.USERNAME_ALREADY_EXISTS)
    if await crud_user.exists(nickname=user.nickname):
        raise ApiError(ApiErrorCode.NICKNAME_ALREADY_EXISTS)

    user.password_hash = psw_hash(user.password_hash)
    user = await crud_user.create(obj=user)
    return ResponseModel(data=user)


@router.post("/email", summary="邮箱号创建用户", response_model=ResponseModel[User])
async def create_user_by_email(user: UserEmailCreate) -> ResponseModel[User]:
    if not user.password_hash:
        raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
    if await crud_user.exists(email=user.email):
        raise ApiError(ApiErrorCode.EMAIL_ALREADY_EXISTS)

    if user.code != captcha:
        raise ApiError(ApiErrorCode.CAPTCHA_INCORRECT)

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


@router.get("/verification", summary="获取验证码", response_model=ResponseModel)
async def get_verification_code(
    email: EmailStr = Query(..., description="邮箱地址"),
) -> ResponseModel:
    global captcha
    captcha = str(fake.random_int(min=100000, max=999999))
    content = render_email_template(
        template_name="verification-email.html", context={"code": captcha}
    )
    await send_mail("注册验证码", [str(email)], content)
    return ResponseModel()


@router.get("/users/", response_model=ResponseModel[List[User]])
async def read_users(limit: int = 100, offset: int = 0) -> ResponseModel[List[User]]:
    users: List[User] = await crud_user.get_multiple(offset=offset, limit=limit)

    return ResponseModel(data=users)
