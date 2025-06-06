# services/app_metadata_service.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    pass

try:
    from sales_dashboard._version import __version__
except ImportError:
    __version__ = "dev-unknown"


@dataclass
class AppMetadata:
    """Application metadata information"""

    name: str = "Sales Dashboard IM3"
    version: str = __version__
    description: str = "Dashboard monitoring penjualan dan KPI IM3"
    author: str = "Development Team"
    contact_email: str = "dev@dashboard.com"
    repository: str = "https://github.com/company/sales-dashboard"
    license: str = "MIT"
    python_version: str = ">=3.10"

    def get_build_info(self) -> dict[str, str]:
        """Get build and runtime information"""
        return {
            "version": self.version,
            "python_version": self.python_version,
            "streamlit_version": st.__version__,
            "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


@st.cache_data
def get_app_metadata() -> AppMetadata:
    """Get application metadata - cached"""
    return AppMetadata()


def show_app_info() -> None:
    """Display application information in sidebar or expander"""
    metadata = get_app_metadata()
    build_info = metadata.get_build_info()

    with st.expander("ℹ️ App Information"):
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{metadata.name}**")
            st.write(f"Version: `{metadata.version}`")
            st.write(f"Author: {metadata.author}")

        with col2:
            st.write(f"Python: {metadata.python_version}")
            st.write(f"Streamlit: {build_info['streamlit_version']}")
            st.write(f"License: {metadata.license}")

        st.write(f"📧 Contact: {metadata.contact_email}")
        st.write(f"🔗 Repository: {metadata.repository}")
