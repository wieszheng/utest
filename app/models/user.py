# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 20:56
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import UTestModel


class User(UTestModel):
    """
    用户模型
    """

    username: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, sort_order=2
    )
    email: Mapped[EmailStr] = mapped_column(
        String(64), unique=True, index=True, sort_order=3
    )
    password_hash: Mapped[str] = mapped_column(
        String(180), nullable=False, sort_order=4
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, sort_order=5)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, sort_order=6)
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True, sort_order=7
    )
