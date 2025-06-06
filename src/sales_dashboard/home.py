"""Main application entry point with modern Python features."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.services.app_initialization_service import ensure_app_ready
from sales_dashboard.services.app_metadata_service import show_app_info
from sales_dashboard.utils.log_setup import setup_logging

# Setup logging once
setup_logging(debug=True)

# Ensure app is ready (cached, runs once across sessions)
if not ensure_app_ready():
    st.stop()

# Initialize session state once per session
if "session_initialized" not in st.session_state:
    st.session_state.session_initialized = True
    st.session_state.logged_in = False
    st.session_state.user = None
    logger.debug("Session state initialized")

# App metadata in sidebar
with st.sidebar:
    show_app_info()

# Pages configuration
auth_page = st.Page("ui/login.py", title="Authentication", icon=":material/login:")
dashboard = st.Page(
    "ui/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)

# Navigation based on login status
if st.session_state.logged_in:
    user = st.session_state.user

    if user and user.is_admin:
        logger.debug(f"Admin user {user.username} - showing full navigation")
        pg = st.navigation(
            {
                "Dashboard": [dashboard],
                "Admin": [auth_page],
            }
        )
    else:
        logger.debug(
            f"Regular user {user.username if user else 'Unknown'} - showing limited navigation"
        )
        pg = st.navigation(
            {
                "Dashboard": [dashboard],
                "Account": [auth_page],
            }
        )
else:
    logger.debug("User not logged in - showing login page only")
    pg = st.navigation([auth_page])

pg.run()
