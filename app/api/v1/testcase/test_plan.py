# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/3/22 02:55
@Author   : shwezheng
@Software : PyCharm
"""

import time

from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter

from app.core.scheduler import scheduler

router = APIRouter()


def demo_task(a1: str):
    print(a1, time.time())


@router.post("/jobs/")
async def create_job(plan_id: str, plan_name: str, cron: str):
    scheduler.add_job(
        func=demo_task,
        args=(plan_id,),
        trigger=CronTrigger.from_crontab(cron),
        id=str(plan_id),
        name=plan_name,
    )
    return True


@router.delete("/jobs/")
async def remove_job(plan_id: str):
    scheduler.remove_job(plan_id)
    return True


@router.put("/jobs/")
async def update_job(plan_id: str, cron: str):
    job = scheduler.get_job(str(plan_id))
    if job:
        job.remove()

    scheduler.add_job(
        func=demo_task,
        args=(plan_id,),
        trigger=CronTrigger.from_crontab(cron),
        id=str(plan_id),
        name=job.name,
    )
    return True


@router.put("/jobs/pause/")
async def pause_job(plan_id: str):
    job = scheduler.get_job(str(plan_id))
    if job:
        job.pause()
    return True


@router.get("/jobs/")
async def list_jobs():
    jobs = scheduler.get_jobs()
    data = []
    for job in jobs:
        data.append(
            {
                "job_id": job.id,
                "func_name": job.func_ref,
                "func_args": job.args,
                "cron_model": str(job.trigger),
                "next_run": str(job.next_run_time),
            }
        )
    return data
