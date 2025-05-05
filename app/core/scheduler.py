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

from config import settings

job_store = {
    "default": SQLAlchemyJobStore(
        url=f"mysql+mysqlconnector://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@"
        f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset=utf8mb4",
        tablename="jobs",
        engine_options={"pool_recycle": 1500},
        pickle_protocol=3,
    )
}

scheduler = AsyncIOScheduler(jobstores=job_store)
__all__ = ["scheduler"]
