"""
Logger utility
Author: Gabriel Demetrios Lafis

Configures a logger with a consistent format. Guards against
adding duplicate handlers when called multiple times.
"""

import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create or retrieve a logger with a standard format.

    If the logger already has handlers (e.g. from a previous call),
    it is returned as-is to prevent duplicate log lines.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
