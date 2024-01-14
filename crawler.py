#!/usr/bin/python3
# pylint: disable=E0401


"""
Script to run a web crawler.

This script initiates web crawling from a provided URL up to a specified depth.
It utilizes the WebCrawler class to perform crawling tasks asynchronously.

To execute the script, provide the URL and depth as command-line arguments.

Usage: python crawler.py <URL> <depth>
Example: python crawler.py https://example.com 3
"""

import asyncio
import sys
from web_crawler import WebCrawler
from config import OUTPUT_FILE
from log import LOGGER as log
from io import BytesIO


# @time_calculator
def start_crawl(url: str, depth: int) -> None:
    """
    Initiates web crawling from a specified URL up to a given depth.

    Args:
    - url (str): The starting URL for crawling. # noqa
    - depth (int): The depth to which the crawler should explore.

    Returns:
    - None

    This function initializes a WebCrawler object, sets up the necessary parameters,
    and runs the crawling process using asyncio. It writes the output to a specified
    file asynchronously and logs the number of URLs traversed during the process.
    """
    crawler = WebCrawler()
    url = crawler.add_protocol(url)
    log.info(f"Starting crawl for URL: {url}")

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as output_file:
        output_file.write("url\tdepth\tratio\n")

    asyncio.run(crawler.crawl(url, 1, depth, OUTPUT_FILE))

    log.debug(f"Number of URLs traversed: {len(crawler.fetched_urls)}")


def start_crawl_bytes(url: str, depth: int):
    crawler = WebCrawler()
    url = crawler.add_protocol(url)

    output_file_bytes = BytesIO()
    output_file_bytes.write("url\tdepth\tratio\n".encode('utf-8'))

    asyncio.run(crawler.crawl_bytes(url, 1, depth, output_file_bytes))
    log.debug(f"Number of URLs traversed: {len(crawler.fetched_urls)}")
    content_bytes = output_file_bytes.getvalue()
    return {'total_length': len(content_bytes)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        log.error("Usage: python crawler.py <URL> <depth>")
        sys.exit(1)

    root_url = sys.argv[1]
    depth_limit = int(sys.argv[2])
    start_crawl(root_url, depth_limit)
