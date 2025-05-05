# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/4/30 10:51
@Author   : shwezheng
@Software : PyCharm
"""

import asyncio
import base64
import json
import os
import random
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import aiosmtplib
from aiosmtplib import SMTPDataError
from jinja2 import Template

from app.core.exceptions.errors import ApiException
from config import ROOT


def generate_code() -> str:
    return str(random.randint(100000, 999999))


def get_config():
    file_path = os.path.join(ROOT, "config.json")
    if not os.path.exists(file_path):
        raise Exception("没有找的配置文件，请检查")
    with open(file_path, mode="r", encoding="utf-8") as f:
        return json.load(f)


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent.parent / "templates" / template_name
    ).read_text(encoding="utf-8")
    html_content = Template(template_str).render(context)
    return html_content


async def send_mail(subject: str, receivers: list[str], html_content: str) -> None:
    # data = get_config().get("email")
    from_addr = "wieszheng@qq.com"
    smtp_server = "smtp.qq.com"
    password = "gudnpniztrxoffje"

    original_str = "uTest"
    try:
        async with aiosmtplib.SMTP(
            hostname=smtp_server, port=465, use_tls=True
        ) as server:
            message = EmailMessage()
            message["From"] = (
                f'"=?UTF-8?B?{base64.b64encode(original_str.encode()).decode()}?=" <{from_addr}>'
            )
            message["To"] = ", ".join(receivers)
            message["Subject"] = subject
            message.add_alternative(html_content, subtype="html")

            await server.login(from_addr, password)
            await server.send_message(message)
    except SMTPDataError as e:
        raise ApiException(
            err_code=10001,
            err_code_des=f"发送邮件失败，请确认邮箱配置是否正确：{e.message}",
        )


if __name__ == "__main__":
    content = render_email_template(
        template_name="verification-email.html",
        context={"code": str(random.randint(100000, 999999))},
    )
    asyncio.run(
        send_mail(
            "验证码",
            ["3248401072@qq.com", "1970690014@qq.com", "wieszheng@qq.com"],
            content,
        )
    )
