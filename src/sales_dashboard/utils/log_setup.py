# log_setup.py
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import streamlit as st
from loguru import logger

if TYPE_CHECKING:
    pass


@st.cache_resource
def setup_logging(debug: bool = True) -> None:
    """Setup logging with Streamlit cache to prevent re-initialization"""
    logger.remove()  # Remove the default logger

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>{name}</yellow>:<magenta>{function}</magenta>:<red>{line}</red> - "
        "<level>{message}</level>"
    )

    if debug:
        logger.add(
            sys.stderr,
            level="DEBUG",
            format=log_format,
            diagnose=True,
            colorize=True,
            backtrace=True,
        )
        logger.info("Debug logging enabled (console output)")
    else:
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        logger.add(
            "logs/sdp_dashboard.log",
            rotation="1 MB",
            retention="7 days",
            level="INFO",  # Production should be INFO, not DEBUG
            format=log_format,
            diagnose=True,
            enqueue=True,
            backtrace=True,
            catch=True,
            compression="zip",
            serialize=False,
        )
        logger.info("Production logging enabled (file output)")
