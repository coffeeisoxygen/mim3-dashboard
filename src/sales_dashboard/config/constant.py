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

# Password hashing (Future: Make admin-configurable)
SIMPLE_HASH_SALT: Final[str] = "sales_dashboard_salt"  # Development only
BCRYPT_DEFAULT_ROUNDS: Final[int] = 12
USE_BCRYPT_DEFAULT: Final[bool] = True

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

# UI Component settings (Future: Make admin-configurable)
SIDEBAR_USER_INFO_WIDTH: Final[str] = "260px"
SIDEBAR_USER_INFO_PADDING: Final[str] = "1rem"
SIDEBAR_USER_INFO_MIN_HEIGHT: Final[str] = "2.5rem"
SIDEBAR_USER_INFO_BORDER_RADIUS: Final[str] = "8px"

# Additional UI spacing constants
SIDEBAR_USER_INFO_BOTTOM_MARGIN: Final[str] = "1rem"
SIDEBAR_USER_INFO_SIDE_MARGIN: Final[str] = "1rem"
SIDEBAR_USER_INFO_MOBILE_MARGIN: Final[str] = "0.5rem"
SIDEBAR_USER_INFO_INTERNAL_PADDING: Final[str] = "0.75rem"

# Additional UI styling constants
SIDEBAR_USER_INFO_FONT_SIZE: Final[str] = "0.8rem"
SIDEBAR_USER_INFO_Z_INDEX: Final[int] = 1000
SIDEBAR_USER_INFO_LINE_HEIGHT: Final[str] = "1.3"

# =============================================================================
# 📄 PAGE CONFIGURATION CONSTANTS
# =============================================================================

# System information
SYSTEM_VERSION: Final[str] = "0.1.0"
DATABASE_TYPE_DISPLAY: Final[str] = "SQLite"

# Password policy (displayed values)
PASSWORD_LENGTH_MIN_DISPLAY: Final[int] = 4
PASSWORD_LENGTH_MAX_DISPLAY: Final[int] = 20
PASSWORD_LENGTH_DEFAULT_DISPLAY: Final[int] = 6

# Session timeout options
SESSION_TIMEOUT_OPTIONS: Final[list[str]] = [
    "Never",
    "1 hour",
    "4 hours",
    "8 hours",
    "24 hours",
]

# Theme options
THEME_OPTIONS: Final[list[str]] = ["Light", "Dark", "Auto"]

# Default application title (for settings display)
APP_TITLE_DEFAULT_DISPLAY: Final[str] = "Sales Dashboard"

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

# Logging configuration (Future: Make admin-configurable)
LOG_LEVEL_DEBUG: Final[str] = "DEBUG"
LOG_LEVEL_INFO: Final[str] = "INFO"
LOG_ROTATION_SIZE: Final[str] = "1 MB"
LOG_RETENTION_DAYS: Final[str] = "7 days"
LOG_COMPRESSION: Final[str] = "zip"
LOG_DIRECTORY: Final[str] = "logs"
LOG_FILENAME: Final[str] = "sdp_dashboard.log"

# Environment detection
DEBUG_MODE: Final[bool] = True  # TODO: Read from environment
