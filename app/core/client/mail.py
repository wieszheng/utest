# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/4/30 10:51
@Author   : shwezheng
@Software : PyCharm
"""

import base64
import json
import os
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from jinja2 import Template

from config import ROOT


def get_config():
    try:
        file_path = os.path.join(ROOT, "config.json")
        if not os.path.exists(file_path):
            raise Exception("没有找的配置文件，请假查")
        with open(file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"获取系统设置失败，{e}")


def render_html(filepath: str, **kwargs) -> str:
    with open(filepath, encoding="utf-8") as f:
        html_str = Template(f.read())
        return html_str.render(**kwargs)


async def send_mail(subject: str, content_msg: str, *recipient) -> None:
    data = get_config().get("email")
    from_addr = data.get("from_addr")
    smtp_server = data.get("smtp_server")
    password = data.get("password")

    original_str = "uTest 机器人"
    encoded_bytes = original_str.encode("utf-8")
    base64_encoded_str = base64.b64encode(encoded_bytes)

    msg = MIMEMultipart("mixed")
    msg["From"] = Header(
        f'"=?UTF-8?B?{base64_encoded_str.decode("utf-8")}?=" <{from_addr}>'
    )
    msg["To"] = Header("其他同学")
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(content_msg, "html", "utf-8"))

    try:
        server = aiosmtplib.SMTP(hostname=smtp_server, port=465, use_tls=True)
        await server.connect()
        await server.login(from_addr, password)
        await server.sendmail(from_addr, [from_addr, *recipient], msg.as_string())
        await server.quit()
    except Exception as e:
        raise Exception(f"发送测试报告邮件失败：{e}")
