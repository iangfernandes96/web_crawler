#!/usr/bin/python3
# pylint: disable=E0401


"""
WebCrawler Module

This module defines a WebCrawler class that facilitates asynchronous web page
crawling, fetches links from HTML content, and calculates same-domain link
ratios.
It utilizes aiohttp for asynchronous HTTP requests and lxml for HTML parsing.

Classes:
    - WebCrawler: A class for crawling web pages asynchronously and extracting
                  information.

Usage:
    To use the WebCrawler class:
    1. Create an instance of WebCrawler.
    2. Use the crawl method to start crawling from a given URL to a specified
       depth.

Example:
    # Instantiate the WebCrawler
    crawler = WebCrawler()

    # Start crawling from a URL up to a depth and write output to a file
    asyncio.run(crawler.crawl('https://example.com', 1, 3, output_file))
"""

from urllib.parse import urlparse, urljoin
from typing import Optional, Coroutine

import asyncio
import aiohttp
import aiofiles as aiof
from aiohttp import ClientSession, ClientError, InvalidURL, ClientTimeout
from asyncio import TimeoutError
from lxml import html
from config import DEFAULT_URL_PROTOCOL, DEFAULT_RETRY_COUNT, DEFAULT_BACKOFF
from utils import get_random_float
from log import LOGGER as log


class WebCrawler:
    """
    WebCrawler Class

    This class implements asynchronous web page crawling, link extraction, and
    same-domain link ratio calculation functionalities.
    It uses aiohttp for asynchronous HTTP requests and lxml for HTML parsing.

    Attributes:
        fetched_urls (set): A set containing visited URLs during crawling.
        timeout (ClientTimeout): A ClientTimeout object, used for setting
                                 request timeouts.

    Methods:
        - add_protocol(url: str, protocol: str = DEFAULT_URL_PROTOCOL) -> str: # noqa
            Adds a protocol (HTTP/HTTPS) to a URL if not specified.
        - fetch_page_async(session: ClientSession, url: str) -> Optional[bytes]:
            Asynchronously fetches content of a web page using an HTTP GET request.
        - fetch_links(html_content: bytes, base_url: str) -> set[str]:
            Extracts links from HTML content given a base URL.
        - calculate_same_domain_ratio(current_url: str, links: set) -> float:
            Calculates the ratio of same-domain links to total links.
        - crawl(url: str, depth: int, max_depth: int, output_file: TextIO) -> Optional[Coroutine]:
            Crawls through web pages starting from a given URL up to a specified depth,
            extracting information and writing results to an output file.

    Usage:
        1. Instantiate the WebCrawler class.
        2. Use the crawl method to start crawling from a URL to a specified depth.
        3. Implement additional functionalities as required.

    Example:
        # Instantiate the WebCrawler
        crawler = WebCrawler()

        # Start crawling from a URL up to a depth and write output to a file
        asyncio.run(crawler.crawl('https://example.com', 1, 3, output_file))
    """

    __slots__ = ("fetched_urls", "timeout",)

    def __init__(self) -> None:
        self.fetched_urls = set()
        self.timeout = ClientTimeout(connect=5,
                                     total=15)

    def add_protocol(
        self, url: str, protocol: str = DEFAULT_URL_PROTOCOL
    ) -> str:
        """
        Adds a protocol (HTTP/HTTPS) to the provided URL if no protocol
        is specified. Returns the modified URL with the added protocol.

        Args:
        - url (str): The URL to which the protocol will be added.
        - protocol (str, optional): The protocol to be added if
        the URL lacks a protocol. Defaults to 'https'.

        Returns:
        - str: The URL with the added protocol.
        """
        parsed_url = urlparse(url)
        if not parsed_url.scheme and not parsed_url.netloc:
            return f"{protocol}://{url}"
        return url

    async def fetch_page_async(
        self, session: ClientSession, url: str
    ) -> Optional[bytes]:
        """
        Asynchronously fetches the content of a web page given its URL
        using an HTTP GET request.

        Args:
        - session (ClientSession): The aiohttp ClientSession to use for
                                   making the request.
        - url (str): The URL of the web page to fetch.

        Returns:
        - Optional[bytes]: The content of the web page as bytes if
                           the request is successful (status code 200).
                           Returns None if there's an error or if the
                           status code is not 200.
        """
        retry_count = DEFAULT_RETRY_COUNT
        backoff = DEFAULT_BACKOFF

        while retry_count > 0:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.read()
                    return None
            except InvalidURL:
                log.error(f"Invalid URL for crawling: {url}")
                return None
            except TimeoutError:
                log.error(f"Request timed out for url {url}")
            except ClientError as ex:
                log.exception(f"HTTP Client error: {ex}")

            delay_with_jitter = backoff + get_random_float(0, 1)
            await asyncio.sleep(delay_with_jitter)
            backoff *= 2
            retry_count -= 1

        log.debug("Failed after multiple retries")
        return None

    def fetch_links(self, html_content: bytes, base_url: str) -> set[str]:
        """
        Fetches links from HTML content given a base URL.

        Args:
        - html_content (bytes): The HTML content from which links are to
                                be extracted.
        - base_url (str): The base URL used to resolve relative links.

        Returns:
        - Set[str]: A set of absolute URLs derived from the HTML content.
        """

        try:
            tree = html.fromstring(html_content)
            links = tree.xpath("//a/@href")
            links = [urljoin(base_url, link) for link in links]
            return set(links)
        except Exception as e:
            log.exception(f"Error extracting links: {e}")
            return set()

    def calculate_same_domain_ratio(self, current_url: str, links: set) -> float:  # noqa
        """
        Calculates the ratio of same-domain links in comparison to the
        total links provided.

        Args:
        - current_url (str): The URL of the current page.
        - links (Set[str]): A set of URLs to calculate the same-domain
                            ratio.

        Returns:
        - float: The ratio of same-domain links to the total number of
                 links.
        Returns 0.0 if the input set of links is empty.
        """

        current_domain = urlparse(current_url).netloc
        same_domain_count = sum(
            urlparse(link).netloc == current_domain for link in links
        )  # noqa
        return round(same_domain_count / len(links), 2) if len(links) > 0 else 0.0  # noqa

    async def write_to_file(self, output_file: str, content: str) -> None:
        async with aiof.open(output_file, 'a', encoding='utf-8') as file:
            await file.write(content)

    async def crawl(
        self, url: str, depth: int, max_depth: int, output_file: str
    ) -> Optional[Coroutine]:
        """
        Crawls through web pages starting from a given URL up to a
        specified depth, extracting information and writing results to an
        output file.

        Args:
        - url (str): The starting URL for crawling.
        - depth (int): The current depth in the crawling tree.
        - max_depth (int): The maximum depth to which the crawler should
                           explore.
        - output_file (TextIO): An open file handler to write the output
                                data.

        Returns:
        - Optional[Coroutine]: Returns None if the depth exceeds the
                               max_depth or if the URL has been visited
                               before.

        Note:
        - The function uses an asynchronous approach for web page crawling.
        """

        if depth > max_depth or url in self.fetched_urls:
            return

        self.fetched_urls.add(url)

        async with aiohttp.ClientSession() as session:
            try:
                html_content = await self.fetch_page_async(session, url)
            except Exception as e:
                log.exception(f"Failed to crawl: {url}, with exception: {e}")
                return

            if html_content:
                links = self.fetch_links(html_content, url)
                same_domain_ratio = self.calculate_same_domain_ratio(url, links)  # noqa

                output_content = f"{url}\t{depth}\t{same_domain_ratio}\n"
                await self.write_to_file(output_file, output_content)

                tasks = [
                    self.crawl(link, depth + 1, max_depth, output_file)
                    for link in links
                ]
                await asyncio.gather(*tasks)
