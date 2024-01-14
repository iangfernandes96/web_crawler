#!/usr/bin/python3
import celery

from crawler import start_crawl_bytes
from log import LOGGER as log

celery_worker = celery.Celery(
    "tasks",
    broker="redis://redis/0",
    backend="redis://redis/0",
    include=["tasks.crawl"],
)


@celery_worker.task(name="crawl_task")
def crawl_task(url, depth):
    log.info("Picked up crawl task")
    res = start_crawl_bytes(url, depth)
    return {"status": "done", **res}


@celery_worker.task(name="simple_task")
def simple_task():
    log.info("Simple task")
    print("Completed simple task")
    return {"status": "done"}


celery_worker.conf.task_routes = {
    "tasks.crawl.crawl_task": "tasks",
    "tasks.crawl.simple_task": "tasks",
}
# celery_worker.conf.update(task_track_started=True)

# celery_worker.autodiscover_tasks(["tasks.crawl"])
