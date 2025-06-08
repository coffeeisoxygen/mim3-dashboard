"""Sales Dashboard - Main Application using Official Streamlit Navigation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from sales_dashboard.core.app_bootstrap import bootstrap_application
from sales_dashboard.core.page_registry import PageGroup, page_registry
from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.ui.components.user_info_sidebar import show_user_info_sidebar

if TYPE_CHECKING:
    from sales_dashboard.infrastructure.db_entities import UserEntity

# =============================================================================
# 🚀 PAGE CONFIGURATION - MUST BE FIRST
# =============================================================================

st.set_page_config(
    page_title="SDP IM3 Report System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 🚀 APPLICATION BOOTSTRAP
# =============================================================================

bootstrap_application()
session_manager.init_session_state()
session_manager.check_and_handle_session_timeout()

# =============================================================================
# 🧭 STREAMLIT NAVIGATION WITH PAGE REGISTRY
# =============================================================================


def main() -> None:
    """Main application using page registry for navigation."""

    # Check authentication state
    if not st.session_state.get("logged_in", False):
        # Unauthenticated - only show public pages
        public_pages = page_registry.get_pages_by_group(PageGroup.PUBLIC)
        pg = st.navigation(public_pages)
    else:
        # Authenticated - get user with type safety
        user: "UserEntity | None" = st.session_state.get("user")

        # Type guard - ensure user exists and is properly typed
        if user is None:
            # Defensive programming - shouldn't happen but handle gracefully
            st.error("🔄 Session error. Please log in again.")
            st.session_state.logged_in = False
            st.rerun()
            return

        # Show user info in sidebar
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
            pg = st.navigation({
                "Account": account_pages + [logout_page],
                "Reports": report_pages,
                "Administration": admin_pages,
            })
        else:
            # Regular user navigation
            pg = st.navigation({
                "Account": account_pages + [logout_page],
                "Reports": report_pages,
            })

    # Run the selected page
    pg.run()


if __name__ == "__main__":
    main()
else:
    main()
