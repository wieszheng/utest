# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:25
@Author   : shwezheng
@Software : PyCharm
"""

import os
import time

from pydantic_settings import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(ROOT, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

SERVER_LOG_FILE: str = os.path.join(LOG_DIR, f"{time.strftime('%Y-%m-%d')}_server.log")
ERROR_LOG_FILE: str = os.path.join(LOG_DIR, f"{time.strftime('%Y-%m-%d')}_error.log")


class Settings(BaseSettings):
    APP_NAME: str = "uTest"
    APP_VERSION: str = "1.0.0"
    APP_API_STR: str = "/api/v1"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True

    # 数据库配置
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_PROTOCOL: str = "mysql+aiomysql"
    MYSQL_USERNAME: str = "root"
    MYSQL_PASSWORD: str = "mysql123"
    MYSQL_DATABASE: str = "utest"
    MYSQL_CHARSET: str = "utf8mb4"
    MYSQL_ECHO: bool = True
    MYSQL_MAX_OVERFLOW: int = 20
    MYSQL_POOL_SIZE: int = 10
    MYSQL_POOL_RECYCLE: int = 3600
    MYSQL_POOL_TIMEOUT: int = 30

    LOGGING_ROTATION: str = "10 MB"
    DATETIME_TIMEZONE: str = "Asia/Shanghai"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # class Config:
    #     case_sensitive = True
    #     env_file = ".env"


settings = Settings()
