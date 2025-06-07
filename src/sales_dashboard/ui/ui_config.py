"""UI Configuration - Modern Material Design constants with proper types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MaterialIcons:
    """Material Design 3 icons for modern UI."""

    # Authentication & Users - Correct format
    LOGIN = ":material/login:"  # ✅ Correct format
    LOGOUT = ":material/logout:"
    PERSON = ":material/person:"
    ADMIN_PANEL = ":material/admin_panel_settings:"

    # States & Feedback
    ERROR = ":material/error:"
    SUCCESS = ":material/check_circle:"
    WARNING = ":material/warning:"

    # Navigation
    DASHBOARD = ":material/dashboard:"
    SETTINGS = ":material/settings:"
    GROUP = ":material/group:"
    ACCOUNT_CIRCLE = ":material/account_circle:"

    # Actions
    EDIT = ":material/edit:"
    DELETE = ":material/delete:"
    ADD = ":material/add:"
    SAVE = ":material/save:"


@dataclass(frozen=True)
class AppConfig:
    """Modern application configuration."""

    TITLE: str = "Sales Dashboard"
    DESCRIPTION: str = "Internal sales management tool for MIM3 offices"


@dataclass(frozen=True)
class AuthConfig:
    """Modern authentication UI configuration."""

    LOGIN_TITLE: str = "Sales Dashboard"
    LOGIN_SUBTITLE: str = "Secure access to your sales management tools"
    LOGIN_BUTTON_TEXT: str = "Sign In"

    # Modern messages
    WELCOME_MESSAGE: str = "Welcome back, {name}!"
    INVALID_CREDENTIALS: str = "Invalid username or password"
    MISSING_FIELDS: str = "Please enter both username and password"


@dataclass(frozen=True)
class NavigationConfig:
    """Navigation structure configuration."""

    # Section names
    ACCOUNT_SECTION: str = "Account"
    REPORTS_SECTION: str = "Reports"
    ADMIN_SECTION: str = "Administration"

    # Page titles
    DASHBOARD_TITLE: str = "Dashboard"
    PROFILE_TITLE: str = "Profile"
    USER_MANAGEMENT_TITLE: str = "User Management"
    SYSTEM_SETTINGS_TITLE: str = "System Settings"


# Global instances for easy import
ICONS = MaterialIcons()
APP = AppConfig()
AUTH = AuthConfig()
NAV = NavigationConfig()

# Streamlit page config as a simple dict with proper types
PAGE_CONFIG = {
    "page_title": "Sales Dashboard",
    "page_icon": ":material/dashboard:",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
