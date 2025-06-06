import streamlit as st

st.title("📊 Dashboard Utama")
st.write("Selamat datang di Dashboard Penjualan & Monitoring Mitra IM3")

# Placeholder metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penjualan", "Rp 1.2M", "12%")
with col2:
    st.metric("Jumlah Mitra", "45", "3")
with col3:
    st.metric("Transaksi Hari Ini", "127", "8%")
with col4:
    st.metric("Margin Rata-rata", "15.2%", "2.1%")

st.info("🚧 Dashboard sedang dalam pengembangan...")

# Placeholder chart
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["Penjualan", "Target", "Margin"]
)

st.line_chart(chart_data)
