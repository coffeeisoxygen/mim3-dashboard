"""Centralized constants for MIM3 Dashboard.

Single source of truth for technical configuration values.
For user-facing messages, see messages.py.
Later migrated to database for admin-editable settings.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

# =============================================================================
# 🗂️ DIRECTORY STRUCTURE
# =============================================================================

# Base directories
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"
CACHE_DIR: Final[Path] = PROJECT_ROOT / ".cache"

# Session storage
SESSION_DIR: Final[Path] = PROJECT_ROOT / ".streamlit_session"
SESSION_FILE: Final[Path] = SESSION_DIR / "session.json"

# =============================================================================
# 🗄️ DATABASE CONFIGURATION
# =============================================================================

DATABASE_NAME: Final[str] = "sales_dashboard.db"
DATABASE_PATH: Final[Path] = DATA_DIR / DATABASE_NAME
DATABASE_URL: Final[str] = f"sqlite:///{DATABASE_PATH}"

# Connection settings
DB_POOL_SIZE: Final[int] = 10
DB_TIMEOUT_SECONDS: Final[int] = 30
DB_POOL_RECYCLE_HOURS: Final[int] = 1

# =============================================================================
# 🔐 AUTHENTICATION & SESSION
# =============================================================================

# Password policy (Future: Make admin-configurable)
MIN_PASSWORD_LENGTH: Final[int] = 6
MAX_PASSWORD_LENGTH: Final[int] = 128
PASSWORD_REQUIRE_SPECIAL: Final[bool] = False
MAX_LOGIN_ATTEMPTS: Final[int] = 5
LOCKOUT_DURATION_MINUTES: Final[int] = 15

# Session management
SESSION_TIMEOUT_HOURS: Final[int] = 8
SESSION_CACHE_TTL_MINUTES: Final[int] = 2
USER_CACHE_TTL_MINUTES: Final[int] = 2

# Default admin credentials
DEFAULT_ADMIN_USERNAME: Final[str] = "admin"
DEFAULT_ADMIN_PASSWORD: Final[str] = "admin123"
DEFAULT_ADMIN_EMAIL: Final[str] = "admin@dashboard.com"
DEFAULT_ADMIN_NAME: Final[str] = "Administrator"

# =============================================================================
# 📊 APPLICATION SETTINGS
# =============================================================================

# Page configuration (Future: Make admin-configurable)
APP_TITLE: Final[str] = "SDP IM3 Report System"
APP_ICON: Final[str] = "📊"
APP_LAYOUT: Final[Literal["centered", "wide"]] = "wide"
SIDEBAR_EXPANDED: Final[bool] = True

# Cache settings
STREAMLIT_CACHE_TTL: Final[int] = 300  # 5 minutes

# =============================================================================
# 🏢 BUSINESS CONSTANTS (Future: Move to database)
# =============================================================================

# Hierarchy levels
HIERARCHY_LEVELS: Final[list[str]] = [
    "IOH",  # Indosat Ooredoo Hutchison
    "Circle",  # Circle level
    "Region",  # Region level
    "Micro Cluster",  # MC level
    "Personal Territory",  # PT level
    "Site",  # Tower/BTS
]

# Report types
REPORT_TYPES: Final[list[str]] = [
    "Daily Sales",
    "Sales Margin",
    "Sell In",
    "KPI Report",
]

# =============================================================================
# 🚀 DEVELOPMENT & LOGGING
# =============================================================================

# Logging
LOG_LEVEL_DEBUG: Final[str] = "DEBUG"
LOG_LEVEL_INFO: Final[str] = "INFO"
LOG_ROTATION_SIZE: Final[str] = "1 MB"
LOG_RETENTION_DAYS: Final[str] = "7 days"

# Environment detection
DEBUG_MODE: Final[bool] = True  # TODO: Read from environment
