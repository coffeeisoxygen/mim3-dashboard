"""Sales Dashboard - Main Application using Official Streamlit Navigation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from sales_dashboard.config.constant import (
    APP_ICON,
    APP_LAYOUT,
    APP_TITLE,
    SIDEBAR_EXPANDED,
)
from sales_dashboard.core.app_bootstrap import bootstrap_application
from sales_dashboard.core.page_registry import PageGroup, page_registry
from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.ui.components.user_info_sidebar import show_user_info_sidebar

if TYPE_CHECKING:
    pass


st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded" if SIDEBAR_EXPANDED else "collapsed",
)

# =============================================================================
# 🚀 APPLICATION BOOTSTRAP
# =============================================================================

bootstrap_application()
session_manager.init_session_state()
session_manager.check_and_handle_session_timeout()


def main() -> None:
    """Main application with role-based navigation."""

    # ✅ Single source of truth for authentication
    user = session_manager.get_logged_in_user()  # Returns UserEntity or None

    # ✅ Build navigation based on authentication state
    if user is None:
        # Unauthenticated - only show public pages
        public_pages = page_registry.get_pages_by_group(PageGroup.PUBLIC)
        pg = st.navigation(public_pages)
    else:
        # Authenticated - show user info and role-based pages
        with st.sidebar:
            show_user_info_sidebar(user)

        # Create logout page (function-based)
        def logout_handler():
            session_manager.logout_user()
            st.rerun()

        logout_page = st.Page(logout_handler, title="Log out", icon=":material/logout:")

        # Get pages organized by category using page registry
        account_pages = page_registry.get_pages_by_category("account", user)
        report_pages = page_registry.get_pages_by_category("reports", user)
        admin_pages = page_registry.get_admin_pages(user) if user.is_admin else []

        # Create navigation based on user type
        if user.is_admin:
            # Admin navigation with all sections
            pg = st.navigation(
                {
                    "Account": account_pages + [logout_page],
                    "Reports": report_pages,
                    "Administration": admin_pages,
                }
            )
        else:
            # Regular user navigation
            pg = st.navigation(
                {
                    "Account": account_pages + [logout_page],
                    "Reports": report_pages,
                }
            )

    pg.run()


if __name__ == "__main__":
    main()
else:
    main()


# TODO: Merubah Sistem Hardcoded menjadi editabel loadable oleh admin , lakukan ini di akhir masa development
