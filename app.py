"""
Highland Rainfall Project - Main Application
Interactive Data Analytics Dashboard (2022–2023)
Halloween Edition 🎃 & Classic Analytics View
"""

import streamlit as st
import streamlit.components.v1 as components
from dashboard.components import apply_custom_css
from dashboard.tab_climate import render_tab_climate
from dashboard.tab_rice_rain import render_tab_rice_rain
from dashboard.tab_methodology import render_tab_methodology
from dashboard.halloween_app import get_halloween_html

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="Highland Rainfall Dashboard — Halloween Edition 🎃",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# แถบด้านข้าง (Sidebar) สำหรับเลือกโหมดการแสดงผล
with st.sidebar:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #211631 0%, #130D22 100%); padding: 1.25rem 1rem; border-radius: 12px; color: #F7F0E8; margin-bottom: 1rem; text-align: center; border: 1px solid rgba(255,138,50,0.4); box-shadow: 0 4px 15px rgba(255,138,50,0.15);">
            <div style="font-size: 2.2rem; margin-bottom: 0.25rem;">🎃🏔️🌾</div>
            <div style="font-weight: 700; font-size: 1.15rem; letter-spacing: 0.02em; color: #FF8A32;">Highland Rainfall</div>
            <div style="font-size: 0.8rem; color: #A778E8;">Halloween Interactive Edition</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 มุมมองแดชบอร์ด (Dashboard View)")
    selected_view = st.radio(
        "เลือกรูปแบบการแสดงผล:",
        [
            "🎃 Halloween Interactive Edition (แนะนำ - มีแอนิเมชันซูม & Cross-Filter)",
            "🛰️ Classic: ภาพรวมภูมิอากาศบนพื้นที่สูง (9 จังหวัด)",
            "🌾 Classic: ฝนกับผลผลิตข้าวนาปี (5 จังหวัด)",
            "📋 Classic: ระเบียบวิธีวิจัยและข้อจำกัด (Methodology & QA)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ℹ️ ธรรมาภิบาลข้อมูล (Data Governance)")
    st.markdown("""
        - **กรอบเวลา:** 2022–2023 (ข้อมูลจริงเท่านั้น)
        - **ความครบถ้วน:** 50 สถานี 983 แถว (Missing 217 แถว, 7 ค่าฝนว่าง)
        - **สถานะโมเดล:** เชิงสำรวจ (Non-causal, ห้ามทำนายผล)
        - **การเป็นตัวแทน:** สถานีเฉพาะจุด ไม่ใช่ตัวแทนทั้งจังหวัด
        - **หน่วยวัด:** ฝนและผลผลิตอยู่ระหว่าง "หน่วยรอยืนยัน"
    """)
    st.caption("Highland_Rainfall_Project © 2026")

# แสดงผลตามมุมมองที่เลือก
if selected_view == "🎃 Halloween Interactive Edition (แนะนำ - มีแอนิเมชันซูม & Cross-Filter)":
    # ซ่อนขอบและช่องว่างส่วนเกินของ Streamlit สำหรับ Halloween Edition
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0.5rem !important;
                padding-bottom: 0rem !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                max-width: 100% !important;
            }
            header[data-testid="stHeader"] {
                background: transparent !important;
            }
            footer {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # โหลด Standalone Halloween Interactive App
    halloween_html = get_halloween_html()
    components.html(halloween_html, height=1400, scrolling=True)

elif selected_view == "🛰️ Classic: ภาพรวมภูมิอากาศบนพื้นที่สูง (9 จังหวัด)":
    apply_custom_css()
    render_tab_climate()

elif selected_view == "🌾 Classic: ฝนกับผลผลิตข้าวนาปี (5 จังหวัด)":
    apply_custom_css()
    render_tab_rice_rain()

else:
    apply_custom_css()
    render_tab_methodology()
