#!/usr/bin/python3

"""
    FastAPI server init
"""

from fastapi import FastAPI
from routes.crawl import router

app = FastAPI()

app.include_router(router, prefix="/api")
