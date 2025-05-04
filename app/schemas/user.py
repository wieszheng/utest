# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 21:22
@Author   : shwezheng
@Software : PyCharm
"""

from pydantic import BaseModel, EmailStr

from app.schemas.common import UTestModel


class UserBase(BaseModel):
    username: str
    nickname: str


class UserCreate(UserBase):
    password_hash: str


class UserEmailCreate(BaseModel):
    email: EmailStr
    password_hash: str
    code: str


class UserUpdate(UserBase):
    password_hash: str


class User(UTestModel, UserBase):
    pass
