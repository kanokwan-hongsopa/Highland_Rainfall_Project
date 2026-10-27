"""
Highland Rainfall Project - Main Application
จุดเริ่มต้นของ Interactive Dashboard สำหรับการวิเคราะห์ภูมิอากาศบนพื้นที่สูงและผลผลิตข้าวนาปี
"""

import streamlit as st
from dashboard.components import apply_custom_css
from dashboard.tab_climate import render_tab_climate
from dashboard.tab_rice_rain import render_tab_rice_rain
from dashboard.tab_methodology import render_tab_methodology

# ตั้งค่าหน้าเว็บ Streamlit
st.set_page_config(
    page_title="Highland Rainfall & Rice Analysis Dashboard (2022–2023)",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ใช้งาน Custom CSS สไตล์ Modern Analytics
apply_custom_css()

# แถบด้านข้าง (Sidebar)
with st.sidebar:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 1.25rem 1rem; border-radius: 10px; color: white; margin-bottom: 1rem; text-align: center;">
            <div style="font-size: 2.2rem; margin-bottom: 0.25rem;">🏔️🌾</div>
            <div style="font-weight: 700; font-size: 1.15rem; letter-spacing: 0.02em;">Highland Rainfall</div>
            <div style="font-size: 0.8rem; opacity: 0.9;">Agro-Climatic Research</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("### โครงการวิจัยพื้นที่สูง")
    st.markdown(
        "**โครงการวิเคราะห์สภาพภูมิอากาศบนพื้นที่สูงและความสัมพันธ์กับผลผลิตข้าวนาปี**  \n"
        "ช่วงข้อมูล: **2022–2023** เท่านั้น"
    )
    
    st.markdown("---")
    st.markdown("#### 🧭 เมนูหลัก (Navigation)")
    selected_tab = st.radio(
        "เลือกมุมมองการวิเคราะห์:",
        [
            "🛰️ ภาพรวมภูมิอากาศบนพื้นที่สูง (9 จังหวัด)",
            "🌾 ฝนกับผลผลิตข้าวนาปี (5 จังหวัด)",
            "📋 ระเบียบวิธีวิจัยและข้อจำกัด (Methodology & QA)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("#### ℹ️ สถานะโครงการ")
    st.markdown("""
        - **กรอบเวลา:** 2022–2023
        - **สถานะข้อมูล:** ข้อมูลจริงผ่านการตรวจสอบ (Cleaned)
        - **สถานะโมเดล:** เชิงสำรวจ (Non-causal, No Forecasting)
        - **การเป็นตัวแทน:** สถานีเฉพาะจุด ไม่ใช่ตัวแทนทั้งจังหวัด
    """)
    st.caption("Highland_Rainfall_Project © 2026")

# แสดงผลตามแท็บที่เลือก
if selected_tab == "🛰️ ภาพรวมภูมิอากาศบนพื้นที่สูง (9 จังหวัด)":
    render_tab_climate()
elif selected_tab == "🌾 ฝนกับผลผลิตข้าวนาปี (5 จังหวัด)":
    render_tab_rice_rain()
else:
    render_tab_methodology()
