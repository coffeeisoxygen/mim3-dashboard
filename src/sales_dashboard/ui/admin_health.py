# ui/admin_health.py (untuk monitoring)
import streamlit as st

from sales_dashboard.services.health_service import HealthCheckService


def show_health_dashboard():
    """Admin health monitoring dashboard"""
    if not st.session_state.get("user", {}).get("is_admin", False):
        st.error("Access denied. Admin only.")
        return

    st.title("🏥 System Health Dashboard")

    health_service = HealthCheckService()

    if st.button("Run Health Check"):
        with st.spinner("Checking system health..."):
            health_status = health_service.check_application_health()

        if health_status["status"] == "healthy":
            st.success("✅ All systems healthy")
        else:
            st.error("❌ System issues detected")

        st.json(health_status)
