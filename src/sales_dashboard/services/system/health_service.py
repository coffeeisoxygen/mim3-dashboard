from __future__ import annotations

from typing import Dict, Any
from datetime import datetime
from loguru import logger
from sqlalchemy import text

from sales_dashboard.infrastructure.db_engine import get_db_session
from sales_dashboard.services.interfaces import HealthServiceInterface


class HealthService(HealthServiceInterface):
    """Health check service"""

    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and basic operations"""
        try:
            with get_db_session() as session:
                result = session.execute(text("SELECT sqlite_version()"))
                version = result.scalar()
                logger.info(f"Database health check passed - SQLite version: {version}")

                return {
                    "status": "healthy",
                    "database": "sqlite",
                    "version": version,
                    "message": "Database connection successful",
                }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "message": "Database connection failed",
            }

    def check_application_health(self) -> Dict[str, Any]:
        """Check overall application health"""
        checks = {
            "database": self.check_database_health(),
            "memory": self._check_memory_usage(),
            "disk": self._check_disk_space(),
        }

        # Determine overall status
        overall_status = "healthy"
        if any(check["status"] != "healthy" for check in checks.values()):
            overall_status = "degraded"

        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "checks": checks,
        }

    def _check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            import psutil

            memory = psutil.virtual_memory()

            return {
                "status": "healthy" if memory.percent < 80 else "warning",
                "usage_percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2),
            }
        except ImportError:
            return {
                "status": "unknown",
                "message": "psutil not available for memory monitoring",
            }

    def _check_disk_space(self) -> Dict[str, Any]:
        """Check disk space"""
        try:
            import shutil

            usage = shutil.disk_usage(".")

            free_percent = (usage.free / usage.total) * 100

            return {
                "status": "healthy" if free_percent > 10 else "warning",
                "free_percent": round(free_percent, 2),
                "free_gb": round(usage.free / (1024**3), 2),
            }
        except Exception as e:
            return {"status": "unknown", "message": f"Disk check failed: {e}"}
