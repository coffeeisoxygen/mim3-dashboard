"""Dashboard Page - Main overview and key metrics.

🔒 SECURITY: Available to all authenticated users (GLOBAL access).
🛡️ BYPASS PROTECTION: Direct URL access is validated and blocked if unauthorized.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.core.page_registry import page_registry


def main() -> None:
    """Dashboard page with bypass-proof security."""

    # 🔒 SECURITY VALIDATION: Prevents direct URL bypass
    page_config = page_registry.get_page_config("dashboard")
    user = page_config.validate_access_or_stop()  # Guaranteed user or st.stop()

    # 🎯 Page logic - user is guaranteed valid and authorized
    st.header(f"📊 Dashboard - Welcome, {user.nama}")

    # ===== KEY METRICS OVERVIEW =====
    st.subheader("📈 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Sales", value="$125,430", delta="12.5%")

    with col2:
        st.metric(label="Active Territories", value="45", delta="2")

    with col3:
        st.metric(label="Monthly Growth", value="8.2%", delta="1.1%")

    with col4:
        st.metric(label="Active Users", value="23", delta="-1")

    # ===== ROLE-BASED FEATURES =====
    st.subheader("📋 Quick Actions")

    # 🔐 Role-based UI - user guaranteed valid by security validation
    if user.is_admin:
        st.success("🔐 **Admin View** - Full system access")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👥 Manage Users", use_container_width=True):
                st.switch_page("ui/pages/admin/pg_users_management.py")
        with col2:
            if st.button("⚙️ System Settings", use_container_width=True):
                st.switch_page("ui/pages/admin/pg_sys_settings.py")
    else:
        st.info("👤 **User View** - Standard access")

    # Common actions for all users
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤 Edit Profile", use_container_width=True):
            st.switch_page("ui/pages/pg_profile.py")

    with col2:
        if st.button("🧮 HPP Calculator", use_container_width=True):
            st.switch_page("ui/pages/pg_hpp_calculator.py")

    with col3:
        st.button("📊 Generate Report", disabled=True)
        st.caption("Coming soon")


# Entry point for navigation
main()
