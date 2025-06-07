"""Sales Dashboard - Internal MIM3 Tool.

Simple Streamlit application for sales territory analysis and management.
Built with Python 3.10+, SQLAlchemy v2, and modern best practices.
"""

__version__ = "0.1.0"

# Main application components for easy importing
from .infrastructure import ensure_database_ready
from .models import authenticate_user
from .utils import setup_logging

__all__ = [
    # Version
    "__version__",
    # Core setup functions
    "ensure_database_ready",
    "setup_logging",
    # Key operations
    "authenticate_user",
]
