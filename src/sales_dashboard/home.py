"""Main application entry point with modern Python features"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st
from loguru import logger

from sales_dashboard.log_setup import setup_logging
from sales_dashboard.services.health_service import HealthCheckService
from sales_dashboard.services.system_bootstrap_service import SystemBootstrapService
from sales_dashboard.services.app_metadata_service import show_app_info
from sales_dashboard.infrastructure.repositories.user_repository import SQLUserRepository
from sales_dashboard.infrastructure.db_engine import create_all_tables

if TYPE_CHECKING:
    pass

# 1. Setup logging FIRST (cached, runs only once)
setup_logging(debug=True)  # Set to False for production
logger.info("Starting Sales Dashboard application")

# 2. Database initialization (cached, safe to run multiple times)
@st.cache_resource
def initialize_database() -> dict[str, str]:
    """Initialize database tables - cached to prevent recreation"""
    try:
        create_all_tables()
        logger.info("Database tables initialized successfully")
        return {"status": "success", "message": "Database ready"}
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return {"status": "error", "message": str(e)}

# 3. Bootstrap system
try:
    # Initialize database
    db_status = initialize_database()
    if db_status["status"] != "success":
        st.error(f"Database initialization failed: {db_status['message']}")
        st.stop()

    # Health check
    health_service = HealthCheckService()
    health_status = health_service.check_database_health()

    if health_status["status"] != "healthy":
        logger.error(f"Database health check failed: {health_status['message']}")
        st.error("Database connection failed. Please check logs.")
        st.stop()

    # Bootstrap default admin (with proper caching)
    user_repo = SQLUserRepository()
    bootstrap_service = SystemBootstrapService(user_repo)
    default_admin = bootstrap_service.ensure_default_admin()

    if default_admin:
        logger.info("System bootstrap completed successfully")

except Exception as e:
    logger.error(f"System bootstrap failed: {e}")
    st.error("System initialization failed. Please check logs.")
    st.stop()

# 4. Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    logger.debug("Session state initialized - user not logged in")

# 5. App metadata in sidebar
with st.sidebar:
    show_app_info()

# 6. Pages configuration
auth_page = st.Page("ui/login.py", title="Authentication", icon=":material/login:")
dashboard = st.Page("ui/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

# 7. Navigation based on login status
if st.session_state.logged_in:
    user = st.session_state.get("user")

    if user and user.is_admin:
        logger.debug(f"Admin user {user.username} - showing full navigation")
        pg = st.navigation({
            "Dashboard": [dashboard],
            "Admin": [auth_page],
        })
    else:
        logger.debug(f"Regular user {user.username if user else 'Unknown'} - showing limited navigation")
        pg = st.navigation({
            "Dashboard": [dashboard],
            "Account": [auth_page],
        })
else:
    logger.debug("User not logged in - showing login page only")
    pg = st.navigation([auth_page])

pg.run()
