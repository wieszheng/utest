# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/2 21:31
@Author   : shwezheng
@Software : PyCharm
"""

import unittest
from fastapi.testclient import TestClient
from faker import Faker
from app.api.v1.users import router


fake = Faker()
client = TestClient(router)


class TestUserAPI(unittest.TestCase):
    def setUp(self):
        """在每个测试前运行，可以用于准备测试数据或初始化环境"""
        pass

    def test_create_user_success(self):
        """测试创建用户的成功场景"""
        user_data = {
            "username": fake.name(),
            "password_hash": "password123",
            "email": fake.email(),
        }

        response = client.post("/users/", json=user_data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # 验证返回中包含 data 字段
        self.assertIn("data", response_data)

        # 验证返回的用户数据是否与输入一致
        user_response = response_data["data"]
        self.assertEqual(user_response["username"], user_data["username"])
        self.assertEqual(user_response["email"], user_data["email"])


if __name__ == "__main__":
    unittest.main()
