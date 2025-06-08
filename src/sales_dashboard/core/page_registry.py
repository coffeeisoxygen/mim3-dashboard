"""Centralized page registry with security-first role-based access control."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity


class PageGroup(str, Enum):
    """Page access groups - simple and extensible."""

    PUBLIC = "public"  # No login required
    GLOBAL = "global"  # All logged-in users
    ADMIN_ONLY = "admin_only"  # Admin users only


class PageCategory(str, Enum):
    """Page categories for navigation organization."""

    PUBLIC = "public"  # Login page
    ACCOUNT = "account"  # Profile management
    REPORTS = "reports"  # Dashboard, HPP calculator
    ADMIN = "admin"  # Admin functions


@dataclass
class PageConfig:
    """Page configuration with security-first role-based access control."""

    path: str
    title: str
    icon: str
    group: PageGroup
    category: PageCategory
    description: str = ""
    default: bool = False

    def create_page(self) -> st.Page:  # type: ignore
        """Create Streamlit page object with correct parameter order."""
        return st.Page(
            self.path,
            title=self.title,
            icon=self.icon,
            default=self.default,
        )

    def can_access(self, user: "UserEntity | None") -> bool:
        """Check if user can access this page (for navigation filtering)."""
        match self.group:
            case PageGroup.PUBLIC:
                return True
            case PageGroup.GLOBAL:
                return user is not None and user.is_active
            case PageGroup.ADMIN_ONLY:
                return user is not None and user.is_admin and user.is_active
            case _:
                return False

    def require_access(self) -> "UserEntity":
        """🔒 SECURITY-FIRST: Enforce authentication and authorization.

        This is the PRIMARY security enforcement point.
        Every protected page MUST call this method.

        Returns:
            UserEntity: Authenticated and authorized user (guaranteed)

        Note:
            This function will call st.stop() if access is denied.
            The calling page can assume they have a valid user after this call.
        """
        from sales_dashboard.core.auth_helper import (
            get_current_user,
            require_admin_access,
            require_user_access,
        )

        match self.group:
            case PageGroup.PUBLIC:
                # Public pages don't require authentication, but if require_access() is called,
                # we should return current user or None - but this method promises UserEntity
                # So for public pages calling require_access(), we ensure there's a user
                user = get_current_user()
                if user is None:
                    st.error(
                        "🔒 Halaman ini memerlukan login. Silakan login terlebih dahulu."
                    )
                    st.switch_page("ui/pages/pg_authentication.py")
                    st.stop()
                return user  # Now guaranteed to be UserEntity

            case PageGroup.GLOBAL:
                # All logged-in users can access
                user = require_user_access()  # Guaranteed UserEntity or st.stop()
                if not user.is_active:
                    st.error("🚫 Account tidak aktif. Hubungi administrator.")
                    st.switch_page("ui/pages/pg_authentication.py")
                    st.stop()
                return user

            case PageGroup.ADMIN_ONLY:
                # Only admin users can access
                user = (
                    require_admin_access()
                )  # Guaranteed admin UserEntity or st.stop()
                if not user.is_active:
                    st.error("🚫 Account tidak aktif. Hubungi administrator.")
                    st.switch_page("ui/pages/pg_authentication.py")
                    st.stop()
                return user

            case _:
                # Unknown page group - deny access
                st.error("❌ Akses tidak diizinkan untuk halaman ini")
                st.switch_page("ui/pages/pg_authentication.py")
                st.stop()


class PageRegistry:
    """🔒 Security-first centralized registry for all pages with role-based access."""

    # All page configurations - easy to extend for new pages
    _PAGES = {
        # ===== PUBLIC PAGES =====
        "login": PageConfig(
            path="ui/pages/pg_authentication.py",
            title="Log in",
            icon=":material/login:",
            group=PageGroup.PUBLIC,
            category=PageCategory.PUBLIC,
            description="Authentication page",
        ),
        # ===== USER PAGES (GLOBAL ACCESS) =====
        "profile": PageConfig(
            path="ui/pages/pg_profile.py",
            title="Profile",
            icon=":material/person:",
            group=PageGroup.GLOBAL,
            category=PageCategory.ACCOUNT,
            description="User profile management",
        ),
        "dashboard": PageConfig(
            path="ui/pages/pg_dashboard.py",
            title="Dashboard",
            icon=":material/dashboard:",
            group=PageGroup.GLOBAL,
            category=PageCategory.REPORTS,
            default=True,
            description="Main dashboard",
        ),
        "hpp_calculator": PageConfig(
            path="ui/pages/pg_hpp_calculator.py",
            title="HPP Calculator",
            icon=":material/calculate:",
            group=PageGroup.GLOBAL,
            category=PageCategory.REPORTS,
            description="HPP calculation tool",
        ),
        # ===== ADMIN PAGES (ADMIN-ONLY ACCESS) =====
        "user_management": PageConfig(
            path="ui/pages/admin/pg_users_management.py",
            title="User Management",
            icon=":material/group:",
            group=PageGroup.ADMIN_ONLY,
            category=PageCategory.ADMIN,
            description="Admin user management",
        ),
        "system_settings": PageConfig(
            path="ui/pages/admin/pg_sys_settings.py",
            title="System Settings",
            icon=":material/settings:",
            group=PageGroup.ADMIN_ONLY,
            category=PageCategory.ADMIN,
            description="System configuration",
        ),
    }

    @classmethod
    def get_pages_by_group(
        cls, group: PageGroup, user: "UserEntity | None" = None
    ) -> list[st.Page]:  # type: ignore
        """Get all pages in a specific group that user can access."""
        return [
            config.create_page()
            for config in cls._PAGES.values()
            if config.group == group and config.can_access(user)
        ]

    @classmethod
    def get_pages_by_category(
        cls, category: str, user: "UserEntity | None" = None
    ) -> list[st.Page]:  # type: ignore
        """Get all pages in a specific category that user can access."""
        category_enum = PageCategory(category)
        return [
            config.create_page()
            for config in cls._PAGES.values()
            if config.category == category_enum and config.can_access(user)
        ]

    @classmethod
    def get_accessible_pages(cls, user: "UserEntity | None") -> dict[str, st.Page]:  # type: ignore
        """🔒 Get all pages accessible to user for navigation (security filtering)."""
        return {
            name: config.create_page()
            for name, config in cls._PAGES.items()
            if config.can_access(user)
        }

    @classmethod
    def get_page_config(cls, page_name: str) -> PageConfig:
        """Get page configuration by name.

        Raises:
            KeyError: If page is not found in registry
        """
        if page_name not in cls._PAGES:
            raise KeyError(f"Page '{page_name}' not found in registry")
        return cls._PAGES[page_name]

    @classmethod
    def add_page(cls, name: str, config: PageConfig) -> None:
        """🆕 Add new page to registry (for future extensibility)."""
        cls._PAGES[name] = config

    @classmethod
    def get_all_pages(cls) -> dict[str, PageConfig]:
        """Get all registered pages (for admin/debugging purposes)."""
        return cls._PAGES.copy()

    @classmethod
    def get_admin_pages(cls, user: "UserEntity") -> list[st.Page]:  # type: ignore
        """Get admin-only pages if user is admin.

        Args:
            user: User entity to check admin status

        Returns:
            List of admin pages if user is admin, empty list otherwise
        """
        if not user.is_admin:
            return []

        return cls.get_pages_by_group(PageGroup.ADMIN_ONLY, user)


# Global registry instance
page_registry = PageRegistry()
