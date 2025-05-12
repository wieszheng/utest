# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/6 22:02
@Author   : shwezheng
@Software : PyCharm
"""

from typing import Annotated

from fastapi import Header, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError

from app.core.exceptions.errors import ApiError
from app.core.security import decode_access_token
from app.enums.code import ApiErrorCode
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/system/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise ApiError(ApiErrorCode.TOKEN_NOT_PROVIDED)
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise ApiError(ApiErrorCode.UNSUPPORTED_TOKEN_TYPE)
    from app.crud.crud_user import crud_user

    user = await crud_user.get(username=token_data.username)
    if user.is_active is False:
        raise ApiError(ApiErrorCode.USER_ACCOUNT_LOCKED)
    if user is None:
        raise ApiError(ApiErrorCode.TOKEN_REVOKED)
    return user


class Authentication:
    def __init__(self, is_admin: bool = False):
        self.is_admin = is_admin

    async def __call__(self, token: str = Header(None)):
        if not token:
            raise ApiError(ApiErrorCode.TOKEN_NOT_PROVIDED)
        try:
            from app.crud.crud_user import crud_user

            payload = decode_access_token(token)
            self._validate_token_payload(payload)
            username = payload["sub"]
            token_data = TokenData(username=username)
        except ExpiredSignatureError:
            raise ApiError(ApiErrorCode.EXPIRED_TOKEN)
        except InvalidTokenError:
            raise ApiError(ApiErrorCode.UNSUPPORTED_TOKEN_TYPE)
        user = await crud_user.get(username=token_data.username)
        if user.is_active is False:
            raise ApiError(ApiErrorCode.USER_ACCOUNT_LOCKED)
        if self.is_admin is True and user.is_admin is False:
            raise ApiError(ApiErrorCode.ACCESS_DENIED_TO_RESOURCE)
        return user

    def _validate_token_payload(self, payload: dict):
        """确保 token 的 payload 包含必要字段并有效"""
        if not isinstance(payload, dict):
            raise ValueError("令牌负载结构无效")
        username = payload.get("sub")
        if not username:
            raise ValueError("令牌有效负载中缺少 'sub'")
