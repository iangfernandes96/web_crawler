#!/usr/bin/python3

"""
This module provides utilities and components for web crawling.
"""

from .utils import time_calculator, get_random_float
from .web_crawler import WebCrawler
from .config import (
    DEFAULT_URL_PROTOCOL,
    OUTPUT_FILE,
    DEFAULT_RETRY_COUNT,
    LOG_FILE,
    DEFAULT_BACKOFF,
)
from .log import LOGGER

__all__ = [
    "time_calculator",
    "get_random_float",
    "WebCrawler",
    "DEFAULT_URL_PROTOCOL",
    "OUTPUT_FILE",
    "DEFAULT_RETRY_COUNT",
    "LOG_FILE",
    "LOGGER",
    "DEFAULT_BACKOFF",
]
