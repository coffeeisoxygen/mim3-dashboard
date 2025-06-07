"""Models layer - simple functions for business operations.

Following KISS principle - direct functions instead of complex repository patterns.
All operations work directly with SQLAlchemy entities.
"""

from .user_operations import (
    activate_user,
    admin_reset_user_password,
    authenticate_user,
    change_user_password,
    create_user_by_admin,
    deactivate_user,
    get_all_active_users,
    get_user_by_id,
)

__all__ = [
    # User authentication
    "authenticate_user",
    # Admin user management
    "create_user_by_admin",
    "activate_user",
    "deactivate_user",
    # Password management
    "change_user_password",
    "admin_reset_user_password",
    # User queries
    "get_user_by_id",
    "get_all_active_users",
]
