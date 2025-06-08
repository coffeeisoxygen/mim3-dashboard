"""Centralized page registry with role-based access control."""

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
    """Page configuration with role-based access."""

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
            self.path,  # ✅ First positional argument (page)
            title=self.title,  # ✅ Named parameters
            icon=self.icon,
            default=self.default,
        )

    def can_access(self, user: "UserEntity | None") -> bool:
        """Check if user can access this page."""
        match self.group:
            case PageGroup.PUBLIC:
                return True
            case PageGroup.GLOBAL:
                return user is not None
            case PageGroup.ADMIN_ONLY:
                return user is not None and user.is_admin
            case _:
                return False


class PageRegistry:
    """Centralized registry for all pages with role-based access."""

    # All page configurations grouped by access level
    _PAGES = {
        # Public pages (no login required)
        "login": PageConfig(
            path="ui/pages/pg_authentication.py",
            title="Log in",
            icon=":material/login:",
            group=PageGroup.PUBLIC,
            category=PageCategory.PUBLIC,
            description="Authentication page",
        ),
        # Account pages
        "profile": PageConfig(
            path="ui/pages/pg_profile.py",
            title="Profile",
            icon=":material/person:",
            group=PageGroup.GLOBAL,
            category=PageCategory.ACCOUNT,
            description="User profile management",
        ),
        # Report pages
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
        # Admin-only pages
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
    def get_global_pages(cls, user: "UserEntity") -> list[st.Page]:  # type: ignore
        """Get all global pages (accessible to all logged-in users)."""
        return cls.get_pages_by_group(PageGroup.GLOBAL, user)

    @classmethod
    def get_admin_pages(cls, user: "UserEntity") -> list[st.Page]:  # type: ignore
        """Get all admin-only pages."""
        return cls.get_pages_by_group(PageGroup.ADMIN_ONLY, user)

    @classmethod
    def get_accessible_pages(cls, user: "UserEntity | None") -> dict[str, st.Page]:  # type: ignore
        """Get all pages accessible to user, organized by name."""
        return {
            name: config.create_page()
            for name, config in cls._PAGES.items()
            if config.can_access(user)
        }

    @classmethod
    def get_page_config(cls, page_name: str) -> PageConfig | None:
        """Get page configuration by name."""
        return cls._PAGES.get(page_name)


# Global registry instance
page_registry = PageRegistry()
