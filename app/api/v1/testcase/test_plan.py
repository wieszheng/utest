# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 02:55
@Author   : shwezheng
@Software : PyCharm
"""

import time
from datetime import datetime
from typing import List

from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Path

from app.core.scheduler import scheduler
from app.schemas.common import ResponseModel
from app.schemas.test_plan import TaskJob, CronJob, IntervalJob, DateJob

router = APIRouter()


def print_task(text: str):
    print(text, time.time(), end=" ")
    print("This is a sync task print test")


async def print_async_task(text: str):
    print(text, time.time(), end=" ")
    print("This is a async task print test")


@router.get(
    "/jobs", summary="获取任务列表", response_model=ResponseModel[List[TaskJob]]
)
async def list_jobs() -> ResponseModel[List[TaskJob]]:
    jobs = scheduler.get_jobs()
    job_list = []
    for job in jobs:
        job_list.append(
            TaskJob(
                **{
                    "id": job.id,
                    "name": job.name,
                    "trigger": str(job.trigger),
                    "func_name": job.func_ref,
                    "executor": job.executor,
                    "coalesce": job.coalesce,
                    "max_instances": job.max_instances,
                    "misfire_grace_time": job.misfire_grace_time,
                    "next_run_time": job.next_run_time,
                }
            )
        )
    return ResponseModel(data=job_list)


@router.get("/{job}", summary="获取任务详情")
async def get_task(
    job: str = Path(..., description="任务ID"),
) -> ResponseModel[TaskJob]:
    job = scheduler.get_job(job_id=job)
    if not job:
        raise Exception("任务不存在")

    job_info = TaskJob(
        **{
            "id": job.id,
            "name": job.name,
            "trigger": str(job.trigger),
            "func_name": job.func_ref,
            "executor": job.executor,
            "coalesce": job.coalesce,
            "max_instances": job.max_instances,
            "misfire_grace_time": job.misfire_grace_time,
            "next_run_time": job.next_run_time,
        }
    )
    return ResponseModel(data=job_info)


@router.post("/job", summary="添加任务")
async def create_job(plan_id: str, plan_name: str, cron: str) -> ResponseModel:
    job = scheduler.add_job(
        func=print_task,
        args=(plan_id,),
        trigger=CronTrigger.from_crontab(cron),
        id=str(plan_id),
        name=plan_name,
    )
    return ResponseModel(data=job.id)


@router.post("/cron", summary="添加 corn 任务")
async def add_cron_task(job: CronJob) -> ResponseModel:
    job = scheduler.add_job(
        **job.model_dump(),
        args=("add_cron_task",),
    )
    return ResponseModel(data=job.id)


@router.post("/interval", summary="添加 interval 任务")
async def add_interval_task(job: IntervalJob) -> ResponseModel:
    job = scheduler.add_job(**job.model_dump(), args=("add_cron_task",))
    return ResponseModel(data=job.id)


@router.post("/date", summary="添加 date 任务")
async def add_date_task(job: DateJob) -> ResponseModel:
    job = scheduler.add_job(**job.model_dump(), args=("add_cron_task",))
    return ResponseModel(data=job.id)


@router.put("/job", summary="修改任务")
async def update_job(plan_id: str, cron: str) -> ResponseModel:
    job = scheduler.get_job(str(plan_id))
    if job:
        job.remove()

    job = scheduler.add_job(
        func=print_task,
        args=(plan_id,),
        trigger=CronTrigger.from_crontab(cron),
        id=str(plan_id),
        name=job.name,
    )
    return ResponseModel(data=job.id)


@router.put("/{plan_id}/pause", summary="暂停任务")
async def pause_job(plan_id: str = Path(..., description="任务ID")) -> ResponseModel:
    job = scheduler.get_job(job_id=plan_id)
    if job:
        job.pause()
    return ResponseModel(data=job.id)


@router.post("/{plan_id}/resume", summary="恢复任务")
async def resume_job(plan_id: str = Path(..., description="任务ID")) -> ResponseModel:
    job = scheduler.get_job(job_id=plan_id)
    if job:
        job.resume()
    return ResponseModel(data=plan_id)


@router.post("/{plan_id}/stop", summary="删除任务")
async def delete_task(plan_id: str = Path(..., description="任务ID")) -> ResponseModel:
    job = scheduler.get_job(job_id=plan_id)
    if job:
        job.remove()
    return ResponseModel(data=plan_id)


@router.post("/{plan_id}/run", summary="执行任务")
async def run_task(plan_id: str = Path(..., description="任务ID")) -> ResponseModel:
    task = scheduler.get_job(job_id=plan_id)
    if not task:
        raise Exception("任务不存在")
    task = scheduler.modify_job(job_id=plan_id, next_run_time=datetime.now())
    return ResponseModel(data=task.id)
