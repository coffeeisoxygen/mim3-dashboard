"""Dashboard Page - Main overview and key metrics.

Available to all authenticated users.
"""

from __future__ import annotations

import streamlit as st


def main() -> None:
    """Dashboard page - native Streamlit navigation approach."""

    # Get user from session (set by navigation system)
    user = st.session_state.get("user")

    # Type guard - should not happen with proper navigation, but defensive programming
    if not user:
        st.error("⚠️ Session error. Please log in again.")
        st.switch_page("ui/pages/pg_authentication.py")
        return

    st.header(f"📊 Dashboard - Welcome, {user.nama}")

    # =============================================================================
    # 📈 KEY METRICS OVERVIEW
    # =============================================================================

    st.subheader("📈 Key Metrics")

    # Placeholder metrics - will be replaced with real data later
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Sales", value="$125,430", delta="12.5%")

    with col2:
        st.metric(label="Active Territories", value="45", delta="2")

    with col3:
        st.metric(label="Monthly Growth", value="8.2%", delta="1.1%")

    with col4:
        st.metric(label="Active Users", value="23", delta="-1")

    # =============================================================================
    # 📊 CHARTS AND VISUALIZATIONS
    # =============================================================================

    st.subheader("📊 Sales Performance")

    # Placeholder charts - will be replaced with real data
    col1, col2 = st.columns(2)

    with col1:
        st.info("📈 **Sales Trend Chart**\n\nComing soon - sales performance over time")

    with col2:
        st.info(
            "🗺️ **Territory Map**\n\nComing soon - interactive territory visualization"
        )

    # =============================================================================
    # 📋 RECENT ACTIVITY
    # =============================================================================

    st.subheader("📋 Recent Activity")

    # Show user-specific information
    if user.is_admin:
        st.success("🔐 **Admin View** - You have access to all system features")

        # Admin-specific quick actions
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👥 Manage Users", use_container_width=True):
                st.switch_page("ui/pages/admin/pg_users_management.py")

        with col2:
            if st.button("⚙️ System Settings", use_container_width=True):
                st.switch_page("ui/pages/admin/pg_sys_settings.py")

    else:
        st.info("👤 **User View** - Access to dashboard and profile features")

    # =============================================================================
    # 🎯 QUICK ACTIONS
    # =============================================================================

    st.subheader("🎯 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤 Edit Profile", use_container_width=True):
            st.switch_page("ui/pages/pg_profile.py")

    with col2:
        st.button("📊 Generate Report", use_container_width=True, disabled=True)
        st.caption("Coming soon")

    with col3:
        st.button("📤 Export Data", use_container_width=True, disabled=True)
        st.caption("Coming soon")

    # =============================================================================
    # 📝 SYSTEM STATUS
    # =============================================================================

    with st.expander("🔧 System Status", expanded=False):
        st.success("✅ Database connection: Active")
        st.success("✅ Authentication system: Online")
        st.info("ℹ️ Last updated: Real-time")

        if user.is_admin:
            st.write("**System Info:**")
            st.write(f"- User ID: {user.id}")
            st.write(f"- Username: {user.username}")
            st.write(f"- Admin Status: {user.is_admin}")
            st.write(f"- Account Created: {user.created}")


# Entry point for navigation
main()
