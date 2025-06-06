from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loguru import logger
import streamlit as st

from sales_dashboard.infrastructure.db_engine import create_all_tables
from sales_dashboard.infrastructure.repositories.user_repository import (
    SQLUserRepository,
)
from sales_dashboard.services.health_service import HealthCheckService
from sales_dashboard.services.system_bootstrap_service import SystemBootstrapService


@dataclass
class AppState:
    """Application state container"""

    initialized: bool = False
    database_ready: bool = False
    admin_ready: bool = False
    error_message: str | None = None


@st.cache_resource
def initialize_application() -> dict[str, Any]:
    """One-time application initialization - cached across all sessions"""
    logger.info("Initializing application (cached)")

    try:
        # Database setup
        create_all_tables()

        # Health check
        health_service = HealthCheckService()
        health_status = health_service.check_database_health()

        if health_status["status"] != "healthy":
            return {
                "success": False,
                "error": f"Database health check failed: {health_status['message']}",
            }

        # Bootstrap admin
        user_repo = SQLUserRepository()
        bootstrap_service = SystemBootstrapService(user_repo)
        default_admin = bootstrap_service.ensure_default_admin()

        if not default_admin:
            return {"success": False, "error": "Failed to ensure default admin exists"}

        logger.info("Application initialization completed successfully")
        return {
            "success": True,
            "admin_id": default_admin.id,
            "message": "Application ready",
        }

    except Exception as e:
        logger.error(f"Application initialization failed: {e}")
        return {"success": False, "error": str(e)}


def ensure_app_ready() -> bool:
    """Ensure application is ready - call this at start of every page"""
    # Check if we've already verified in this session
    if st.session_state.get("app_verified", False):
        return True

    # Get cached initialization result
    init_result = initialize_application()

    if not init_result["success"]:
        st.error(f"Application initialization failed: {init_result['error']}")
        st.stop()
        return False

    # Mark as verified for this session
    st.session_state.app_verified = True
    logger.debug("Application readiness verified")
    return True
