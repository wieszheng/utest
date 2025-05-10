# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/4/29 22:45
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import timedelta
from typing import BinaryIO, Iterator

from minio import Minio
from minio.datatypes import Bucket, Object
from minio.error import S3Error
from minio.helpers import ObjectWriteResult
from pydantic import BaseModel


class UploadPart(BaseModel):
    part_number: str
    upload_id: str


class MinioClient:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        *,
        bucket_name: str | None = None,
        secure: bool = False,
    ):
        """
        初始化 Minio 客户端。

        参数：
            endpoint （str）：Minio 服务终端节点。
            access_key （str）：用于鉴权的访问密钥。
            secret_key （str）：用于身份验证的密钥。
            bucket_name （Optional[str]）：要使用的默认存储桶名称。
            secure （bool）：是使用 HTTPS （True） 还是 HTTP （False）。
        """

        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name
        self._client = Minio(
            self._endpoint,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=secure,
        )

    @property
    def client(self) -> Minio:
        """
        获取 Minio 客户端实例。

        返回：
            Minio：Minio 客户端。
        """
        return self._client

    @property
    def bucket_name(self) -> str:
        """
        获取存储桶名称。检查存储桶是否存在，如果不存在，则引发异常。
        返回：
            str：存储桶名称。
        提高：
            AttributeError：如果存储桶名称未设置或不存在。
        """
        if self._bucket_name is None:
            raise AttributeError("Bucket name is not set.")

        if not self.bucket_exists(self._bucket_name):
            raise AttributeError(f"Bucket does not exist: {self._bucket_name}")

        return self._bucket_name

    def bucket_exists(self, bucket_name: str) -> bool:
        """
        检查 Bucket 是否存在。
        参数：
            bucket_name （str）：存储桶的名称。
        返回：
            bool：如果存储桶存在，则为 True，否则为 False。
        """
        return self.client.bucket_exists(bucket_name)

    def file_exists(
        self, filename: str, *, bucket_name: str | None = None, nullable: bool = True
    ) -> bool:
        """
        检查存储桶中是否存在文件。

        参数：
            filename （str）：要检查的文件的名称。
            bucket_name （Optional[str]）：存储桶的名称。默认为默认存储桶。
            nullable （bool）：如果为 True，则在文件不存在时返回 False。如果为 False，则引发异常。
        返回：
            bool：如果文件存在，则为 True，否则为 False。
        提高：
            S3Error：如果文件不存在且可为 null，则为 False。
        """
        bucket_name = bucket_name or self.bucket_name

        try:
            self.client.stat_object(bucket_name=bucket_name, object_name=filename)
            return True
        except S3Error:
            if not nullable:
                raise
            return False

    def presigned_get_url(
        self,
        filename: str,
        *,
        bucket_name: str | None = None,
        nullable: bool = True,
        expires: timedelta = timedelta(days=30),
    ) -> str:
        """
        生成用于下载文件的预签名 URL。

        参数：
            filename （str）：要为其生成 URL 的文件的名称。
            bucket_name （Optional[str]）：存储桶的名称。默认为默认存储桶。
            nullable （bool）：如果为 True，则在生成 URL 之前检查文件是否存在。
             如果为 False，则如果文件不存在，则引发异常。
            expires （timedelta）：预签名 URL 的过期时间。默认值为 30 天。

        返回：
            str：用于访问文件的预签名 URL。

        提高：
            S3Error：如果文件不存在且可为 null，则为 False。
        """
        bucket_name = bucket_name or self.bucket_name
        if not nullable:
            self.file_exists(filename, bucket_name=bucket_name, nullable=False)
        return self.client.presigned_get_object(
            bucket_name=bucket_name, object_name=filename, expires=expires
        )

    def create_multipart_upload(
        self,
        filename: str,
        *,
        bucket_name: str | None = None,
        headers: dict | None = None,
    ) -> str:
        """
        启动文件的分段上传。
        参数：
            filename （str）：要上传的文件的名称。
            bucket_name （Optional[str]）：存储桶的名称。默认为默认存储桶。
            headers （Optional[dict]）：要包含在上传请求中的自定义标头。

        返回：
            str：分段上传的上传 ID。
        """
        bucket_name = bucket_name or self.bucket_name
        headers = headers or {}
        return self.client._create_multipart_upload(
            bucket_name=bucket_name, object_name=filename, headers=headers
        )

    def complete_multipart_upload(
        self,
        filename: str,
        upload_id: str,
        max_parts: int,
        *,
        bucket_name: str | None = None,
    ) -> None:
        """
        通过组合上传的段完成分段上传。

        参数：
            filename （str）：文件的名称。
            upload_id （str）：分段上传的上传 ID。
            max_parts （int）：要列出和完成的零件的最大数量。
            bucket_name （Optional[str]）：存储桶的名称。默认为默认存储桶。
        """
        bucket_name = bucket_name or self.bucket_name
        part_list = self.client._list_parts(
            bucket_name=bucket_name,
            object_name=filename,
            upload_id=upload_id,
            max_parts=max_parts,
        )
        self.client._complete_multipart_upload(
            bucket_name=bucket_name,
            object_name=filename,
            upload_id=upload_id,
            parts=part_list.parts,
        )

    def presigned_put_url(
        self,
        filename: str,
        *,
        bucket_name: str | None = None,
        upload_part: UploadPart | dict[str, str] | None = None,
        expires: timedelta = timedelta(days=2),
    ) -> str:
        """
        生成用于上传文件部分的预签名 URL。

        参数：
            filename （str）：要上传的文件的名称。
            bucket_name （Optional[str]）：存储桶的名称。默认为默认存储桶。
            upload_part （Optional[UploadPart|dict]）：段详细信息（段编号和上传 ID）。
             可以作为字典或 UploadPart 实例提供。
            expires （timedelta）：预签名 URL 的过期时间。默认值为 2 天。

        返回：
            str：用于上传文件一部分的预签名 PUT URL。

        提高：
            AttributeError：如果部件号无效。
        """
        bucket_name = bucket_name or self.bucket_name
        upload_part_map = {}
        if upload_part is not None:
            if isinstance(upload_part, dict):
                upload_part = UploadPart.model_validate(upload_part)

            if int(upload_part.part_number) < 1:
                raise AttributeError(f"Invalid part number: {upload_part.part_number}")

            upload_part_map = upload_part.serializable_dict()

        return self.client.get_presigned_url(
            "PUT",
            bucket_name,
            filename,
            expires=expires,
            extra_query_params=upload_part_map,
        )

    def upload(
        self,
        filename: str,
        data: BinaryIO,
        *,
        length: int = -1,
        content_type: str = "application/octet-stream",
        num_parallel_uploads: int = 3,
        bucket_name: str | None = None,
    ) -> ObjectWriteResult:
        """
        将文件上传到指定的 Minio 存储桶。
        此方法将数据并行上传到存储桶，必要时使用多个段。

        参数：
            filename （str）：Minio 存储桶中对象的名称。
            data （BinaryIO）：包含待上传数据的类文件对象。
            length （int， optional）：需要上传的数据长度。默认值为 -1 （unknown）。
            content_type （str，可选）：对象的内容类型（MIME 类型）。
             默认为 “application/octet-stream”。
            num_parallel_uploads （int， optional）：大型对象的并行上传次数。默认值为 3。
            bucket_name （Optional[str]， optional）：将上传对象的存储桶的名称。
             默认为 None （使用默认存储桶）。

        返回：
            ObjectWriteResult：对象上传作的结果。
        """
        bucket_name = bucket_name or self.bucket_name

        return self.client.put_object(
            bucket_name=bucket_name,
            object_name=filename,
            data=data,
            length=length,
            content_type=content_type,
            part_size=64 * 1024 * 1024,
            num_parallel_uploads=num_parallel_uploads,
        )

    def get_buckets_list(self) -> list[Bucket]:
        """
        检索 Minio 服务器中所有可用存储桶的列表。
        此方法返回表示所有可用存储桶的 Bucket 对象列表。

        返回：
            list[Bucket]：Bucket 对象的列表。
        """
        return self.client.list_buckets()

    def get_objects_list(
        self,
        *,
        bucket_name: str | None = None,
        prefix: str | None = None,
        recursive: bool = False,
    ) -> Iterator[Object]:
        """
        检索 Minio 上指定存储桶中的对象列表。
        此方法允许您列出特定存储桶中的对象，并可选择按前缀和递归进行筛选。

        参数：
            bucket_name （Optional[str]， optional）：存储桶的名称。默认为 None （使用默认存储桶）。
            prefix （Optional[str]， optional）：对象名称的前缀筛选条件。默认为 None。
            recursive （bool， optional）：递归列出而不是目录结构仿真。默认为 False。

        返回：
            Iterator[Object]：存储桶中与提供的参数匹配的对象的迭代器。
        """
        bucket_name = bucket_name or self.bucket_name
        return self.client.list_objects(
            bucket_name=bucket_name, prefix=prefix, recursive=recursive
        )


if __name__ == "__main__":
    _endpoint = "localhost:9000"
    _access_key = "minio"
    _secret_key = "minio123"
    _bucket_name = "test-bucket"
    client = MinioClient(
        _endpoint,
        access_key=_access_key,
        secret_key=_secret_key,
        bucket_name=_bucket_name,
    )
    path = "C:/Users/shwezheng/Downloads/BT2022_R8_216048_Full_x64.exe"
    for item in client.get_objects_list():
        print(item)
