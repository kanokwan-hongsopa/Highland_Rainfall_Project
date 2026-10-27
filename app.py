"""
Highland Rainfall Project - Main Application
Interactive Data Analytics Dashboard (2022–2023)
Halloween Horror Edition — 100% Matching assets/dashboard_reference.png
"""

import streamlit as st
import streamlit.components.v1 as components
from dashboard.halloween_app import get_halloween_html

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="สภาพภูมิอากาศบนพื้นที่สูงของประเทศไทย (2022–2023)",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ซ่อน Sidebar และ Header ของ Streamlit 100% เพื่อให้แสดงผลเต็มหน้าจอตามภาพต้นแบบ
st.markdown("""
    <style>
        /* ซ่อน Streamlit Sidebar */
        [data-testid="stSidebar"], section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* ซ่อน Header และ Footer */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        /* คืนพื้นที่ให้คอนเทนต์เต็ม 100% ไร้ขอบส่วนเกิน */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            border: none !important;
            width: 100% !important;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# เรนเดอร์ Halloween Interactive Dashboard
html_code = get_halloween_html()
components.html(html_code, height=1680, scrolling=True)
