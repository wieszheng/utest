# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/5/2 18:16
@Author   : shwezheng
@Software : PyCharm
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator, FutureDatetime


class TaskJob(BaseModel):
    id: str
    name: str
    trigger: str
    func_name: str
    executor: str
    coalesce: bool
    max_instances: int
    misfire_grace_time: int
    next_run_time: datetime | None

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
    )


class AddJobBase(BaseModel):
    func: str = Field(default="app.api.v1.testcase.test_plan:print_task")
    id: str | None = None
    name: str | None = None
    next_run_time: datetime | None = None


class CronJob(AddJobBase):
    trigger: Literal["cron"] = Field(default="cron", frozen=True)
    year: str = Field(default="*", pattern=r"^(\*|\d{4})")
    month: str = Field(default="*", pattern=r"^(\*|(?:[1-9]$|1[012]$))")
    day: str = Field(default="*", pattern=r"^(\*|(?:[1-9]$|([12][0-9])$|3[01]$))")
    day_of_week: str = Field(default="*", pattern=r"^(\*|([0-6]$))")
    hour: str = Field(default="*", pattern=r"^(\*|(?:[0-9]$|1[0-9]$|2[0-3]$))")
    minute: str = Field(default="*", pattern=r"^(\*|(?:[0-9]$|([1-5][0-9]$)))")
    second: str = Field(default="0", pattern=r"^(\*|(?:[0-9]$|([1-5][0-9]$)))")


class IntervalJob(AddJobBase):
    trigger: Literal["interval"] = Field(default="interval", frozen=True)
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    @model_validator(mode="after")
    def check_interval_times(self) -> "IntervalJob":
        if not any(
            [
                i != 0
                for i in [self.seconds, self.minutes, self.hours, self.days, self.weeks]
            ]
        ):
            raise ValueError("必须添加至少一个间隔时间")
        return self


class DateJob(BaseModel):
    func: str = Field(default="app.api.v1.testcase.test_plan:print_task")
    id: str | None = None
    name: str | None = None
    trigger: Literal["date"] = Field(default="date", frozen=True)
    run_date: FutureDatetime
