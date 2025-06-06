import streamlit as st
from loguru import logger

from sales_dashboard.shared.auth import validate_credentials

# Cek apakah user sudah login
if st.session_state.get("logged_in", False):
    # Logout Interface
    st.title("👋 Logout")
    st.write(f"Selamat datang, **{st.session_state.get('username', 'Admin')}**!")
    st.write("Terima kasih telah menggunakan Dashboard IM3.")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Logout", type="secondary", use_container_width=True):
            username = st.session_state.get("username", "Unknown")
            logger.info(f"User {username} logged out")
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

else:
    # Login Interface
    st.title("🔐 Login Dashboard")
    st.write("Silakan masukkan kredensial Anda untuk mengakses dashboard.")

    with st.container():
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input(
            "Password", type="password", placeholder="Masukkan password"
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    logger.debug(f"Login attempt for username: {username}")
                    result = validate_credentials(username, password)
                    if result["success"]:
                        logger.info(f"Successful login for user: {username}")
                        st.session_state.logged_in = True
                        st.session_state.username = result["username"]
                        st.success("Login berhasil! Mengalihkan...")
                        st.rerun()
                    else:
                        logger.warning(f"Failed login attempt for username: {username}")
                        st.error("Username atau password salah!")
                else:
                    logger.debug("Login attempt with empty credentials")
                    st.warning("Harap isi username dan password!")
