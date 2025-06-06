from __future__ import annotations

import streamlit as st

# Check if user is logged in
if not st.session_state.get("logged_in", False):
    st.error("Access denied. Please login first.")
    st.stop()

user = st.session_state.get("user")

st.title("📊 Dashboard Utama")
st.write(f"Selamat datang, **{user.nama if user else 'User'}**!")

# User info
if user:
    with st.expander("👤 User Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {user.nama}")
            st.write(f"**Username:** {user.username}")
        with col2:
            st.write(f"**Email:** {user.email}")
            st.write(f"**Role:** {'Admin' if user.is_admin else 'User'}")

# Placeholder metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penjualan", "Rp 1.2M", "12%")
with col2:
    st.metric("Jumlah Mitra", "45", "3")
with col3:
    st.metric("Transaksi Hari Ini", "127", "8%")
with col4:
    st.metric("Margin Rata-rata", "15.2%", "2.1%")

st.info("🚧 Dashboard features sedang dalam pengembangan...")

# Admin-only section
if user and user.is_admin:
    st.subheader("🔧 Admin Section")
    st.write("Admin features akan ditambahkan di sini")
