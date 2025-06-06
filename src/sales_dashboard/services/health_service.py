from __future__ import annotations

from typing import Dict, Any
from loguru import logger
from sqlalchemy import text

from sales_dashboard.infrastructure.db_engine import get_db_session

class HealthCheckService:
    """Application health check service"""

    def check_database_health(self) -> Dict[str, Any]:
        """Check database connection health"""
        try:
            with get_db_session() as session:
                # More explicit SQLite check
                result = session.execute(text("SELECT sqlite_version()")).scalar()

            logger.info(f"Database health check passed - SQLite version: {result}")
            return {
                "status": "healthy",
                "database": "connected",
                "sqlite_version": result,
                "message": "Database connection successful"
            }

        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "message": f"Database error: {str(e)}"
            }

    def check_application_health(self) -> Dict[str, Any]:
        """Complete application health check"""
        db_health = self.check_database_health()

        # Add other health checks here (file system, external APIs, etc.)
        return {
            "status": db_health["status"],
            "checks": {
                "database": db_health,
                # "file_system": self.check_file_system(),
                # "external_api": self.check_external_api(),
            },
            "timestamp": "2025-01-07T10:00:00Z"  # Use actual timestamp
        }
