#!/usr/bin/python3
# pylint: disable=E0401


"""
This module contains utility functions such as time calculation and random float generation, # noqa
along with decorators for measuring execution time.
"""
from functools import wraps
import time

import random
from log import LOGGER as log


def time_calculator(func):
    """
    Decorator to measure the execution time of a function.

    Args:
    - func: The function to be decorated.   # noqa

    Returns:
    - wrapper: The wrapped function.

    The decorator measures the execution time of the given function by recording the start time
    before the function call and the end time after the function call. It logs the elapsed time
    using the 'log' module and returns the result of the original function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function
        """
        start_time = time.time()
        val = func(*args, **kwargs)
        end_time = time.time()
        log.debug(f"Elapsed time: {end_time-start_time}")
        return val

    return wrapper


def get_random_float(low: int, high: int) -> float:
    """
    Returns a random floating-point number within the range [low, high).

    Args:
    - low (int): The lower boundary of the range (inclusive).
    - high (int): The upper boundary of the range (exclusive).

    Returns:
    - float: A random float within the specified range [low, high).
    """
    return random.uniform(low, high)
