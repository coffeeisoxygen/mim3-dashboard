"""Centralized logging setup - intercept all logging to Loguru"""

from __future__ import annotations

import inspect
import logging
from pathlib import Path
import sys
from typing import TYPE_CHECKING

from loguru import logger
import streamlit as st

from sales_dashboard.config.constant import (
    LOG_COMPRESSION,
    LOG_DIRECTORY,
    LOG_FILENAME,
    LOG_LEVEL_DEBUG,
    LOG_RETENTION_DAYS,
    LOG_ROTATION_SIZE,
)
from sales_dashboard.config.messages import (
    LOG_ALREADY_INITIALIZED,
    LOG_DEBUG_ENABLED,
    LOG_PRODUCTION_ENABLED,
    LOG_SETUP_COMPLETE,
    LOG_STARTING_INITIALIZATION,
)

if TYPE_CHECKING:
    pass


class InterceptHandler(logging.Handler):
    """Intercept standard logging and redirect to Loguru"""

    def emit(self, record: logging.LogRecord) -> None:
        """Redirect standard logging records to Loguru"""
        # Get corresponding Loguru level if it exists
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(debug: bool = True) -> None:
    """Setup centralized logging - once per session (consistent with database pattern)"""

    # Check if already initialized this session
    if st.session_state.get("logging_initialized", False):
        logger.debug(LOG_ALREADY_INITIALIZED)
        return

    try:
        logger.info(LOG_STARTING_INITIALIZATION)

        # CRITICAL: Remove existing handlers first
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Remove default Loguru handler
        logger.remove()

        # Define consistent log format
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<magenta>{function}</magenta>:<red>{line}</red> - "
            "<level>{message}</level>"
        )

        if debug:
            # Debug mode: Console output with colors
            logger.add(
                sys.stderr,
                level=LOG_LEVEL_DEBUG,
                format=log_format,
                diagnose=True,
                colorize=True,
                backtrace=True,
            )
            logger.info(LOG_DEBUG_ENABLED)
        else:
            # Production mode: File output
            Path(LOG_DIRECTORY).mkdir(parents=True, exist_ok=True)
            logger.add(
                f"{LOG_DIRECTORY}/{LOG_FILENAME}",
                rotation=LOG_ROTATION_SIZE,
                retention=LOG_RETENTION_DAYS,
                level="INFO",
                format=log_format,
                diagnose=True,
                enqueue=True,
                backtrace=True,
                catch=True,
                compression=LOG_COMPRESSION,
                serialize=False,
            )
            logger.info(LOG_PRODUCTION_ENABLED)

        # Intercept ALL logging - this must be aggressive
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=logging.DEBUG,  # Capture everything
            force=True,
        )

        # Mark as initialized for this session
        st.session_state.logging_initialized = True
        logger.info(LOG_SETUP_COMPLETE)

    except Exception as e:
        # Fallback - don't break app if logging fails
        print(f"Logging setup failed: {e}")
        raise
