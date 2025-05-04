# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/3 21:30
@Author   : shwezheng
@Software : PyCharm
"""

from enum import Enum
from functools import lru_cache


class Code(Enum):
    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def msg(self) -> str:
        return self.value[1]

    @classmethod
    @lru_cache
    def get_code_msg_dict_cache(cls) -> dict[int, str]:
        return {item.code: item.msg for item in cls}

    @classmethod
    def use_code_get_enum_msg(cls, code: int) -> str:
        mapping = cls.get_code_msg_dict_cache()
        return mapping[code]


class CustomCode(Code):
    HTTP_200 = (200, "请求成功")
    HTTP_201 = (201, "新建请求成功")
    HTTP_202 = (202, "请求已接受，但处理尚未完成")
    HTTP_204 = (204, "请求成功，但没有返回内容")
    HTTP_400 = (400, "错误的请求")
    HTTP_401 = (401, "未经许可授权")
    HTTP_403 = (403, "失败！当前访问没有权限，或操作的数据没权限!")
    HTTP_404 = (404, "请求的地址不存在")
    HTTP_405 = (405, "不允许使用此方法提交访问")
    HTTP_410 = (410, "请求的资源已永久删除")
    HTTP_422 = (422, "请求参数非法")
    HTTP_425 = (425, "无法执行请求，由于服务器无法满足要求")
    HTTP_429 = (429, "请求过多，服务器限制")
    HTTP_500 = (500, "服务器内部错误")
    HTTP_502 = (502, "网关错误")
    HTTP_503 = (503, "服务器暂时无法处理请求")
    HTTP_504 = (504, "网关超时")


class ApiErrorCode(Code):
    # 用户相关错误 10000 - 11000
    WRONG_USER_NAME_OR_PASSWORD = (10001, "账号或者密码错误！😱")
    PARTNER_CODE_EMPLOYEE_FAIL = (10002, "账号错误！🚫")
    WRONG_USER_NAME_OR_PASSWORD_LOCK = (
        10003,
        "密码输入错误超过次数，请5分钟后再登录！😭",
    )
    USERNAME_ALREADY_EXISTS = (10004, "用户名已被注册 🧑‍💻")
    NICKNAME_ALREADY_EXISTS = (10005, "昵称已被注册 🧑‍💻")
    EMAIL_ALREADY_EXISTS = (10006, "邮箱已被注册 📧")
    USER_ID_REQUIRED = (10007, "用户id不能为空 ❌")
    USER_PASSWORD_REQUIRED = (10010, "密码不能为空 🚫")
    PASSWORD_MISMATCH = (10008, "两次输入的密码不一致 🔐")
    CAPTCHA_INCORRECT = (10009, "验证码错误 🔑")
    NEW_PASSWORD_SAME_AS_OLD = (10009, "新密码不能与旧密码相同 🔄")
    OLD_PASSWORD_INCORRECT = (10010, "旧密码错误 ⚠️")
    USER_ACCOUNT_LOCKED = (10011, "用户账号被锁定，请联系管理员 😭")
    USER_CANNOT_EDIT_ADMIN = (10012, "不可操作超级管理员 ⚡")
    USER_CAN_ONLY_EDIT_OWN_INFO = (10013, "只能修改自己的信息呦 👉")

    # 用户权限相关错误 10100 - 10200
    PERMISSION_DENIED = (10100, "没有操作权限，请联系管理员 ⛔")
    ACCESS_DENIED_TO_RESOURCE = (10101, "无权访问该资源 🚫")
    ACTION_NOT_ALLOWED_FOR_ROLE = (10102, "当前角色不允许执行此操作 👮")
    USER_HAS_NO_PERMISSION_TO_PROJECT = (10103, "你没有权限操作该项目 😞")
    PROJECT_OWNER_ONLY_OPERATION = (10104, "仅项目拥有者可操作 🏅")
    ONLY_ADMIN_CAN_MANAGE_ROLES = (10105, "只有管理员可以管理角色 ⚡")
    CANNOT_REMOVE_YOURSELF_FROM_PROJECT = (10106, "不能将自己从项目中移除 🙅‍♂️")
    CANNOT_DELETE_DEFAULT_ROLE = (10107, "默认角色不可删除 ❌")
    ROLE_ASSIGNMENT_FAILED = (10108, "角色分配失败，请重试 🔄")
    CANNOT_EDIT_OWN_PERMISSIONS = (10109, "不能修改自己的权限设置 🚫")
    INSUFFICIENT_PERMISSIONS = (10110, "权限不足，无法完成操作 ⚠️")
    CANNOT_REMOVE_LAST_ADMIN = (10111, "不能删除最后一个管理员 🚫")
    CANNOT_REMOVE_LAST_PROJECT_MEMBER = (10112, "不能删除最后一个项目成员 🚫")

    # 调度器相关错误 20000 - 20100
    SCHEDULER_JOB_ALREADY_EXISTS = (20001, "任务ID已存在，请更换ID 🔄")
    SCHEDULER_TRIGGER_EXPIRED = (20002, "触发器已过期，不会再次执行 ⏳")
    SCHEDULER_RUNNING = (20003, "调度器已在运行中 🚀")
    SCHEDULER_PAUSED_CANNOT_SUBMIT = (20004, "调度器已暂停，无法提交任务 ⛔")
    SCHEDULER_SERIALIZE_JOB_FAILED = (20005, "任务无法序列化，请检查参数或函数路径 🔒")
    SCHEDULER_CUSTOM_TRIGGER_UNSERIALIZABLE = (20006, "自定义触发器不支持序列化 🧱")
    SCHEDULER_JOB_NOT_FOUND = (20007, "任务未找到，请确认任务ID ❌")
    SCHEDULER_EVENT_LOOP_CLOSED = (20008, "事件循环已关闭，无法执行异步任务 💥")
    SCHEDULER_ADD_JOB_FAILED = (20009, "添加任务失败，请检查参数或函数 🛠️")
    SCHEDULER_REMOVE_JOB_FAILED = (20010, "移除任务失败，任务可能不存在或已被移除 🗑️")
    SCHEDULER_PAUSE_JOB_FAILED = (20011, "暂停任务失败，任务可能不存在或已暂停 ⚠️")
    SCHEDULER_RESUME_JOB_FAILED = (20012, "恢复任务失败，任务可能不存在或未暂停 🔁")
