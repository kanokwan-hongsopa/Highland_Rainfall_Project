"""
Highland Rainfall Project - Tab A: Climate Overview
แท็บ A: ภาพรวมสภาพภูมิอากาศบนพื้นที่สูง 9 จังหวัด (50 สถานี HRDI/OWM)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from dashboard.components import (
    render_header,
    render_metric_card,
    render_notice_box,
    render_empty_state,
    render_source_footer,
)
from dashboard.data_loader import (
    load_climate_data,
    get_climate_completeness_summary,
    MONTH_NAMES_TH,
)

# นิยามตัวแปรสภาพอากาศและหน่วยวัด
WEATHER_VARIABLES = {
    "rainfall_mm": {
        "label": "ปริมาณน้ำฝน (Rainfall)",
        "unit": "หน่วยรอยืนยัน (คาดการณ์ mm)",
        "col": "rainfall_mm",
        "description": "ปริมาณฝนสะสมรายเดือนจากสถานีตรวจวัด",
        "color": "#0284c7"
    },
    "TEMP": {
        "label": "อุณหภูมิเฉลี่ย (Mean Temperature)",
        "unit": "°C",
        "col": "TEMP",
        "description": "อุณหภูมิเฉลี่ยรายเดือน",
        "color": "#ea580c"
    },
    "HUMIDITY": {
        "label": "ความชื้นสัมพัทธ์ (Relative Humidity)",
        "unit": "%",
        "col": "HUMIDITY",
        "description": "ความชื้นสัมพัทธ์เฉลี่ยรายเดือน",
        "color": "#0d9488"
    },
    "WIND_SPEED": {
        "label": "ความเร็วลม (Wind Speed)",
        "unit": "m/s",
        "col": "WIND_SPEED",
        "description": "ความเร็วลมเฉลี่ยรายเดือน",
        "color": "#6366f1"
    },
    "RAINDAY": {
        "label": "จำนวนวันฝนตก (Rainy Days)",
        "unit": "วัน",
        "col": "RAINDAY",
        "description": "จำนวนวันที่มีฝนตกในแต่ละเดือน",
        "color": "#3b82f6"
    }
}


def render_tab_climate():
    """
    ฟังก์ชันหลักสำหรับแสดงผล แท็บ A: ภาพรวมภูมิอากาศบนพื้นที่สูง
    """
    df = load_climate_data()
    summary = get_climate_completeness_summary(df)

    # 1. ส่วนหัว
    render_header(
        title="🛰️ ภาพรวมสภาพภูมิอากาศบนพื้นที่สูง (9 จังหวัด)",
        subtitle="สำรวจข้อมูลรายเดือนจากสถานีตรวจวัดสภาพอากาศบนพื้นที่สูงของโครงการหลวง (HRDI) และ OpenWeatherMap (OWM) ปี 2022–2023",
        badges=[
            {"text": "ขอบเขต: 9 จังหวัดพื้นที่สูง", "class": ""},
            {"text": "50 สถานีตรวจวัด", "class": ""},
            {"text": "ช่วงข้อมูล: 2022–2023 เท่านั้น", "class": "scope-badge-purple"},
            {"text": "สถานะหน่วย: หน่วยรอยืนยัน", "class": "scope-badge-amber"}
        ]
    )

    # คำเตือนสำคัญประจำแท็บ
    render_notice_box(
        text="ข้อมูลภูมิอากาศในหน้านี้รวบรวมจากสถานีตรวจวัดเฉพาะจุดบนพื้นที่สูง <strong>ไม่ใช่ค่าเฉลี่ยพื้นที่ของทั้งจังหวัด</strong> "
             "และสถานีแต่ละแห่งมีช่วงเวลาเปิดบันทึกต่างกัน จึงมีเดือนที่ข้อมูลขาดหาย (Missing Rows) "
             "<strong>ห้ามนำผลรวมทั้งปีของสถานีที่มีเดือนขาดไปเปรียบเทียบกับสถานีที่มีข้อมูลครบ 12 เดือน</strong>",
        box_type="warning",
        title="ข้อกำหนดและข้อจำกัดของข้อมูลสถานี"
    )

    # 2. แถบตัวกรอง (Filters Section)
    with st.expander("🔍 ตัวกรองข้อมูลภูมิอากาศ (Climate Filters)", expanded=True):
        col_f1, col_f2, col_f3, col_f4 = st.columns([1.2, 1.8, 1.8, 1.2])

        with col_f1:
            year_options = ["ทั้งหมด (2022–2023)", "2022", "2023"]
            selected_year_str = st.selectbox("เลือกปี (Year):", year_options, index=0)
            if selected_year_str == "2022":
                selected_years = [2022]
            elif selected_year_str == "2023":
                selected_years = [2023]
            else:
                selected_years = [2022, 2023]

        with col_f2:
            all_provinces = sorted(df["province_clean"].unique().tolist())
            selected_provinces = st.multiselect(
                "เลือกจังหวัด (Provinces):",
                options=all_provinces,
                default=all_provinces,
                help="เลือกจังหวัดที่ต้องการสำรวจ (ค่าเริ่มต้นเลือกครบ 9 จังหวัด)"
            )

        with col_f3:
            # กรองรายชื่อสถานีตามจังหวัดที่เลือก
            available_stations = sorted(
                df[df["province_clean"].isin(selected_provinces)]["STA_TH"].unique().tolist()
            )
            selected_stations = st.multiselect(
                "เลือกสถานีตรวจวัด (Stations):",
                options=available_stations,
                default=[],
                help="หากไม่เลือก จะแสดงข้อมูลของทุกสถานีในจังหวัดที่เลือก"
            )

        with col_f4:
            var_keys = list(WEATHER_VARIABLES.keys())
            var_labels = [WEATHER_VARIABLES[k]["label"] for k in var_keys]
            selected_var_idx = st.selectbox(
                "ตัวแปรสภาพอากาศ:",
                options=range(len(var_keys)),
                format_func=lambda i: var_labels[i],
                index=0
            )
            selected_var_key = var_keys[selected_var_idx]
            selected_var_info = WEATHER_VARIABLES[selected_var_key]

        # ปุ่มรีเซ็ตตัวกรอง
        col_btn1, col_btn2 = st.columns([1, 5])
        with col_btn1:
            if st.button("🔄 รีเซ็ตตัวกรอง", use_container_width=True):
                st.rerun()

    # กรองข้อมูล
    filtered_df = df[
        (df["year"].isin(selected_years)) &
        (df["province_clean"].isin(selected_provinces))
    ].copy()

    if selected_stations:
        filtered_df = filtered_df[filtered_df["STA_TH"].isin(selected_stations)]

    # 3. จัดการกรณีไม่พบข้อมูล (Empty State)
    if filtered_df.empty:
        render_empty_state(
            message="ไม่พบข้อมูลสถานีตามเงื่อนไขตัวกรองที่คุณเลือก",
            suggestion="กรุณาเลือกจังหวัดหรือปีอื่น หรือกดปุ่ม 'รีเซ็ตตัวกรอง' เพื่อแสดงข้อมูลทั้งหมด"
        )
        return

    # 4. KPI Cards
    st.markdown("#### 📊 ข้อมูลสรุปเชิงสถิติ (Summary KPIs)")
    kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)

    num_sel_stations = filtered_df["STA_TH"].nunique()
    num_sel_provinces = filtered_df["province_clean"].nunique()
    total_records = len(filtered_df)
    
    # คำนวณความสมบูรณ์เฉพาะขอบเขตที่เลือก
    val_col = selected_var_info["col"]
    valid_records = filtered_df[val_col].notna().sum()
    missing_records = filtered_df[val_col].isna().sum()
    completeness_pct = round((valid_records / total_records * 100), 1) if total_records > 0 else 0

    with kpi_c1:
        render_metric_card(
            title="จำนวนสถานีจริง",
            value=f"{num_sel_stations:,}",
            subtext=f"จากทั้งหมด 50 สถานี ({round(num_sel_stations/50*100)}%)"
        )
    with kpi_c2:
        render_metric_card(
            title="จังหวัดที่มีข้อมูล",
            value=f"{num_sel_provinces}",
            subtext="จากขอบเขต 9 จังหวัด"
        )
    with kpi_c3:
        render_metric_card(
            title="ระเบียนสถานี–เดือน",
            value=f"{total_records:,}",
            subtext="แถวข้อมูลที่มีในชุดข้อมูล"
        )
    with kpi_c4:
        render_metric_card(
            title=f"ค่าสมบูรณ์ ({selected_var_key})",
            value=f"{valid_records:,}",
            subtext=f"ความครบถ้วน {completeness_pct}%",
            delta=f"ขาด {missing_records} ค่า" if missing_records > 0 else "ครบ 100%",
            delta_color="amber" if missing_records > 0 else "green"
        )
    with kpi_c5:
        # สรุปภาพรวม Missing Rows ทั้งหมดในชุดข้อมูล
        render_metric_card(
            title="Missing Rows (ภาพรวม)",
            value=f"{summary['missing_rows']}",
            subtext=f"สถานี-เดือนที่ไม่มีแถว ({summary['missing_rows_pct']}%)",
            delta="217 จาก 1,200",
            delta_color="amber"
        )

    st.markdown("---")

    # 5. Visualizations Section
    tab_view1, tab_view2, tab_view3, tab_view4 = st.tabs([
        "📈 แนวโน้มรายเดือน (Monthly Trend)",
        "🗺️ Heatmap ความครบถ้วน (Completeness Grid)",
        "📊 เปรียบเทียบสถานีในจังหวัด (Station Comparison)",
        "📋 ทะเบียนสถานีและพิกัด (Station Directory)"
    ])

    # -------------------------------------------------------------
    # มุมมองที่ 1: กราฟเส้นแนวโน้มรายเดือน
    # -------------------------------------------------------------
    with tab_view1:
        st.markdown(f"##### แนวโน้มรายเดือน: {selected_var_info['label']} ({selected_var_info['unit']})")
        
        # ตัวเลือกระดับการพล็อต: รายสถานี หรือ ค่าเฉลี่ยรายจังหวัด
        col_t1, col_t2 = st.columns([1.5, 3.5])
        with col_t1:
            agg_mode = st.radio(
                "การแสดงผลเส้นกราฟ:",
                ["รายสถานี (Individual Stations)", "ค่าเฉลี่ยสถานีในจังหวัด (Station-Average)"],
                index=1 if num_sel_stations > 10 else 0,
                horizontal=True
            )

        # เตรียมข้อมูลสำหรับพล็อต
        if "รายสถานี" in agg_mode:
            # พล็อตรายสถานี (ถ้าสถานีเยอะเกิน 15 ให้แสดงคำแนะนำ)
            if num_sel_stations > 20:
                render_notice_box(
                    text=f"ปัจจุบันมีสถานีที่เลือกจำนวนมาก ({num_sel_stations} สถานี) เส้นกราฟอาจซ้อนทับกัน แนะนำให้เลือกสถานีเจาะจง หรือเลือกโหมด 'ค่าเฉลี่ยสถานีในจังหวัด'",
                    box_type="info"
                )

            plot_df = filtered_df.sort_values(["year", "month"]).copy()
            fig_trend = px.line(
                plot_df,
                x="year_month",
                y=val_col,
                color="STA_TH",
                markers=True,
                labels={
                    "year_month": "ปี-เดือน (Year-Month)",
                    val_col: f"{selected_var_info['label']} ({selected_var_info['unit']})",
                    "STA_TH": "สถานีตรวจวัด"
                },
                title=f"แนวโน้มรายเดือนของ {selected_var_info['label']} รายสถานี ({selected_year_str})"
            )
        else:
            # ค่าเฉลี่ยเฉพาะสถานีที่มีในจังหวัด (ห้ามตีความว่าเป็นค่าเฉลี่ยทั้งจังหวัด)
            render_notice_box(
                text="<strong>คำเตือนการแปลผล:</strong> เส้นกราฟด้านล่างคือ <strong>ค่าเฉลี่ยของสถานีตรวจวัดบนพื้นที่สูงในแต่ละจังหวัด</strong> "
                     "ไม่ใช่ค่าเฉลี่ยของพื้นที่ทั้งจังหวัด และสถานีที่มีเดือนขาดจะไม่ถูกคำนวณในเดือนที่ขาดนั้น",
                box_type="warning"
            )
            prov_monthly = filtered_df.groupby(["year_month", "province_clean"], as_index=False).agg(
                mean_val=(val_col, "mean"),
                station_count=("STA_TH", "nunique")
            ).sort_values("year_month")

            fig_trend = px.line(
                prov_monthly,
                x="year_month",
                y="mean_val",
                color="province_clean",
                markers=True,
                labels={
                    "year_month": "ปี-เดือน (Year-Month)",
                    "mean_val": f"ค่าเฉลี่ยสถานี ({selected_var_info['unit']})",
                    "province_clean": "จังหวัด",
                    "station_count": "จำนวนสถานีที่คำนวณ"
                },
                title=f"ค่าเฉลี่ยสถานีบนพื้นที่สูงรายจังหวัด: {selected_var_info['label']} ({selected_year_str})"
            )

        fig_trend.update_layout(
            hovermode="x unified",
            xaxis=dict(tickangle=-45),
            margin=dict(l=40, r=40, t=50, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # -------------------------------------------------------------
    # มุมมองที่ 2: Heatmap ความครบถ้วนของข้อมูลสถานี x เดือน
    # -------------------------------------------------------------
    with tab_view2:
        st.markdown("##### ตารางความครบถ้วนของข้อมูลรายสถานี × รายเดือน (Data Completeness Matrix)")
        st.markdown(
            "ตารางแสดงสถานะความครบถ้วนของข้อมูลรายเดือนของสถานีทั้งหมด 50 สถานี โดยแยกแยะอย่างชัดเจนระหว่าง "
            "**Missing Rows (ไม่มีแถวข้อมูลบันทึกในเดือนนั้น)** และ **Missing Values (มีแถวข้อมูลแต่ตัวแปรมีค่าว่าง)**"
        )

        grid_df = summary["grid_matrix"].copy()
        # กรองตามจังหวัด/ปีที่เลือก
        if selected_provinces:
            grid_df = grid_df[grid_df["province_clean"].isin(selected_provinces) | grid_df["province_clean"].isna()]
        if selected_years:
            grid_df = grid_df[grid_df["year"].isin(selected_years)]
        if selected_stations:
            grid_df = grid_df[grid_df["STA_TH"].isin(selected_stations)]

        # รหัสสีตามสถานะ:
        # มีข้อมูลสมบูรณ์ -> เขียว (2)
        # ค่าฝนเท่ากับ 0 -> ฟ้า (1)
        # ค่าฝนสูญหาย (Missing Value) -> ส้ม (0)
        # ไม่มีแถวข้อมูล (Missing Row) -> เทา (-1)
        status_code_map = {
            "มีข้อมูลสมบูรณ์ (Valid)": 3,
            "ค่าฝนเท่ากับ 0 (ตรวจสอบแล้ว)": 2,
            "ค่าฝนสูญหาย (Missing Value)": 1,
            "ไม่มีแถวข้อมูล (Missing Row)": 0
        }
        grid_df["status_code"] = grid_df["status"].map(status_code_map)
        grid_df["year_month"] = grid_df["year"].astype(str) + "-" + grid_df["month"].astype(str).str.zfill(2)

        # ทำ Pivot Table สำหรับ Heatmap
        heatmap_matrix = grid_df.pivot(index="STA_TH", columns="year_month", values="status_code")
        heatmap_labels = grid_df.pivot(index="STA_TH", columns="year_month", values="status")

        # Custom colorscale: [0=Missing Row (แดงสลัว/เทา), 1=Missing Val (ส้ม), 2=Zero (ฟ้าอ่อน), 3=Valid (เขียว)]
        colorscale = [
            [0.0, "#f87171"],   # แดงอ่อน: Missing Row
            [0.25, "#f87171"],
            [0.25, "#fbbf24"],  # ส้มเหลือง: Missing Value
            [0.5, "#fbbf24"],
            [0.5, "#67e8f9"],   # ฟ้า: Zero Rain
            [0.75, "#67e8f9"],
            [0.75, "#4ade80"],  # เขียว: Valid Data
            [1.0, "#4ade80"]
        ]

        fig_heat = go.Figure(data=go.Heatmap(
            z=heatmap_matrix.values,
            x=heatmap_matrix.columns,
            y=heatmap_matrix.index,
            text=heatmap_labels.values,
            hoverinfo="text+x+y",
            colorscale=colorscale,
            showscale=False
        ))

        fig_heat.update_layout(
            title="ความครบถ้วนของข้อมูลรายสถานี-เดือน (เขียว=มีข้อมูล, ฟ้า=ฝนเป็น 0, ส้ม=ค่าว่าง, แดง=ไม่มีแถวข้อมูล)",
            xaxis_title="ปี-เดือน",
            yaxis_title="ชื่อสถานีตรวจวัด",
            yaxis=dict(tickfont=dict(size=10)),
            margin=dict(l=150, r=40, t=50, b=50),
            height=max(450, len(heatmap_matrix) * 16)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # Legend สรุปสถานะ
        c_leg1, c_leg2, c_leg3, c_leg4 = st.columns(4)
        with c_leg1:
            st.markdown("🟢 **มีข้อมูลสมบูรณ์ (Valid):** มีแถวและค่าตัวแปรพร้อมใช้งาน")
        with c_leg2:
            st.markdown("🔵 **ค่าฝนเท่ากับ 0 (Zero Rain):** บันทึกค่าฝนเป็น 0.0 มม.")
        with c_leg3:
            st.markdown("🟠 **ค่าฝนสูญหาย (Missing Value):** มีแถวข้อมูลแต่ค่าฝนเป็น NaN (พบ 7 ค่า)")
        with c_leg4:
            st.markdown("🔴 **ไม่มีแถวข้อมูล (Missing Row):** สถานียังไม่ติดตั้งหรือหยุดบันทึก (พบ 217 สถานี–เดือน)")

    # -------------------------------------------------------------
    # มุมมองที่ 3: เปรียบเทียบสถานีในจังหวัดเดียวกัน
    # -------------------------------------------------------------
    with tab_view3:
        st.markdown(f"##### การกระจายตัวและเปรียบเทียบระหว่างสถานี: {selected_var_info['label']}")
        
        render_notice_box(
            text="กราฟนี้แสดงค่าเฉลี่ยของแต่ละสถานีเฉพาะเดือนที่มีข้อมูลจริง "
                 "<strong>ไม่อนุญาตให้นำผลรวมทั้งปีของสถานีที่มีเดือนขาดมาเทียบกับสถานีที่ข้อมูลครบ</strong> "
                 "และไม่สามารถใช้แทนสภาพอากาศของทั้งจังหวัดได้",
            box_type="info"
        )

        # สรุปค่าเฉลี่ยรายสถานีพร้อมนับจำนวนเดือนที่มีข้อมูล
        station_summary = filtered_df.groupby(["STA_TH", "province_clean"], as_index=False).agg(
            mean_val=(val_col, "mean"),
            valid_months=(val_col, "count"),
            source_type=("source_type", "first")
        )

        fig_bar = px.bar(
            station_summary.sort_values(["province_clean", "mean_val"], ascending=[True, False]),
            x="STA_TH",
            y="mean_val",
            color="province_clean",
            hover_data=["valid_months", "source_type"],
            labels={
                "STA_TH": "สถานีตรวจวัด",
                "mean_val": f"ค่าเฉลี่ย ({selected_var_info['unit']})",
                "province_clean": "จังหวัด",
                "valid_months": "จำนวนเดือนที่มีข้อมูล",
                "source_type": "แหล่งข้อมูล"
            },
            title=f"ค่าเฉลี่ย {selected_var_info['label']} รายสถานี (แยกตามจังหวัด)"
        )
        fig_bar.update_layout(
            xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
            margin=dict(l=40, r=40, t=50, b=80),
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------------------------------------
    # มุมมองที่ 4: ทะเบียนสถานีและพิกัด
    # -------------------------------------------------------------
    with tab_view4:
        st.markdown("##### ทะเบียนสถานีตรวจวัดสภาพอากาศบนพื้นที่สูง 50 สถานี")
        
        station_dir = df.groupby(["STA_TH", "province_clean"], as_index=False).agg(
            amphoe=("AMPHOE", "first"),
            tambon=("TAMBON", "first"),
            lat=("LAT", "first"),
            long=("LONG", "first"),
            source_type=("source_type", "first"),
            total_records=("year", "count"),
            valid_rain_records=("rainfall_mm", lambda s: s.notna().sum()),
            source_detail=("DATA SOURCE", "first")
        )
        
        # จัดรูปแบบพิกัด
        station_dir["lat"] = pd.to_numeric(station_dir["lat"], errors="coerce").round(4)
        station_dir["long"] = pd.to_numeric(station_dir["long"], errors="coerce").round(4)

        # กรองตามที่เลือก
        display_dir = station_dir[station_dir["province_clean"].isin(selected_provinces)].copy()
        if selected_stations:
            display_dir = display_dir[display_dir["STA_TH"].isin(selected_stations)]

        st.dataframe(
            display_dir.rename(columns={
                "STA_TH": "ชื่อสถานีตรวจวัด",
                "province_clean": "จังหวัด",
                "amphoe": "อำเภอ",
                "tambon": "ตำบล",
                "lat": "ละติจูด (Lat)",
                "long": "ลองจิจูด (Long)",
                "source_type": "ประเภทแหล่งข้อมูล",
                "total_records": "จำนวนแถวข้อมูล",
                "valid_rain_records": "แถวฝนที่ใช้ได้",
                "source_detail": "รายละเอียดแหล่งที่มา"
            }),
            use_container_width=True,
            hide_index=True
        )

    # 6. Source & Limitations Footer
    render_source_footer(
        sources=[
            "<strong>สถาบันวิจัยและพัฒนาพื้นที่สูง (องค์การมหาชน) - HRDI:</strong> สถานีตรวจวัดสภาพอากาศภาคพื้นดินบนพื้นที่สูง (HRDI Weather Station) จำนวน 100 ระเบียน",
            "<strong>OpenWeatherMap (OWM):</strong> ข้อมูลภูมิอากาศสังเคราะห์/แบบจำลองเสริมในจุดสถานีโครงการหลวง จำนวน 883 ระเบียน",
            "<strong>หน่วยวัดตัวแปร:</strong> ปริมาณฝนระบุเป็น 'หน่วยรอยืนยัน (คาดการณ์ mm)', อุณหภูมิ (°C), ความชื้น (%), ความเร็วลม (m/s)"
        ],
        limitations=[
            "ข้อมูลสถานีตรวจวัดไม่ใช่ตัวแทนค่าเฉลี่ยของทั้งจังหวัด เป็นเพียงสภาพอากาศเฉพาะจุดบนพื้นที่สูง",
            "มี Missing Rows จำนวน 217 แถว (18.08% ของเมทริกซ์ 50 สถานี × 24 เดือน) เนื่องจากสถานีเริ่มบันทึกไม่พร้อมกัน",
            "มี Missing Values ของค่าฝนจำนวน 7 แถว",
            "ตัวแปร PM2.5 มีข้อมูลเพียง 99 แถว ไม่ครบถ้วนเพียงพอสำหรับการวิเคราะห์เปรียบเทียบเชิงเวลา"
        ]
    )
