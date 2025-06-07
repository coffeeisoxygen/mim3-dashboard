"""Sales Dashboard - Main Application with Dynamic Navigation.

Role-based multipage app following Streamlit best practices.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.infrastructure.db_engine import ensure_database_ready
from sales_dashboard.ui.pages.pg_authentication import (
    handle_logout,
    show_login_page,
    show_user_info_sidebar,
)

# Import our clean configuration
from sales_dashboard.ui.ui_config import APP, ICONS, NAV
from sales_dashboard.utils.log_setup import setup_logging

# =============================================================================
# 🚀 PAGE CONFIGURATION - MUST BE FIRST
# =============================================================================

st.set_page_config(**APP.PAGE_CONFIG)

# =============================================================================
# 🚀 APPLICATION INITIALIZATION
# =============================================================================


# Initialize core services
setup_logging(debug=True)
try:
    ensure_database_ready()
except Exception:
    st.error("Failed to initialize database. Please contact support.")
    st.stop()  # Halt app execution

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# =============================================================================
# 📄 PAGE DEFINITIONS
# =============================================================================

# Authentication pages
login = st.Page(show_login_page, title="Login", icon=ICONS.LOGIN)
logout = st.Page(handle_logout, title="Logout", icon=ICONS.LOGOUT)

# Main application pages
dashboard = st.Page(
    "ui/pages/dashboard.py",
    title=NAV.DASHBOARD_TITLE,
    icon=ICONS.DASHBOARD,
    default=True,
)
profile = st.Page(
    "ui/pages/profile.py",
    title=NAV.PROFILE_TITLE,
    icon=ICONS.PERSON,
)

# Admin pages
admin_users = st.Page(
    "ui/pages/admin/users.py",
    title=NAV.USER_MANAGEMENT_TITLE,
    icon=ICONS.GROUP,
)
admin_settings = st.Page(
    "ui/pages/admin/settings.py",
    title=NAV.SYSTEM_SETTINGS_TITLE,
    icon=ICONS.SETTINGS,
)

# =============================================================================
# 🧭 DYNAMIC NAVIGATION
# =============================================================================

# App title
st.title(APP.TITLE)

# Build navigation based on authentication
if st.session_state.logged_in and st.session_state.user:
    user = st.session_state.user

    # Show user info in sidebar
    show_user_info_sidebar(user)

    # Build role-based page dictionary
    page_dict = {
        NAV.ACCOUNT_SECTION: [profile, logout],
        NAV.REPORTS_SECTION: [dashboard],
    }

    # Add admin section if user is admin
    if user.is_admin:
        page_dict[NAV.ADMIN_SECTION] = [admin_users, admin_settings]

    # Create navigation
    pg = st.navigation(page_dict)
else:
    # Not logged in - show only login
    pg = st.navigation([login])

# Run the selected page
pg.run()
