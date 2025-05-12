# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:44
@Author   : shwezheng
@Software : PyCharm
"""

import re
from typing import List, Annotated

from fastapi import APIRouter, Query, BackgroundTasks, Request, Depends
from faker import Faker
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1 import get_current_user
from app.core.client.mail import render_email_template, send_mail, generate_code
from app.core.client.redisEx import redis_client
from app.core.exceptions.errors import ApiError
from app.core.security import psw_hash, create_access_token, psw_verify
from app.crud.crud_user import crud_user
from app.enums.code import ApiErrorCode
from app.models.user import Users
from app.schemas.common import ResponseModel
from app.schemas.user import UserCreate, User, UserEmailCreate, Token
from app.tools.default import rate_limit

router = APIRouter()
fake = Faker()


@router.post("/user", summary="账户密码创建用户", response_model=ResponseModel[User])
async def create_user(user: UserCreate) -> ResponseModel[User]:
    """
    账户密码创建用户
    """
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
    """
    邮箱号创建用户
    """
    if not user.password_hash:
        raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
    if await crud_user.exists(email=user.email):
        raise ApiError(ApiErrorCode.EMAIL_ALREADY_EXISTS)

    rc = await redis_client.client
    stored_code = await rc.get(user.email)
    if stored_code != user.code:
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
    await rc.delete(user.email)
    return ResponseModel(data=user)


@router.get("/verification", summary="获取验证码", response_model=ResponseModel)
@rate_limit(max_calls=1, period=60)
async def get_verification_code(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Query(..., description="邮箱地址"),
) -> ResponseModel:
    """
    获取注册验证码
    """
    rc = await redis_client.client

    code = generate_code()
    await rc.setex(email, 120, code)
    content = render_email_template(
        template_name="verification-email.html", context={"code": code}
    )
    background_tasks.add_task(send_mail, "注册验证码", [str(email)], content)
    return ResponseModel()


@router.get("/users/", response_model=ResponseModel[List[User]])
async def read_users(limit: int = 100, offset: int = 0) -> ResponseModel[List[User]]:
    users: List[Users] = await crud_user.get_multiple(offset=offset, limit=limit)

    return ResponseModel(data=users)


@router.post("/login", summary="用户登录", response_model=ResponseModel[Token])
async def login(username: str, password: str) -> ResponseModel[Token]:
    """
    用户账号密码登录
    """
    user = await crud_user.get(username=username)

    if not user:
        raise ApiError(ApiErrorCode.WRONG_USER_NAME_OR_PASSWORD)
    if not psw_verify(password, user.password_hash):
        raise ApiError(ApiErrorCode.WRONG_USER_NAME_OR_PASSWORD)
    access_token = create_access_token(data={"sub": user.username})

    return ResponseModel(data=Token(access_token=access_token, token_type="bearer"))


@router.post("/token", summary="token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    docs获取token
    """
    user = await crud_user.get(username=form_data.username)

    if not user:
        raise ApiError(ApiErrorCode.WRONG_USER_NAME_OR_PASSWORD)
    if not psw_verify(form_data.password, user.password_hash):
        raise ApiError(ApiErrorCode.WRONG_USER_NAME_OR_PASSWORD)
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
