#!/usr/bin/python3
"""
Module: tasks
Description: Celery tasks for web crawling and related functionalities.
"""

import celery

from crawler import start_crawl_worker
from log import LOGGER as log
from s3_client import upload_file_object_to_s3, get_presigned_s3_link
from config import S3_BUCKET_NAME

celery_worker = celery.Celery(
    "tasks",
    broker="redis://redis/0",
    backend="redis://redis/0",
    include=["tasks.crawl"],
)


@celery_worker.task(name="crawl_task")
def crawl_task(url, depth):
    """
    Celery task for initiating a web crawl, uploading results to S3,
    and returning a presigned link to the S3 file.

    Args:
    - url (str): The starting URL for crawling.
    - depth (int): The depth to which the crawler should explore.

    Returns:
    - dict: Dictionary containing the presigned S3 link.
    """
    log.info("Picked up crawl task")
    file_bytes, file_name = start_crawl_worker(url, depth)
    upload_file_object_to_s3(file_bytes, S3_BUCKET_NAME, file_name)
    params = {"Bucket": S3_BUCKET_NAME, "Key": file_name}
    res = get_presigned_s3_link("get_object", params=params, expiration=30000)
    return {"s3_link": res}


celery_worker.conf.task_routes = {
    "tasks.crawl.crawl_task": "tasks",
}
