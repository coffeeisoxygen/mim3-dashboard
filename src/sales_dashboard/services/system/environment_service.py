# services/system/environment_service.py
from __future__ import annotations

import os
import shutil
import platform
import time
from dataclasses import dataclass
import streamlit as st

@dataclass
class SystemMetrics:
    """System metrics for dashboard display"""
    cpu_percent: float
    memory_percent: float
    disk_free_gb: float
    disk_total_gb: float
    python_version: str
    platform: str
    uptime_hours: float

class EnvironmentService:
    """Environment monitoring for modern dashboard UI"""

    @st.cache_data(ttl=30)  # Refresh every 30 seconds
    def get_system_metrics(_self) -> SystemMetrics:
        """Get current system metrics - cached for performance"""
        try:
            import psutil

            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            # Disk usage
            disk_usage = shutil.disk_usage(".")
            disk_free_gb = disk_usage.free / (1024**3)
            disk_total_gb = disk_usage.total / (1024**3)

            # System info
            uptime = psutil.boot_time()
            current_time = time.time()
            uptime_hours = (current_time - uptime) / 3600

            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_free_gb=round(disk_free_gb, 2),
                disk_total_gb=round(disk_total_gb, 2),
                python_version=platform.python_version(),
                platform=platform.platform(),
                uptime_hours=round(uptime_hours, 2)
            )
        except ImportError:
            # Fallback without psutil
            return SystemMetrics(
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_free_gb=0.0,
                disk_total_gb=0.0,
                python_version=platform.python_version(),
                platform=platform.platform(),
                uptime_hours=0.0
            )

    def show_system_status(self) -> None:
        """Display system status in modern UI"""
        metrics = self.get_system_metrics()

        st.subheader("🖥️ System Status")

        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "CPU Usage",
                f"{metrics.cpu_percent:.1f}%",
                delta=None,
                delta_color="inverse"
            )

        with col2:
            st.metric(
                "Memory Usage",
                f"{metrics.memory_percent:.1f}%",
                delta=None,
                delta_color="inverse"
            )

        with col3:
            st.metric(
                "Disk Free",
                f"{metrics.disk_free_gb:.1f} GB",
                delta=f"of {metrics.disk_total_gb:.1f} GB"
            )

        with col4:
            st.metric(
                "Uptime",
                f"{metrics.uptime_hours:.1f}h",
                delta=None
            )

        # Progress bars for visual appeal
        st.progress(metrics.cpu_percent / 100, text="CPU")
        st.progress(metrics.memory_percent / 100, text="Memory")

        # System info expander
        with st.expander("🔧 System Information"):
            st.write(f"**Platform**: {metrics.platform}")
            st.write(f"**Python Version**: {metrics.python_version}")
            st.write(f"**Process ID**: {os.getpid()}")
