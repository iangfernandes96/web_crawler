#!/usr/bin/python3

from fastapi import APIRouter
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks.crawl import celery_worker, crawl_task, simple_task


router = APIRouter()


class CrawlRequest(BaseModel):
    url: str
    max_depth: int


@router.post("/crawl/")
async def crawl(request: CrawlRequest):
    result = crawl_task.delay(request.url, request.max_depth) # noqa
    task_id = result.id
    return {'task_id': task_id}


@router.post("/simple/")
async def simple():
    result = simple_task.delay()
    task_id = result.id
    return {'task_id': task_id}


@router.get("/crawl/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_worker)
    return {"status": result.status, "result": result.result}
