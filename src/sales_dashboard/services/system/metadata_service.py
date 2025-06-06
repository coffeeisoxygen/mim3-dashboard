from __future__ import annotations

from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
import streamlit as st

try:
    from sales_dashboard._version import __version__
except ImportError:
    __version__ = "dev-unknown"


@dataclass
class AppMetadata:
    """Application metadata information"""

    name: str = "Sales Dashboard IM3"
    version: str = __version__
    description: str = "Desktop ETL Dashboard untuk monitoring penjualan dan analytics"
    author: str = "Development Team"
    contact_email: str = "dev@dashboard.com"
    repository: str = "https://github.com/company/sales-dashboard"
    license: str = "MIT"
    python_version: str = ">=3.10"

    def get_build_info(self) -> Dict[str, Any]:
        """Get build and runtime information"""
        return {
            "version": self.version,
            "python_version": self.python_version,
            "streamlit_version": st.__version__,
            "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "environment": "development" if "dev" in self.version else "production",
        }


class MetadataService:
    """Application metadata service"""

    def __init__(self) -> None:
        self.metadata = AppMetadata()

    @st.cache_data
    def get_metadata(_self) -> AppMetadata:
        """Get application metadata - cached"""
        return _self.metadata

    def get_build_info(self) -> Dict[str, Any]:
        """Get build information"""
        return self.metadata.get_build_info()

    def show_app_info(self) -> None:
        """Display application information in sidebar"""
        metadata = self.get_metadata()
        build_info = metadata.get_build_info()

        with st.expander("ℹ️ App Information"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**{metadata.name}**")
                st.write(f"Version: `{metadata.version}`")
                st.write(f"Environment: `{build_info['environment']}`")

            with col2:
                st.write(f"Python: {metadata.python_version}")
                st.write(f"Streamlit: {build_info['streamlit_version']}")
                st.write(f"License: {metadata.license}")

            st.write(f"📧 Contact: {metadata.contact_email}")
            st.write(f"🔗 Repository: {metadata.repository}")

            if build_info["environment"] == "development":
                st.warning("🚧 Development Mode")
