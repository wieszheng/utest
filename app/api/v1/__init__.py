# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/6 22:02
@Author   : shwezheng
@Software : PyCharm
"""

from fastapi import Header

from app.core.exceptions.errors import ApiError
from app.enums.code import ApiErrorCode


class Authentication:
    def __init__(self, isAdmin: bool = False):
        self.isAdmin = isAdmin

    async def __call__(self, token: str = Header(None)):
        if not token:
            raise ApiError(ApiErrorCode.USER_PASSWORD_REQUIRED)
        # current_user_dict = await UserMapper.parse_token(token)
        #
        # # 要求admin。但是是普通用户
        # if self.isAdmin is True and current_user_dict["isAdmin"] is False:
        #     raise AuthError("无权操作")
        # current_user = await UserMapper.get_by_id(current_user_dict["id"], )
        # LOG.info(f"current user {current_user}")
        return "current_user"
