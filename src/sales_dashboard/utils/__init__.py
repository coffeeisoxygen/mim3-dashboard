"""Utilities package.

Contains utility functions and helpers.
"""

from __future__ import annotations

"""Utilities layer - shared helper functions and utilities.

Simple, focused utilities that can be used across the application.
"""

from .hasher import get_password_hasher
from .log_setup import setup_logging

__all__ = [
    # Password utilities
    "get_password_hasher",
    # Logging setup
    "setup_logging",
]
