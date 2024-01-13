#!/usr/bin/python3
# pylint: disable=E0401

"""
Module for managing logging configurations.

This module provides a LogHandler class responsible for creating and configuring a logger # noqa
with file handling, log level settings, and a specified log format.

It contains the LogHandler class, which offers a method to retrieve a configured logger object
with a specified log file.

Example:
    # Import LogHandler class
    from log_handler import LogHandler

    # Get a logger with default log file
    logger = LogHandler().get_logger()
    logger.info('Logging information message')
"""

import logging

from config import LOG_FILE

DEFAULT_LOG_MODE = logging.DEBUG

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class LogHandler:
    # pylint: disable=R0903
    """
    A class responsible for creating and configuring a logger.

    This class allows the creation of a logger object with file handling, log level settings, # noqa
    and a specified log format.

    Attributes:
        _logger (Logger): A logger object for handling logs.

    Methods:
        get_logger(log_file: str = LOG_FILE) -> Logger:
            Retrieves the configured logger object with the specified log file.

    Usage:
        1. Import the LogHandler class.
        2. Use get_logger to obtain the configured logger.

    Example:
        # Get the logger with default log file
        logger = LogHandler().get_logger()
        logger.info('Logging information message')
    """

    _logger = None

    @classmethod
    def get_logger(cls, log_file=LOG_FILE):
        """
        Retrieves a configured logger object.

        Args:
            log_file (str): Optional. The file to write logs to. Defaults to
                            LOG_FILE.

        Returns:
            Logger: The configured logger object.
        """
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
            cls._logger.setLevel(DEFAULT_LOG_MODE)

            # Create a file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(DEFAULT_LOG_MODE)

            # Create a log format
            formatter = logging.Formatter(LOG_FORMAT)
            file_handler.setFormatter(formatter)

            # Add the handlers to the logger
            cls._logger.addHandler(file_handler)

        return cls._logger


LOGGER = LogHandler().get_logger()
