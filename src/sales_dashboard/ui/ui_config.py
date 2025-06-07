"""UI Configuration - centralized constants and settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# Type aliases for Streamlit configuration
LayoutType = Literal["centered", "wide"]
SidebarStateType = Literal["auto", "expanded", "collapsed"]


@dataclass(frozen=True)
class MaterialIcons:
    """Material Design 3 icons for consistent UI."""

    # Authentication
    LOGIN = ":material/login:"
    LOGOUT = ":material/logout:"
    PERSON = ":material/person:"
    ADMIN_PANEL = ":material/admin_panel_settings:"

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
    REFRESH = ":material/refresh:"


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""

    TITLE = "Sales Dashboard"
    DESCRIPTION = "Internal sales management tool for MIM3 offices"

    # Streamlit page config with proper typing
    @property
    def PAGE_CONFIG(self) -> dict[str, Any]:
        """Page configuration for st.set_page_config()."""
        layout: LayoutType = "wide"
        sidebar_state: SidebarStateType = "expanded"

        return {
            "page_title": "Sales Dashboard",
            "page_icon": MaterialIcons.DASHBOARD,
            "layout": layout,
            "initial_sidebar_state": sidebar_state,
        }


@dataclass(frozen=True)
class AuthConfig:
    """Authentication-related UI configuration."""

    LOGIN_TITLE = "User Authentication"
    LOGIN_SUBTITLE = "Sign In"
    LOGIN_BUTTON_TEXT = "Sign In"

    # Messages
    WELCOME_MESSAGE = "Welcome, {name}"
    INVALID_CREDENTIALS = "Invalid username or password"
    MISSING_FIELDS = "Please enter both username and password"
    LOGOUT_SUCCESS = "You have been logged out"

    # Session timeout (8 hours for office use)
    SESSION_TIMEOUT_HOURS = 8


@dataclass(frozen=True)
class NavigationConfig:
    """Navigation structure configuration."""

    # Section names
    ACCOUNT_SECTION = "Account"
    REPORTS_SECTION = "Reports"
    ADMIN_SECTION = "Administration"

    # Page titles
    DASHBOARD_TITLE = "Dashboard"
    PROFILE_TITLE = "Profile"
    USER_MANAGEMENT_TITLE = "User Management"
    SYSTEM_SETTINGS_TITLE = "System Settings"


# Global instances for easy import
ICONS = MaterialIcons()
APP = AppConfig()
AUTH = AuthConfig()
NAV = NavigationConfig()
