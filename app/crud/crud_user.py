# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/21 22:06
@Author   : shwezheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.user import Users


class CRUDUser(BaseCRUD[Users]): ...


crud_user: CRUDUser = CRUDUser(Users)
