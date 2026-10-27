"""
Highland Rainfall Project - UI Components Module
สไตล์และคอมโพเนนต์ส่วนแสดงผลสำหรับ Streamlit Dashboard
"""

import streamlit as st


def apply_custom_css():
    """
    แทรก CSS สไตล์ Modern Analytics Dashboard
    """
    st.markdown("""
        <style>
        /* สไตล์ฟอนต์และการจัดวางหลัก */
        .main-header {
            font-size: 1.85rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        .sub-header {
            font-size: 0.95rem;
            color: #475569;
            margin-bottom: 1.25rem;
        }
        
        /* Badge สรุปขอบเขต */
        .scope-badge {
            display: inline-block;
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
        }
        .scope-badge-amber {
            background-color: #fef3c7;
            color: #b45309;
        }
        .scope-badge-purple {
            background-color: #f3e8ff;
            color: #7e22ce;
        }
        
        /* Metric Card ทันสมัย */
        .metric-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 0.75rem;
            transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
        }
        .metric-title {
            font-size: 0.82rem;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.025em;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            font-size: 1.65rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }
        .metric-sub {
            font-size: 0.78rem;
            color: #94a3b8;
        }

        /* Banner ข้อจำกัดและคำเตือน */
        .notice-box {
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
            border-radius: 6px;
            padding: 0.85rem 1.1rem;
            margin: 0.9rem 0;
            color: #334155;
            font-size: 0.88rem;
            line-height: 1.5;
        }
        .notice-box-warning {
            border-left-color: #f59e0b;
            background-color: #fffbeb;
            color: #92400e;
        }
        .notice-box-danger {
            border-left-color: #ef4444;
            background-color: #fef2f2;
            color: #991b1b;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 3rem 1.5rem;
            background-color: #f8fafc;
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            margin: 1.5rem 0;
        }
        .empty-state-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: #475569;
            margin-bottom: 0.5rem;
        }
        .empty-state-text {
            font-size: 0.9rem;
            color: #64748b;
        }
        
        /* Data Source Footer */
        .source-footer {
            margin-top: 1.5rem;
            padding-top: 0.75rem;
            border-top: 1px solid #e2e8f0;
            font-size: 0.78rem;
            color: #64748b;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, badges: list = None):
    """
    ส่วนหัวหลักของหน้าหรือแท็บ
    """
    st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub-header">{subtitle}</div>', unsafe_allow_html=True)

    if badges:
        badge_html = "".join([f'<span class="scope-badge {b.get("class", "")}">{b["text"]}</span>' for b in badges])
        st.markdown(f'<div>{badge_html}</div>', unsafe_allow_html=True)


def render_metric_card(title: str, value: str, subtext: str = "", delta: str = None, delta_color: str = "normal"):
    """
    การ์ดแสดงค่า KPI สไตล์ Modern Web
    """
    delta_html = ""
    if delta:
        color_map = {"normal": "#0369a1", "green": "#16a34a", "red": "#dc2626", "amber": "#d97706"}
        dcolor = color_map.get(delta_color, "#0369a1")
        delta_html = f'<span style="font-size: 0.85rem; font-weight: 600; color: {dcolor}; margin-left: 0.5rem;">{delta}</span>'

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}{delta_html}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)


def render_notice_box(text: str, box_type: str = "info", title: str = None):
    """
    กล่องข้อความเตือน / ข้อจำกัด
    box_type: 'info', 'warning', 'danger'
    """
    type_class = ""
    icon = "ℹ️"
    if box_type == "warning":
        type_class = "notice-box-warning"
        icon = "⚠️"
    elif box_type == "danger":
        type_class = "notice-box-danger"
        icon = "🛑"

    title_html = f"<strong>{icon} {title}</strong><br/>" if title else f"<strong>{icon} ข้อสังเกตเชิงวิเคราะห์:</strong> "
    st.markdown(f"""
        <div class="notice-box {type_class}">
            {title_html}{text}
        </div>
    """, unsafe_allow_html=True)


def render_empty_state(message: str = "ไม่พบข้อมูลที่ตรงกับเงื่อนไขตัวกรอง", suggestion: str = "กรุณาปรับเปลี่ยนเงื่อนไขตัวกรองหรือกดปุ่มรีเซ็ต"):
    """
    กล่องแสดงผลเมื่อไม่มีข้อมูลตามตัวกรอง
    """
    st.markdown(f"""
        <div class="empty-state">
            <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🔍</div>
            <div class="empty-state-title">{message}</div>
            <div class="empty-state-text">{suggestion}</div>
        </div>
    """, unsafe_allow_html=True)


def render_source_footer(sources: list, limitations: list = None):
    """
    ส่วนท้ายระบุแหล่งที่มาของข้อมูล หน่วยวัด และข้อจำกัด
    """
    src_items = "".join([f"<li>{s}</li>" for s in sources])
    limit_items = "".join([f"<li>{l}</li>" for l in limitations]) if limitations else ""
    limit_section = f"<br/><strong>ข้อจำกัดของการวิเคราะห์:</strong><ul>{limit_items}</ul>" if limitations else ""

    st.markdown(f"""
        <div class="source-footer">
            <strong>แหล่งที่มาของข้อมูลและหน่วยวัด:</strong>
            <ul>{src_items}</ul>
            {limit_section}
        </div>
    """, unsafe_allow_html=True)
