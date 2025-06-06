"""Initialize default data for the application"""

from __future__ import annotations

from loguru import logger

from sales_dashboard.domain.models.user import User
from sales_dashboard.infrastructure.db_engine import (
    create_all_tables,
    get_streamlit_connection,
)
from sales_dashboard.infrastructure.repositories.user_repository import UserRepository


def init_default_admin() -> None:
    """Create default admin if not exists"""
    # Create tables first
    create_all_tables()

    conn = get_streamlit_connection()
    user_repo = UserRepository()

    try:
        # Check if any admin exists
        result = conn.query("SELECT * FROM users WHERE is_admin = 1")

        if result.empty:
            # Create default admin using domain model
            admin_user = User(
                id=None,
                nama="Administrator",
                email="admin@dashboard.com",
                username="admin",
                password="admin123",  # TODO: Hash this properly
                is_admin=True,
                is_active=True,
            )

            user_repo.save(admin_user)
            logger.info("✅ Default admin user created")
        else:
            logger.info("✅ Admin user already exists")

    except Exception as e:
        logger.error(f"❌ Error initializing admin: {e}")
        raise e
