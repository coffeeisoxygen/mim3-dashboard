"""Navigation sidebar component - Centralized navbar setup.

Responsibility: Build navigation structure based on user authentication
- Role-based navigation sections
- Clean page organization
- Reusable navigation logic
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import streamlit as st

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity


def build_navigation_for_user(
    user: "UserEntity", pages: dict[str, Any]
) -> dict[str, list[Any]]:
    """Build navigation structure based on user role.

    Args:
        user: User entity to build navigation for
        pages: Dictionary of page name to st.Page objects

    Returns:
        Dictionary of section name to list of pages

    Example:
        pages = {
            "profile": profile_page,
            "logout": logout_page,
            "dashboard": dashboard_page,
            "hpp_calculator": hpp_calculator_page,
            "admin_users": admin_users_page,
            "admin_settings": admin_settings_page,
        }
        nav_dict = build_navigation_for_user(user, pages)
    """
    from sales_dashboard.ui.ui_config import NAV

    # Base navigation for all authenticated users
    navigation = {
        NAV.ACCOUNT_SECTION: [pages["profile"], pages["logout"]],
        NAV.REPORTS_SECTION: [pages["dashboard"], pages["hpp_calculator"]],
    }

    # Add admin section if user is admin
    if user.is_admin:
        navigation[NAV.ADMIN_SECTION] = [
            pages["admin_users"],
            pages["admin_settings"],
        ]

    return navigation


def create_streamlit_navigation(
    user: "UserEntity | None", pages: dict[str, Any]
) -> (
    Any
):  # Changed from st.navigation to Any since StreamlitPage isn't directly importable
    """Create Streamlit navigation based on authentication state.

    Args:
        user: User entity (None if not logged in)
        pages: Dictionary of page name to st.Page objects

    Returns:
        Streamlit navigation object ready to run

    Example:
        nav = create_streamlit_navigation(user, pages)
        nav.run()
    """
    if user:
        # Build authenticated navigation
        page_dict = build_navigation_for_user(user, pages)
        return st.navigation(page_dict)
    else:
        # Show only login page for unauthenticated users
        return st.navigation([pages["login"]])


# Alternative: Simple function for basic navigation needs
def build_simple_navigation(
    user: "UserEntity | None",
) -> dict[str, list[Any]] | list[Any]:
    """Simple navigation builder without external page dependencies.

    For cases where you just need the structure without actual pages.

    Args:
        user: User entity (None if not logged in)

    Returns:
        Navigation structure or login page list
    """
    from sales_dashboard.ui.ui_config import NAV

    if not user:
        return []  # Return empty list for login-only navigation

    # Return structure template
    navigation = {
        NAV.ACCOUNT_SECTION: [],  # Profile, logout
        NAV.REPORTS_SECTION: [],  # Dashboard, calculator
    }

    if user.is_admin:
        navigation[NAV.ADMIN_SECTION] = []  # Admin pages

    return navigation
