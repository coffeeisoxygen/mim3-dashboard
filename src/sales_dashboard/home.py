"""Sales Dashboard - Main Application with Clean Architecture."""

from __future__ import annotations

import streamlit as st

from sales_dashboard.core.app_bootstrap import bootstrap_application
from sales_dashboard.core.streamlit_session_manager import session_manager
from sales_dashboard.ui.components.navigation_sidebar import create_streamlit_navigation
from sales_dashboard.ui.components.user_info_sidebar import show_user_info_sidebar
from sales_dashboard.ui.pages.pg_authentication import handle_logout, show_login_page
from sales_dashboard.ui.pages.pg_hpp_calculator import show_hpp_calculator_page
from sales_dashboard.ui.ui_config import ICONS, NAV

# =============================================================================
# 🚀 PAGE CONFIGURATION - MUST BE FIRST
# =============================================================================

st.set_page_config(
    page_title=":streamlit: SDP IM3 Report System",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# 🚀 APPLICATION BOOTSTRAP - STREAMLIT NATIVE
# =============================================================================

# Initialize application once (cached with @st.cache_resource)
bootstrap_application()

# Initialize session state (Streamlit native approach)
session_manager.init_session_state()

# Check for session timeout using the DRY wrapper
session_manager.check_and_handle_session_timeout()

# =============================================================================
# 📄 PAGE DEFINITIONS - CENTRALIZED
# =============================================================================


def _create_page_registry() -> dict[str, "st.Page"]: # type: ignore
    """Create centralized page registry for clean organization.

    Returns:
        Dictionary mapping page names to st.Page objects
    """
    return {
        # Authentication pages
        "login": st.Page(show_login_page, title="Login", icon=ICONS.LOGIN),
        "logout": st.Page(handle_logout, title="Logout", icon=ICONS.LOGOUT),
        # Main application pages
        "dashboard": st.Page(
            "ui/pages/pg_dashboard.py",
            title=NAV.DASHBOARD_TITLE,
            icon=ICONS.DASHBOARD,
            default=True,
        ),
        "profile": st.Page(
            "ui/pages/pg_profile.py",
            title=NAV.PROFILE_TITLE,
            icon=ICONS.PERSON,
        ),
        "hpp_calculator": st.Page(
            show_hpp_calculator_page,
            title="HPP Calculator",
            icon="📊",
        ),
        # Admin pages
        "admin_users": st.Page(
            "ui/pages/admin/pg_users_management.py",
            title=NAV.USER_MANAGEMENT_TITLE,
            icon=ICONS.GROUP,
        ),
        "admin_settings": st.Page(
            "ui/pages/admin/pg_sys_settings.py",
            title=NAV.SYSTEM_SETTINGS_TITLE,
            icon=ICONS.SETTINGS,
        ),
    }


# =============================================================================
# 🧭 MAIN APPLICATION FLOW - COMPONENT-BASED
# =============================================================================


def main() -> None:
    """Main application flow using component-based architecture."""
    # Get current user from session
    user = st.session_state.get("user") if st.session_state.get("logged_in") else None

    # Create page registry
    pages = _create_page_registry()

    # Create navigation using component
    navigation = create_streamlit_navigation(user, pages)

    # Show user info in sidebar if logged in
    if user:
        with st.sidebar:
            show_user_info_sidebar(user)

    # Run the navigation
    navigation.run()


# Run the application
if __name__ == "__main__":
    main()
else:
    # When imported (e.g., by streamlit run), execute main
    main()

# ============# LIST TODO: masalah Authentiation dan Session Management
# TODO: Phase 2 - Enhanced Session Management (Optional)
#
# 1. Per-user session files for multi-user support
#    Path: .streamlit_session/{username}.json
#    Benefit: Multiple users can login on same machine
#    Priority: Low (single user per machine is typical in office)
#
# 2. User-agent security for session validation
#    Hash browser/device fingerprint for security
#    Benefit: Prevent session hijacking
#    Priority: Low (internal office environment)
#
# 3. Enhanced session cleanup and management
#    Auto-cleanup old session files
#    Session monitoring and analytics
#    Priority: Low (basic cleanup already works)
