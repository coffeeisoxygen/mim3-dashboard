"""Centralized logging setup - intercept all logging to Loguru"""

from __future__ import annotations

import inspect
import logging
from pathlib import Path
import sys
from typing import TYPE_CHECKING

from loguru import logger
import streamlit as st

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
        logger.debug("Logging already initialized this session - skipping")
        return

    try:
        logger.info("Starting logging initialization...")

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
                level="DEBUG",
                format=log_format,
                diagnose=True,
                colorize=True,
                backtrace=True,
            )
            logger.info("Debug logging enabled (console output via Loguru)")
        else:
            # Production mode: File output
            Path("logs").mkdir(parents=True, exist_ok=True)
            logger.add(
                "logs/sdp_dashboard.log",
                rotation="1 MB",
                retention="7 days",
                level="INFO",
                format=log_format,
                diagnose=True,
                enqueue=True,
                backtrace=True,
                catch=True,
                compression="zip",
                serialize=False,
            )
            logger.info("Production logging enabled (file output via Loguru)")

        # Intercept ALL logging - this must be aggressive
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=logging.DEBUG,  # Capture everything
            force=True,
        )

        # Mark as initialized for this session
        st.session_state.logging_initialized = True
        logger.info(
            "Centralized logging setup complete - all logs route through Loguru"
        )

    except Exception as e:
        # Fallback - don't break app if logging fails
        print(f"Logging setup failed: {e}")
        raise
