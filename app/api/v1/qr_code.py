# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/4/23 21:15
@Author   : shwezheng
@Software : PyCharm
"""

from fastapi import Query, APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from amzqr import amzqr
from app.enums.status import QrLevel
import os
import tempfile

router = APIRouter()


@router.post("/")
async def generate_qr_with_upload(
    words: str = Query(..., description="要编码到 QR 码中的文本或 URL"),
    version: int = Query(1, ge=1, le=40, description="QR 码的版本，范围从 1 到 40"),
    level: QrLevel = QrLevel.H,
    colorized: bool = Query(False, description="是否生成彩色 QR 码"),
    contrast: float = Query(1.0, description="图片对比度"),
    brightness: float = Query(1.0, description="图片亮度"),
    picture: UploadFile = File(..., description="用于艺术 QR 码的图片文件"),
):
    file_extension = picture.filename.split(".")[-1].lower()
    save_name = f"qrcode.{file_extension}"
    save_dir = os.getcwd()
    # 确保输出目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 保存上传的图片到临时文件
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=f".{picture.filename.split('.')[-1]}"
    ) as tmp:
        tmp.write(await picture.read())
        tmp_path = tmp.name.lower()

    # 生成 QR 码（有图片）
    _, _, qr_name = amzqr.run(
        words=words,
        version=version,
        level=level.value,
        picture=tmp_path,
        colorized=colorized,
        contrast=contrast,
        brightness=brightness,
        save_name=save_name,
        save_dir=save_dir,
    )

    os.remove(tmp_path)
    return FileResponse(os.path.join(save_dir, qr_name))
