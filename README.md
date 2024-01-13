# WebCrawler

## Overview

This Python-based web crawler explores web pages up to a specified depth, extracting information and recording results in an output file. It utilizes asynchronous methods for efficient crawling.

## Components

1. **WebCrawler Class**: The core component responsible for managing the crawling process. It tracks visited URLs, fetches web pages asynchronously, extracts links, and calculates same-domain ratios.

2. **Utils Module**: Contains utility functions used in the crawler. The `time_calculator` decorator measures the time taken by functions, and `get_random_float` generates random floats within a specified range.

3. **Config Module**: Holds configuration parameters for the crawler, such as the default URL protocol, output file name, retry count, backoff time, etc.

4. **Log Module**: Implements a logging handler (`LogHandler`) and provides a logger object (`LOGGER`) for consistent and structured logging throughout the application.

5. **Main Script (crawler.py)**: The entry point of the application. It initializes the crawler, sets up the necessary configurations, and starts the crawling process.


## Features

- **Asynchronous Crawling**: Utilizes `aiohttp` and `asyncio` for asynchronous web page crawling.
- **Depth Control**: Allows crawling up to a specified depth.
- **Same Domain Ratio**: Calculates the ratio of same-domain links for each page.
- **Retry Mechanism**: Implements retries with an exponential backoff for robustness against network issues.
- **Logging**: Uses Python's `logging` module for log handling.
- **Configurability**: Easily configurable with `config.py` for parameters like protocol, output file, retries, and more.

## Installation

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the crawler:

    ```bash
    python crawler.py <URL> <depth>
    ```

    Example:

    ```bash
    python crawler.py https://example.com 3
    ```

    - `<URL>`: Starting URL for crawling.
    - `<depth>`: Depth to which the crawler should explore.

2. Results will be written to `output.tsv` by default.

## Configuration

Modify `config.py` to adjust parameters like URL protocol, output file name, retry count, and backoff time.

## Logging

Logs are written to `app.log` by default. Adjust logging settings in `log.py` as needed.


## Note

Used `black` and `pylint` for formatting and linting.
