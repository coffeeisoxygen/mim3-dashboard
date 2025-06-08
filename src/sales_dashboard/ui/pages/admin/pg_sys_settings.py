"""Admin System Settings Page - System configuration and maintenance.

🔒 SECURITY: Admin-only page (ADMIN_ONLY access).
🛡️ BYPASS PROTECTION: Direct URL access is validated and blocked for non-admin users.
"""

from __future__ import annotations

import streamlit as st

from sales_dashboard.config.constant import (
    APP_TITLE_DEFAULT_DISPLAY,
    DATABASE_TYPE_DISPLAY,
    PASSWORD_LENGTH_DEFAULT_DISPLAY,
    PASSWORD_LENGTH_MAX_DISPLAY,
    PASSWORD_LENGTH_MIN_DISPLAY,
    SESSION_TIMEOUT_OPTIONS,
    SYSTEM_VERSION,
    THEME_OPTIONS,
)
from sales_dashboard.config.messages import (
    SYS_CAPTION_APP_TITLE,
    SYS_CAPTION_AUTO_LOGOUT,
    SYS_CAPTION_CLEAR_SESSIONS,
    SYS_CAPTION_EXPORTS,
    SYS_CAPTION_PASSWORD_LENGTH,
    SYS_CAPTION_REPORTS,
    SYS_CAPTION_RESET_DB,
    SYS_CAPTION_SESSION_TIMEOUT,
    SYS_CAPTION_SPECIAL_CHARS,
    SYS_CAPTION_THEME,
    SYS_COMING_SOON_BACKUP,
    SYS_COMING_SOON_LOGS,
    SYS_COMING_SOON_PERFORMANCE,
    SYS_COMING_SOON_RESTORE,
    SYS_DANGER_CLEAR_SESSIONS,
    SYS_DANGER_RESET_DATABASE,
    SYS_DANGER_WARNING,
    SYS_DB_STATS_COMING_SOON,
    SYS_DB_STATUS_CONNECTION,
    SYS_DB_STATUS_MIGRATIONS,
    SYS_DB_STATUS_TABLES,
    SYS_DB_TEST_SUCCESS,
    SYS_HEADER_APPLICATION_SETTINGS,
    SYS_HEADER_DATABASE_SETTINGS,
    SYS_HEADER_MAINTENANCE,
    SYS_HEADER_SYSTEM_SETTINGS,
    SYS_HEADER_USER_SYSTEM_SETTINGS,
    SYS_INFO_CURRENT_ADMIN,
    SYS_INFO_DATABASE_TYPE,
    SYS_INFO_RUNNING_NORMAL,
    SYS_INFO_SYSTEM_VERSION,
    WARNING_DANGER_ZONE,
)
from sales_dashboard.core.page_registry import page_registry


def main() -> None:
    """System settings page with bypass-proof admin security."""

    # 🔒 SECURITY VALIDATION: Prevents direct URL bypass
    page_config = page_registry.get_page_config("system_settings")
    user = page_config.validate_access_or_stop()  # Guaranteed admin user or st.stop()    # 🎯 Page logic - user is guaranteed valid admin
    st.header(SYS_HEADER_SYSTEM_SETTINGS)

    # ===== DATABASE SETTINGS =====
    st.subheader(SYS_HEADER_DATABASE_SETTINGS)

    col1, col2 = st.columns(2)

    with col1:
        st.info("**Database Status**")
        st.success(SYS_DB_STATUS_CONNECTION)
        st.success(SYS_DB_STATUS_TABLES)
        st.success(SYS_DB_STATUS_MIGRATIONS)

    with col2:
        st.info("**Database Actions**")

        if st.button("🔄 Test Connection", use_container_width=True):
            st.success(SYS_DB_TEST_SUCCESS)

        if st.button("📊 View Statistics", use_container_width=True, disabled=True):
            st.info(SYS_DB_STATS_COMING_SOON)  # ===== USER SYSTEM SETTINGS =====
    st.subheader(SYS_HEADER_USER_SYSTEM_SETTINGS)

    col1, col2 = st.columns(2)

    with col1:
        st.info("**Password Policy**")

        min_password_length = st.number_input(
            "Minimum password length",
            min_value=PASSWORD_LENGTH_MIN_DISPLAY,
            max_value=PASSWORD_LENGTH_MAX_DISPLAY,
            value=PASSWORD_LENGTH_DEFAULT_DISPLAY,
            disabled=True,
        )
        st.caption(SYS_CAPTION_PASSWORD_LENGTH)

        require_special_chars = st.checkbox(
            "Require special characters", value=False, disabled=True
        )
        st.caption(SYS_CAPTION_SPECIAL_CHARS)

    with col2:
        st.info("**Session Settings**")

        session_timeout = st.selectbox(
            "Session timeout",
            options=SESSION_TIMEOUT_OPTIONS,
            index=0,
            disabled=True,
        )
        st.caption(SYS_CAPTION_SESSION_TIMEOUT)

        auto_logout = st.checkbox(
            "Auto-logout on browser close", value=True, disabled=True
        )
        st.caption(SYS_CAPTION_AUTO_LOGOUT)  # ===== APPLICATION SETTINGS =====
    st.subheader(SYS_HEADER_APPLICATION_SETTINGS)

    col1, col2 = st.columns(2)

    with col1:
        st.info("**General Settings**")

        app_title = st.text_input(
            "Application title", value=APP_TITLE_DEFAULT_DISPLAY, disabled=True
        )
        st.caption(SYS_CAPTION_APP_TITLE)

        default_theme = st.selectbox(
            "Default theme", options=THEME_OPTIONS, index=0, disabled=True
        )
        st.caption(SYS_CAPTION_THEME)

    with col2:
        st.info("**Feature Flags**")

        enable_reports = st.checkbox(
            "Enable report generation", value=False, disabled=True
        )
        st.caption(SYS_CAPTION_REPORTS)

        enable_exports = st.checkbox("Enable data exports", value=False, disabled=True)
        st.caption(SYS_CAPTION_EXPORTS)  # ===== MAINTENANCE =====
    st.subheader(SYS_HEADER_MAINTENANCE)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Backup & Restore**")

        if st.button("💾 Create Backup", use_container_width=True, disabled=True):
            st.info(SYS_COMING_SOON_BACKUP)

        if st.button("📂 Restore Backup", use_container_width=True, disabled=True):
            st.info(SYS_COMING_SOON_RESTORE)

    with col2:
        st.info("**Logs & Monitoring**")

        if st.button("📋 View System Logs", use_container_width=True, disabled=True):
            st.info(SYS_COMING_SOON_LOGS)

        if st.button("📊 Performance Monitor", use_container_width=True, disabled=True):
            st.info(SYS_COMING_SOON_PERFORMANCE)

    with col3:
        st.info("**System Info**")

        if st.button("ℹ️ System Information", use_container_width=True):
            st.success(SYS_INFO_RUNNING_NORMAL)
            st.write(f"**{SYS_INFO_CURRENT_ADMIN}**", user.nama)
            st.write(f"**{SYS_INFO_SYSTEM_VERSION}** {SYSTEM_VERSION}")
            st.write(
                f"**{SYS_INFO_DATABASE_TYPE}** {DATABASE_TYPE_DISPLAY}"
            )  # ===== DANGER ZONE =====
    with st.expander("⚠️ Danger Zone", expanded=False):
        st.warning(WARNING_DANGER_ZONE)
        st.write(SYS_DANGER_WARNING)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🧹 Clear All Sessions", disabled=True):
                st.error(SYS_DANGER_CLEAR_SESSIONS)
            st.caption(SYS_CAPTION_CLEAR_SESSIONS)

        with col2:
            if st.button("🗑️ Reset Database", disabled=True):
                st.error(SYS_DANGER_RESET_DATABASE)
            st.caption(SYS_CAPTION_RESET_DB)


# Entry point for navigation
main()
