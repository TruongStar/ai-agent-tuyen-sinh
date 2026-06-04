# run_admin.py
# Chạy giao diện quản trị: streamlit run run_admin.py

import streamlit as st
from app.ui.admin_view import render_admin_view

st.set_page_config(page_title="ICTU AI Agent - Admin", page_icon="🛠️", layout="wide")
render_admin_view(rebuild_kb_func=None)
