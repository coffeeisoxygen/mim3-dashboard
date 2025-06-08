"""Security-first page registry with bypass protection for MIM3 office tool."""

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
    """Page configuration with bypass-proof security validation."""

    path: str
    title: str
    icon: str
    group: PageGroup
    category: PageCategory
    description: str = ""
    default: bool = False

    def create_page(self) -> st.Page:  # type: ignore
        """Create Streamlit page object."""
        return st.Page(
            self.path,
            title=self.title,
            icon=self.icon,
            default=self.default,
        )

    def can_access(self, user: "UserEntity | None") -> bool:
        """Navigation filtering - primary security layer for UX."""
        match self.group:
            case PageGroup.PUBLIC:
                return True
            case PageGroup.GLOBAL:
                return user is not None and user.is_active
            case PageGroup.ADMIN_ONLY:
                return user is not None and user.is_admin and user.is_active
            case _:
                return False

    def validate_access_or_stop(self) -> "UserEntity":
        """🔒 BYPASS PROTECTION: Validate access or stop execution.

        This method provides page-level security that prevents direct URL bypass.
        Every protected page MUST call this method.

        Returns:
            UserEntity: Authenticated and authorized user (guaranteed)

        Note:
            Calls st.stop() if access is denied - no return on failure.
            Calling code can safely assume they have a valid, authorized user.
        """
        from sales_dashboard.core.streamlit_session_manager import session_manager

        # Step 1: Check session exists (prevents expired sessions)
        user = session_manager.get_logged_in_user()
        if not user:
            st.error("🔒 Session expired. Please log in again.")
            st.switch_page("ui/pages/pg_authentication.py")
            st.stop()

        # Step 2: Check account is active (prevents deactivated accounts)
        if not user.is_active:
            st.error("🚫 Account tidak aktif. Hubungi administrator.")
            st.switch_page("ui/pages/pg_authentication.py")
            st.stop()

        # Step 3: Check role-based access (prevents privilege escalation)
        match self.group:
            case PageGroup.PUBLIC:
                # Public pages allow any authenticated user
                return user

            case PageGroup.GLOBAL:
                # All active users can access
                return user

            case PageGroup.ADMIN_ONLY:
                # Only admin users can access - BYPASS PROTECTION
                if not user.is_admin:
                    st.error(
                        "❌ Anda tidak memiliki akses administrator untuk halaman ini."
                    )
                    st.switch_page("ui/pages/pg_dashboard.py")  # Redirect to safe page
                    st.stop()
                return user

            case _:
                # Unknown page group - deny access
                st.error("❌ Halaman tidak ditemukan.")
                st.switch_page("ui/pages/pg_dashboard.py")
                st.stop()


class PageRegistry:
    """🔒 Security-first page registry for MIM3 office tool."""

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
            description="Main dashboard with key metrics",
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
    def get_admin_pages(cls, user: "UserEntity") -> list[st.Page]:  # type: ignore
        """Get admin-only pages if user is admin."""
        if not user.is_admin:
            return []
        return [
            config.create_page()
            for config in cls._PAGES.values()
            if config.group == PageGroup.ADMIN_ONLY
        ]

    @classmethod
    def get_page_config(cls, page_name: str) -> PageConfig:
        """Get page configuration by name for security validation.

        Args:
            page_name: Name of the page in registry

        Returns:
            PageConfig: Configuration for the requested page

        Raises:
            KeyError: If page is not found in registry
        """
        if page_name not in cls._PAGES:
            raise KeyError(f"Page '{page_name}' not found in registry")
        return cls._PAGES[page_name]

    @classmethod
    def add_page(cls, name: str, config: PageConfig) -> None:
        """🆕 Easy page addition - just add to registry.

        Args:
            name: Unique name for the page
            config: Page configuration with security settings
        """
        cls._PAGES[name] = config

    @classmethod
    def get_all_pages(cls) -> dict[str, PageConfig]:
        """Get all registered pages (for admin/debugging purposes)."""
        return cls._PAGES.copy()


# Global registry instance
page_registry = PageRegistry()
