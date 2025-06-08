"""Application bootstrap - handles initialization with Streamlit patterns."""

from __future__ import annotations

from loguru import logger
import streamlit as st

from sales_dashboard.config.constant import DEBUG_MODE
from sales_dashboard.config.messages import ERROR_APP_INITIALIZATION
from sales_dashboard.infrastructure.db_engine import ensure_database_ready
from sales_dashboard.utils.log_setup import setup_logging


@st.cache_resource
def initialize_application() -> bool:
    """One-time application initialization - Streamlit native caching."""
    try:
        logger.info("🚀 Starting application initialization...")  # Setup logging once
        setup_logging(debug=DEBUG_MODE)

        # Initialize database (already cached)
        ensure_database_ready()

        logger.info("✅ Application initialization completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Application initialization failed: {e}")
        raise


def bootstrap_application() -> None:
    """Bootstrap application - called from home.py.

    Uses cached initialization to prevent rerun spam.
    """
    try:
        # Initialize core application (cached - only runs once)
        initialization_success = initialize_application()

        # Only log bootstrap completion in debug mode and when not cached
        if initialization_success and "bootstrap_logged" not in st.session_state:
            st.session_state.bootstrap_logged = True
            logger.debug("🎯 Application bootstrap completed")

    except Exception as e:
        # User-friendly error for MIM3 office users
        st.error(f"{ERROR_APP_INITIALIZATION}\n\nDetail error: {str(e)}")
        logger.error(f"Bootstrap failed: {e}")
        st.stop()
