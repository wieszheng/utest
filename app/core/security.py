# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 22:10
@Author   : shwezheng
@Software : PyCharm
"""

import jwt
import hashlib
from datetime import timedelta, datetime, timezone

import bcrypt
from config import settings

ALGORITHM = "HS256"
SECRET_KEY = "ves8C_LqOJ8_uH_9e0k-7n04Vneha47dMKH_vRwaQrg"


def psw_add_salt(password: str) -> str:
    """
    对密码进行加盐
    :param password:
    :return:
    """
    m = hashlib.md5()
    bt = f"{password}{settings.SALT}".encode("utf-8")
    m.update(bt)
    return m.hexdigest()


def psw_hash(password: str) -> str:
    """
    获取 hash 后的密码
    :param password:
    :return:
    """
    salt_ = bcrypt.gensalt(rounds=6)
    hashed = bcrypt.hashpw(password.encode(), salt_)
    return hashed.decode()


def psw_verify(plain_psw: str, hashed_psw: str) -> bool:
    """
    验证密码
    :param plain_psw: 原密码
    :param hashed_psw: hash后的密码
    :return:
    """

    return bcrypt.checkpw(plain_psw.encode(), hashed_psw.encode())


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    创建 access_token
    :param data: 用户信息
    :param expires_delta: 时间 默认15m
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.now(timezone.utc)})
    to_encode.update({"nbf": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> str | dict:
    """
    解码 access_token
    :param token:
    :return:
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


if __name__ == "__main__":
    print(create_access_token({"sub": '{"username": "string"}'}))
