# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/20 21:38
@Author   : shwezheng
@Software : PyCharm
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.staticfiles import StaticFiles

from app import lifespan
from app.api import api_router_v1
from app.core.exceptions.exception_handler import register_exception
from app.tools.openapi import get_stoplight_ui_html

from config import settings, SERVER_LOG_FILE, ERROR_LOG_FILE

description = """
    \n\n![](https://i.ibb.co/v3Yt03v/todo-api-background.png)\n\n ## \U0001f4ab Overview\n\nTo Do API provides a simple way
    for people to manage their tasks and plan their day. This API can be used to create mobile and web applications.This
    API is documented using **OpenAPI 3.0**. The implementation lives in this [GitHub
    repo](https://github.com/stoplight-qa/studio-demo/blob/main/reference/todos/todo.v1.yaml).
    \n\n ### \U0001f9f0 Cross-Origin Resource Sharing\n\nThis API features Cross-Origin Resource Sharing (CORS) implemented in compliance
    with  [W3C spec](https://www.w3.org/TR/cors/). CORS support is necessary to make calls from the request maker within
    the API docs.\n\n### \U0001f3c1 Trying out your own API Specification\nElements can be used to generate API docs for
    any OpenAPI document. Replace this OpenAPI with a URL to your own OpenAPI document to get started.
"""


LOGGING_CONF: dict = {
    "server_handler": {
        "file": SERVER_LOG_FILE,
        "level": "INFO",
        "rotation": "10 MB",
        "backtrace": False,
        "diagnose": False,
    },
    "error_handler": {
        "file": ERROR_LOG_FILE,
        "level": "ERROR",
        "rotation": "10 MB",
        "backtrace": True,
        "diagnose": True,
    },
}
# init_logging(LOGGING_CONF)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=description,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(api_router_v1, prefix=settings.APP_API_STR)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/openapi", include_in_schema=False)
async def api_documentation():
    """Add stoplight elements api doc. https://dev.to/amal/replacing-fastapis-default-api-docs-with-elements-391d"""
    return get_stoplight_ui_html(
        openapi_url="/openapi.json",
        title=settings.APP_NAME + " - OpenApi",
        logo="/static/utest.svg",
        stoplight_elements_favicon_url="/static/utest.svg",
    )


register_exception(app)

if __name__ == "__main__":
    logger.info("Starting the server")
    uvicorn.run(
        app="main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD,
        forwarded_allow_ips="*",
        access_log=True,
    )
