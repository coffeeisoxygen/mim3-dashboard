"""User info sidebar component - Reusable UI component for displaying user info.

Responsibility: Display user information at bottom of sidebar
- Clean CSS styling with responsive design
- Session time display
- Role-based icon and display
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from sales_dashboard.config.constant import (
    SIDEBAR_USER_INFO_BORDER_RADIUS,
    SIDEBAR_USER_INFO_BOTTOM_MARGIN,
    SIDEBAR_USER_INFO_FONT_SIZE,
    SIDEBAR_USER_INFO_INTERNAL_PADDING,
    SIDEBAR_USER_INFO_LINE_HEIGHT,
    SIDEBAR_USER_INFO_MIN_HEIGHT,
    SIDEBAR_USER_INFO_MOBILE_MARGIN,
    SIDEBAR_USER_INFO_SIDE_MARGIN,
    SIDEBAR_USER_INFO_WIDTH,
    SIDEBAR_USER_INFO_Z_INDEX,
)
from sales_dashboard.config.messages import (
    ICON_ADMIN_FANCY,
    ICON_ADMIN_SIMPLE,
    ICON_USER_FANCY,
    ICON_USER_SIMPLE,
    ROLE_ADMIN_SHORT,
    ROLE_USER_SHORT,
)

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity


def show_user_info_sidebar(user: "UserEntity") -> None:
    """Display user info at absolute bottom of sidebar.

    Reusable component that can be used across different pages.

    Args:
        user: User entity to display info for

    Features:
        - Fixed position at bottom of sidebar
        - Responsive design for mobile
        - Role-based styling (admin vs user)
        - Session time display
    """
    _inject_user_info_css()
    _render_user_info_content(user)


def _inject_user_info_css() -> None:
    """Inject CSS styles for user info component."""
    st.markdown(
        f"""
        <style>
        .user-info-bottom {{
            position: fixed;
            bottom: {SIDEBAR_USER_INFO_BOTTOM_MARGIN};
            left: {SIDEBAR_USER_INFO_SIDE_MARGIN};
            right: {SIDEBAR_USER_INFO_SIDE_MARGIN};
            max-width: {SIDEBAR_USER_INFO_WIDTH};
            min-height: {SIDEBAR_USER_INFO_MIN_HEIGHT};
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: {SIDEBAR_USER_INFO_BORDER_RADIUS};
            padding: {SIDEBAR_USER_INFO_INTERNAL_PADDING};
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            z-index: {SIDEBAR_USER_INFO_Z_INDEX};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}

        .user-info-bottom .user-text {{
            font-size: {SIDEBAR_USER_INFO_FONT_SIZE};
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
            line-height: {SIDEBAR_USER_INFO_LINE_HEIGHT};
        }}

        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .user-info-bottom {{
                left: {SIDEBAR_USER_INFO_MOBILE_MARGIN};
                right: {SIDEBAR_USER_INFO_MOBILE_MARGIN};
                bottom: {SIDEBAR_USER_INFO_MOBILE_MARGIN};
                max-width: none;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_user_info_content(user: "UserEntity") -> None:
    """Render user info content with role-based styling.

    Args:
        user: User entity to display
    """
    # Role-based display using centralized constants
    role_display = ROLE_ADMIN_SHORT if user.is_admin else ROLE_USER_SHORT
    icon = ICON_ADMIN_FANCY if user.is_admin else ICON_USER_FANCY

    # Session time formatting
    session_time = ""
    if st.session_state.get("login_time"):
        login_time = st.session_state.login_time
        session_time = f" • {login_time.strftime('%H:%M')}"

    # Render user info in fixed container
    st.markdown(
        f"""
        <div class="user-info-bottom">
            <div class="user-text">
                {icon}<strong>{user.nama}</strong>
                ({role_display}){session_time}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Alternative: Simple text-only version for testing/fallback
def show_user_info_simple(user: "UserEntity") -> None:
    """Simple user info display without fancy CSS.

    Fallback version for testing or when CSS styling is not needed.

    Args:
        user: User entity to display
    """
    role_display = ROLE_ADMIN_SHORT if user.is_admin else ROLE_USER_SHORT
    icon = ICON_ADMIN_SIMPLE if user.is_admin else ICON_USER_SIMPLE

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"{icon} **{user.nama}** ({role_display})")

    if st.session_state.get("login_time"):
        login_time = st.session_state.login_time
        st.sidebar.caption(f"Login: {login_time.strftime('%H:%M')}")
