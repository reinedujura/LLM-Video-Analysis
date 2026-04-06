"""
Logging configuration following logging standards.

Sets up structured logging for the application.
"""

import logging
import logging.config
from typing import Dict, Any

from app.core.config import get_settings


def configure_logging() -> None:
    """
    Configure application logging.

    Sets up logging format, level, and handlers based on settings.
    """
    settings = get_settings()

    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": settings.LOG_FORMAT,
            },
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - "
                    "%(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
        },
        "loggers": {
            "app": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Name of logger (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
