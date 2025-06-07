# services/app_service.py - Main application orchestrator
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loguru import logger
import streamlit as st

from sales_dashboard.infrastructure.db_engine import create_all_tables
from sales_dashboard.infrastructure.repositories.user_repository import (
    SQLUserRepository,
)
from sales_dashboard.services.core.auth_service import AuthService
from sales_dashboard.services.core.user_service import UserService
from sales_dashboard.services.system.bootsrap_service import BootstrapService
from sales_dashboard.services.system.health_service import HealthService
from sales_dashboard.services.system.metadata_service import MetadataService


@dataclass
class AppConfiguration:
    """Application configuration"""

    debug_mode: bool = True
    auto_create_admin: bool = True
    cache_enabled: bool = True


class ApplicationService:
    """Main application service - orchestrates all other services"""

    def __init__(self, config: AppConfiguration) -> None:
        self.config = config
        self._services_initialized = False

        # Initialize repositories
        self.user_repo = SQLUserRepository()

        # Initialize core services
        self.auth_service = AuthService(self.user_repo)
        self.user_service = UserService(self.user_repo, self.auth_service)
        self.health_service = HealthService()
        self.bootstrap_service = BootstrapService(self.user_service)
        self.metadata_service = MetadataService()

    @st.cache_resource
    def initialize(self) -> dict[str, Any]:
        """One-time application initialization"""
        logger.info("Initializing application (cached)")

        try:
            # Database setup
            create_all_tables()

            # Health check
            health_status = self.health_service.check_database_health()
            if health_status["status"] != "healthy":
                return {
                    "success": False,
                    "error": f"Database health check failed: {health_status['message']}",
                }

            # Bootstrap if enabled
            if self.config.auto_create_admin:
                default_admin = self.bootstrap_service.ensure_default_admin()
                if not default_admin:
                    return {
                        "success": False,
                        "error": "Failed to ensure default admin exists",
                    }

            logger.info("Application initialization completed successfully")
            return {"success": True, "message": "Application ready"}

        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            return {"success": False, "error": str(e)}

    def ensure_ready(self) -> bool:
        """Ensure application is ready"""
        if st.session_state.get("app_verified", False):
            return True

        init_result = self.initialize()

        if not init_result["success"]:
            st.error(f"Application initialization failed: {init_result['error']}")
            st.stop()
            return False

        st.session_state.app_verified = True
        logger.debug("Application readiness verified")
        return True


# Global application service instance
@st.cache_resource
def get_app_service() -> ApplicationService:
    """Get application service singleton"""
    config = AppConfiguration(debug_mode=True)
    return ApplicationService(config)
