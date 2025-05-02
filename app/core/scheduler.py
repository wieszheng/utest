# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 01:22
@Author   : shwezheng
@Software : PyCharm
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

DATABASE_URL = (
    "mysql+mysqlconnector://root:mysql123@127.0.0.1:3306/utest?charset=utf8mb4"
)

job_store = {
    "default": SQLAlchemyJobStore(
        url=DATABASE_URL,
        tablename="jobs",
        engine_options={"pool_recycle": 1500},
        pickle_protocol=3,
    )
}

scheduler = AsyncIOScheduler(jobstores=job_store)
__all__ = ["scheduler"]
