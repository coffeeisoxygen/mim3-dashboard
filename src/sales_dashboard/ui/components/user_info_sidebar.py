"""User info sidebar component - Reusable UI component for displaying user info.

Responsibility: Display user information at bottom of sidebar
- Clean CSS styling with responsive design
- Session time display
- Role-based icon and display
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

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
        """
        <style>
        .user-info-bottom {
            position: fixed;
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            max-width: 260px;
            min-height: 2.5rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .user-info-bottom .user-text {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
            line-height: 1.3;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .user-info-bottom {
                left: 0.5rem;
                right: 0.5rem;
                bottom: 0.5rem;
                max-width: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_user_info_content(user: "UserEntity") -> None:
    """Render user info content with role-based styling.

    Args:
        user: User entity to display
    """
    # Role-based display
    role_display = "Admin" if user.is_admin else "User"
    icon = "😎" if user.is_admin else "🤓"

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
    role_display = "Admin" if user.is_admin else "User"
    icon = "😎" if user.is_admin else "👤"

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"{icon} **{user.nama}** ({role_display})")

    if st.session_state.get("login_time"):
        login_time = st.session_state.login_time
        st.sidebar.caption(f"Login: {login_time.strftime('%H:%M')}")
