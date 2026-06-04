# run_student.py
# Chạy giao diện sinh viên: streamlit run run_student.py

import streamlit as st
from app.ui.student_view import render_student_view

st.set_page_config(page_title="ICTU AI Agent - Sinh viên", page_icon="🎓", layout="wide")
render_student_view(agent=None)
