#!/usr/bin/python3

"""
    FastAPI server init
"""

from fastapi import FastAPI
from routes.crawl import router
from s3_client import client
from contextlib import asynccontextmanager
from log import LOGGER as log
from config import S3_BUCKET_NAME


def run_startup():
    response = client.create_bucket(Bucket=S3_BUCKET_NAME)
    if response.get('HTTPStatusCode') == 200:
        log.debug("Created bucket successfully")
    else:
        log.debug("Failed to create bucket")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_startup()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api")
