"""Sales Dashboard - Main Application with Dynamic Navigation.

TODO: Refactor for better architecture
TODO: Implement browser sessionStorage for refresh persistence
TODO: Move user info to absolute bottom of sidebar
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.core.session_management import session_manager
from sales_dashboard.infrastructure.db_engine import ensure_database_ready
from sales_dashboard.ui.pages.pg_authentication import handle_logout, show_login_page
from sales_dashboard.ui.pages.pg_hpp_calculator import show_hpp_calculator_page
from sales_dashboard.ui.ui_config import ICONS, NAV
from sales_dashboard.utils.log_setup import setup_logging

# =============================================================================
# 🚀 PAGE CONFIGURATION - MUST BE FIRST
# =============================================================================

st.set_page_config(
    page_title=":streamlit: SDP IM3 Report System",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 🚀 APPLICATION INITIALIZATION
# =============================================================================

# Initialize core services
setup_logging(debug=True)

try:
    ensure_database_ready()
except Exception:
    st.error("Failed to initialize database. Please contact support.")
    st.stop()

# Initialize session state with manager
session_manager.init_session_state()

# Check for session timeout
if session_manager.check_session_timeout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.warning("Session expired after 8 hours. Please log in again.")

# Update activity on each interaction
session_manager.update_activity()

# =============================================================================
# 📄 PAGE DEFINITIONS
# =============================================================================

# Authentication pages
login = st.Page(show_login_page, title="Login", icon=ICONS.LOGIN)
logout = st.Page(handle_logout, title="Logout", icon=ICONS.LOGOUT)

# Main application pages
dashboard = st.Page(
    "ui/pages/pg_dashboard.py",
    title=NAV.DASHBOARD_TITLE,
    icon=ICONS.DASHBOARD,
    default=True,
)
profile = st.Page(
    "ui/pages/pg_profile.py",
    title=NAV.PROFILE_TITLE,
    icon=ICONS.PERSON,
)
hpp_calculator = st.Page(
    show_hpp_calculator_page,
    title="HPP Calculator",
    icon="📊",
)

# Admin pages
admin_users = st.Page(
    "ui/pages/admin/pg_users_management.py",
    title=NAV.USER_MANAGEMENT_TITLE,
    icon=ICONS.GROUP,
)
admin_settings = st.Page(
    "ui/pages/admin/pg_sys_settings.py",
    title=NAV.SYSTEM_SETTINGS_TITLE,
    icon=ICONS.SETTINGS,
)

# =============================================================================
# 🧭 DYNAMIC NAVIGATION & SIDEBAR
# =============================================================================


def _show_user_info_at_absolute_bottom(user) -> None:
    """Show user info at absolute bottom of sidebar with enhanced CSS."""
    # Enhanced CSS for better reliability and responsiveness
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

    # User info in fixed container with better structure
    role_display = "Admin" if user.is_admin else "User"
    icon = "😎" if user.is_admin else "👤"

    session_time = ""
    if st.session_state.get("login_time"):
        login_time = st.session_state.login_time
        session_time = f" • {login_time.strftime('%H:%M')}"

    st.markdown(
        f"""
        <div class="user-info-bottom">
            <div class="user-text">
                {icon} <strong>{user.nama}</strong> ({role_display}){session_time}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Build navigation based on authentication
if st.session_state.logged_in and st.session_state.user:
    user = st.session_state.user

    # TODO: Refactor cross-border dependencies between UI modules
    # Build navigation
    page_dict = {
        NAV.ACCOUNT_SECTION: [profile, logout],
        NAV.REPORTS_SECTION: [dashboard, hpp_calculator],
    }

    if user.is_admin:
        page_dict[NAV.ADMIN_SECTION] = [admin_users, admin_settings]

    # Create navigation
    pg = st.navigation(page_dict)

    # TODO: Move to absolute bottom - current implementation
    with st.sidebar:
        _show_user_info_at_absolute_bottom(user)

else:
    pg = st.navigation([login])

pg.run()
