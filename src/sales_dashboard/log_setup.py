import os
import sys

from loguru import logger


def setup_logging(debug: bool = True):
    logger.remove()  # Remove the default logger

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>{name}</yellow>:<magenta>{function}</magenta>:<red>{line}</red> - "
        "<level>{message}</level>"
    )

    if debug:
        logger.add(
            sys.stderr,  # Log to standard error
            level="DEBUG",  # Set the logging level to DEBUG
            format=log_format,  # Improved log format
            diagnose=True,  # Enable diagnostic information
            colorize=True,  # Enable colorized output in the console
            backtrace=True,  # Enable backtrace for better
        )
    else:
        # Pastikan folder logs/ ada sebelum logging ke file
        os.makedirs("logs", exist_ok=True)
        logger.add(
            "logs/sdp_dashboard.log",  # Log file path
            rotation="1 MB",  # Rotate log files when they reach 1 MB
            retention="7 days",  # Keep logs for 7 days
            level="DEBUG",  # Set the logging level to DEBUG
            format=log_format,  # Improved log format
            diagnose=True,  # Enable diagnostic information
            enqueue=True,  # Use a queue for logging to avoid blocking
            backtrace=True,  # Enable backtrace for better error reporting
            catch=True,  # Catch exceptions and log them
            colorize=True,  # Enable colorized output in the console
            compression="zip",  # Compress log files
            serialize=False,  # Do not serialize logs to JSON
        )
