"""Sales Dashboard - Main Application with Dynamic Navigation.

Role-based multipage app following Streamlit best practices.
"""
# if needed emoji head here https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

from __future__ import annotations

from datetime import datetime, timedelta
import json

import streamlit as st

from sales_dashboard.infrastructure.db_engine import ensure_database_ready
from sales_dashboard.ui.pages.pg_authentication import (
    handle_logout,
    show_login_page,
)
from sales_dashboard.ui.ui_config import ICONS, NAV  # Remove PAGE_CONFIG import
from sales_dashboard.utils.log_setup import setup_logging

# =============================================================================
# 🚀 PAGE CONFIGURATION - MUST BE FIRST
# =============================================================================

# Define page config inline to avoid type issues
st.set_page_config(
    page_title=":streamlit: SDP IM3 Report System",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state() -> None:
    """Initialize session state with simple, reliable approach.

    SIMPLIFIED SESSION STATE MANAGEMENT
    """
    # Basic session initialization
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "login_time" not in st.session_state:
        st.session_state.login_time = None

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = None


def check_session_timeout() -> bool:
    """Check if session has timed out (8 hours for office use)."""
    if not st.session_state.get("logged_in", False):
        return False

    login_time = st.session_state.get("login_time")
    if not login_time:
        return False

    # 8-hour timeout for office environment
    timeout_hours = 8
    time_diff = datetime.now() - login_time
    return time_diff > timedelta(hours=timeout_hours)


def update_activity() -> None:
    """Update last activity timestamp."""
    if st.session_state.get("logged_in", False):
        st.session_state.last_activity = datetime.now()


# Quick fix - store session in hidden file
def save_session_state(user) -> None:
    """Save current session to file."""
    session_data = {
        "username": user.username,
        "login_time": datetime.now().isoformat(),
        "user_id": user.id,
    }

    with open(".streamlit_session", "w") as f:
        json.dump(session_data, f)


def load_session_state() -> dict | None:
    """Load session from file if exists and valid."""
    try:
        with open(".streamlit_session", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


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

# Initialize session state
init_session_state()

# Check for session timeout
if check_session_timeout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.warning("Session expired after 8 hours. Please log in again.")

# Update activity on each interaction
update_activity()

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
# 🧭 DYNAMIC NAVIGATION
# =============================================================================
def _show_bottom_user_info(user) -> None:
    """Compact user info at bottom of sidebar."""
    # Compact user display
    if user.is_admin:
        st.caption(f"👑 **{user.nama}** (Admin)")
    else:
        st.caption(f"👤 **{user.nama}**")

    # Session info if needed
    if st.session_state.get("login_time"):
        login_time = st.session_state.login_time
        st.caption(f"Session: {login_time.strftime('%H:%M')}")


# App title
# st.title(APP.TITLE)

# Build navigation based on authentication
if st.session_state.logged_in and st.session_state.user:
    user = st.session_state.user

    # Build navigation first
    page_dict = {
        NAV.ACCOUNT_SECTION: [profile, logout],
        NAV.REPORTS_SECTION: [dashboard],
    }

    if user.is_admin:
        page_dict[NAV.ADMIN_SECTION] = [admin_users, admin_settings]

    # Create navigation (Streamlit manages the sidebar)
    pg = st.navigation(page_dict)

    # Add user info at bottom of sidebar AFTER navigation
    with st.sidebar:
        st.markdown("---")  # Clean separator
        _show_bottom_user_info(user)

else:
    pg = st.navigation([login])

pg.run()
