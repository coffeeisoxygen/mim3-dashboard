"""Main application entry point with modern Python features"""

from __future__ import annotations

import streamlit as st
from loguru import logger

from sales_dashboard.infrastructure.init_data import init_default_admin
from sales_dashboard.log_setup import setup_logging

# Setup logging at application start
setup_logging(debug=True)  # Set to False for production
logger.info("Starting Sales Dashboard application")

# Initialize database and default admin
init_default_admin()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    logger.debug("Session state initialized - user not logged in")

# Auth Pages
auth_page = st.Page("ui/auth.py", title="Authentication", icon=":material/login:")

# Dashboard Pages
dashboard = st.Page(
    "ui/dashboard.py",
    title="Dashboard Utama",
    icon=":material/dashboard:",
    default=True,
)
# sales_report = st.Page("ui_sales_report.py", title="Laporan Penjualan", icon=":material/trending_up:")
# partner_monitoring = st.Page("ui_partner_monitoring.py", title="Monitoring Mitra", icon=":material/groups:")
# sales_margin = st.Page("ui_sales_margin.py", title="Analisis Margin", icon=":material/analytics:")

# Tools Pages - TODO: Create these files
# search = st.Page("ui_search.py", title="Pencarian Data", icon=":material/search:")
# history = st.Page("ui_history.py", title="Riwayat Aktivitas", icon=":material/history:")

# Settings Pages - TODO: Create these files
# profile = st.Page("ui_profile.py", title="Profil Admin", icon=":material/person:")
# settings = st.Page("ui_settings.py", title="Pengaturan", icon=":material/settings:")

if st.session_state.logged_in:
    logger.debug(
        f"User {st.session_state.get('username')} is logged in - showing full navigation"
    )
    pg = st.navigation({
        "Dashboard": [dashboard],
        # "📈 Laporan": [sales_report, partner_monitoring, sales_margin],
        # "🔧 Tools": [search, history],
        "⚙️ Admin": [auth_page],  # Logout di admin
    })
else:
    logger.debug("User not logged in - showing login page only")
    pg = st.navigation([auth_page])  # Login page

pg.run()
