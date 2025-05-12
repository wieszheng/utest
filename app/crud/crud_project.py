# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/11 21:01
@Author   : shwezheng
@Software : PyCharm
"""

from app.crud import BaseCRUD
from app.models.project import Projects


class CRUDProject(BaseCRUD[Projects]): ...


crud_project: CRUDProject = CRUDProject(Projects)
