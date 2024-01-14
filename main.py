#!/usr/bin/python3
# pylint: disable=E0401

"""
    Module: main
    Description: FastAPI application configuration and startup logic.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.crawl import router
from s3_client import s3_client
from log import LOGGER as log
from config import S3_BUCKET_NAME


def run_startup():
    """
    Run startup logic for the FastAPI application, such as creating an S3 bucket. # noqa
    """
    response = s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
    if response.get("HTTPStatusCode") == 200:
        log.debug("Created bucket successfully")
    else:
        log.debug("Failed to create bucket")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for managing the lifespan of the FastAPI application.

    Args:
    - app (FastAPI): The FastAPI application.
    # noqa
    Yields:
    - None

    Runs the startup logic when entering the context and performs cleanup when exiting.
    """
    run_startup()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")
