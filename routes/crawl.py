#!/usr/bin/python3

"""
Module: crawl_api
Description: FastAPI router for initiating and monitoring crawling tasks.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks.crawl import (celery_worker, crawl_task)


router = APIRouter()


class CrawlRequest(BaseModel):
    """
    Pydantic model for the request body when initiating a crawl task.
    """
    url: str
    max_depth: int


@router.post("/crawl/")
async def crawl(request: CrawlRequest):
    """
    Endpoint to initiate a crawl task.

    Args:
    - request (CrawlRequest): Pydantic model representing the request body.

    Returns:
    - dict: Dictionary containing the task_id.
    """
    result = crawl_task.delay(request.url, request.max_depth)
    task_id = result.id
    return {"task_id": task_id}


@router.get("/crawl/status/{task_id}")
async def get_status(task_id: str):
    """
    Endpoint to retrieve the status and result of a crawling task.

    Args:
    - task_id (str): The task ID.

    Returns:
    - dict: Dictionary containing the task status and result.
    """

    result = AsyncResult(task_id, app=celery_worker)
    return {"status": result.status, "result": result.result}
