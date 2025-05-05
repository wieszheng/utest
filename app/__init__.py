# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/19 23:57
@Author   : shwezheng
@Software : PyCharm
"""

import logging
from contextlib import asynccontextmanager
from types import FrameType
from typing import cast

from fastapi import FastAPI
from loguru import logger

from app.core.client.redis_ import redis_client
from app.core.scheduler import scheduler
from app.models import create_table


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def init_logging(logging_conf: dict):
    """
    初始化日志
    :param logging_conf: 日志配置字典
    :return:
    """
    logger.info("初始化日志记录")
    LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

    # change handler for default uvicorn logger
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]

    # for name in logging.root.manager.loggerDict:
    #     if name.startswith("uvicorn"):
    #         logging.getLogger(name).handlers = []
    #
    # logging.getLogger("uvicorn").handlers = [InterceptHandler()]

    for log_handler, log_conf in logging_conf.items():
        log_file = log_conf.pop("file", None)
        logger.add(log_file, **log_conf)

    logger.info("设置日志记录成功")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    启动初始化

    :return:
    """
    logger.info("Starting up the application")
    await create_table()
    await redis_client.connect()

    scheduler.start()
    yield
    scheduler.shutdown()
    await redis_client.disconnect()
    logger.info("Shutting down the application")
