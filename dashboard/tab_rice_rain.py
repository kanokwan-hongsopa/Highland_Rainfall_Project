"""
Highland Rainfall Project - Tab B: Rice vs Rain Analysis
แท็บ B: การวิเคราะห์ความสัมพันธ์ระหว่างฝนกับผลผลิตข้าวนาปี (5 จังหวัด, 25 ตำบล Balanced Panel)
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
    load_rice_tambon_data,
    load_province_changes_data,
    load_correlations_data,
    load_sensitivity_reports,
    load_tambon_geo_mapping,
    get_within_tambon_changes,
    PROVINCE_NAMES,
)


def render_tab_rice_rain():
    """
    ฟังก์ชันหลักสำหรับแสดงผล แท็บ B: ฝนกับผลผลิตข้าวนาปี
    """
    rice_df = load_rice_tambon_data()
    prov_changes_df = load_province_changes_data()
    corr_df = load_correlations_data()
    sens_reports = load_sensitivity_reports()
    geo_df = load_tambon_geo_mapping()
    diff_df = get_within_tambon_changes(rice_df, geo_df)

    # 1. ส่วนหัว
    render_header(
        title="🌾 การวิเคราะห์ความสัมพันธ์ระหว่างฝนกับผลผลิตข้าวนาปี (5 จังหวัด)",
        subtitle="สำรวจข้อมูลกลุ่มตัวอย่าง Balanced Panel 25 ตำบลที่มีข้อมูลครบทั้งสองปี (2022–2023) และเปรียบเทียบกับฝนช่วง ก.พ.–ก.ค.",
        badges=[
            {"text": "กลุ่มตัวอย่าง: 25 ตำบล (Balanced Panel)", "class": ""},
            {"text": "5 จังหวัด (50 ระเบียนตำบล–ปี)", "class": ""},
            {"text": "ช่วงฝน: ก.พ.–ก.ค. (ช่วงข้อมูลครบ)", "class": "scope-badge-purple"},
            {"text": "ประเภทการวิเคราะห์: เชิงสำรวจ (Non-causal)", "class": "scope-badge-amber"},
            {"text": "สถานะหน่วย: หน่วยรอยืนยัน", "class": "scope-badge-amber"}
        ]
    )

    # คำเตือนสำคัญประจำแท็บ
    render_notice_box(
        text="<strong>ข้อจำกัดและข้อควรระวังทางสถิติที่สำคัญ:</strong><br/>"
             "1. <strong>ห้ามตีความเชิงเหตุและผล:</strong> ค่าสหสัมพันธ์ที่ติดลบเป็นเพียงการสำรวจความสัมพันธ์ทางสถิติจากข้อมูล 2 ปี "
             "ไม่สามารถอ้างว่าการลดลงของฝนเป็นสาเหตุให้ผลผลิตเพิ่มขึ้น หรือทำนายผลผลิตในอนาคตได้<br/>"
             "2. <strong>การเป็นตัวแทนพื้นที่:</strong> กลุ่มตัวอย่าง 25 ตำบลใน 5 จังหวัดนี้ "
             "<strong>ไม่ใช่ตัวแทนของพื้นที่สูงทั้ง 9 จังหวัด</strong> และเชียงใหม่ครองสัดส่วนถึง 56% (14 จาก 25 ตำบล)<br/>"
             "3. <strong>ความตรงกับฤดูปลูกและหน่วยวัด:</strong> ช่วง ก.พ.–ก.ค. เป็นช่วงที่ข้อมูลฝนสถานีมีความครบถ้วน "
             "<em>ยังไม่ได้รับการยืนยันว่าเป็นฤดูปลูกข้าวนาปีจริง</em> และหน่วยวัดของฝนและผลผลิตต่อพื้นที่ยังรอการยืนยันจากเอกสารต้นทาง<br/>"
             "4. <strong>ระดับข้อมูล HII:</strong> ฝน HII เป็นข้อมูลระดับจังหวัด ห้ามนับค่า HII ที่ซ้ำกันในหลายตำบลเป็นตัวอย่างอิสระ",
        box_type="danger",
        title="ข้อกำหนดจริยธรรมข้อมูลและข้อจำกัดการแปลผล"
    )

    # 2. แถบตัวกรอง (Filters Section)
    with st.expander("🔍 ตัวกรองการวิเคราะห์ข้าวนาปีและฝน (Rice & Rain Filters)", expanded=True):
        col_f1, col_f2, col_f3 = st.columns([1.2, 2.0, 1.8])

        with col_f1:
            year_mode = st.selectbox(
                "ช่วงปีที่วิเคราะห์:",
                ["เปรียบเทียบทั้งสองปี (2022 vs 2023)", "เฉพาะปี 2022", "เฉพาะปี 2023"],
                index=0,
                help="การวิเคราะห์การเปลี่ยนแปลงและสหสัมพันธ์ต้องใช้ข้อมูลทั้ง 2 ปี"
            )

        with col_f2:
            all_provinces = sorted(rice_df["province_name"].unique().tolist())
            selected_provinces = st.multiselect(
                "เลือกจังหวัด (Provinces):",
                options=all_provinces,
                default=all_provinces,
                help="เลือกจังหวัดที่ต้องการดูข้อมูล (ค่าเริ่มต้นเลือกครบ 5 จังหวัด)"
            )

        with col_f3:
            rain_source_option = st.radio(
                "เลือกแหล่งข้อมูลฝนเปรียบเทียบ:",
                ["ฝน HRDI (สถานี/ตำบล)", "ฝน HII (ระดับจังหวัด)"],
                index=0,
                horizontal=True,
                help="HRDI คือฝนจากสถานีโครงการหลวงในตำบล; HII คือข้อมูลฝนสะสมระดับจังหวัดของ สสน."
            )

        col_btn1, col_btn2 = st.columns([1, 5])
        with col_btn1:
            if st.button("🔄 รีเซ็ตตัวกรอง", key="btn_reset_rice", use_container_width=True):
                st.rerun()

    # กรองข้อมูล
    filtered_rice = rice_df[rice_df["province_name"].isin(selected_provinces)].copy()
    filtered_diff = diff_df[diff_df["province_name"].isin(selected_provinces)].copy()
    filtered_prov_changes = prov_changes_df[prov_changes_df["province_name"].isin(selected_provinces)].copy()

    # จัดการกรณีไม่พบข้อมูล
    if filtered_rice.empty or filtered_diff.empty:
        render_empty_state(
            message="ไม่พบข้อมูลตามเงื่อนไขจังหวัดที่เลือก",
            suggestion="กรุณาเลือกอย่างน้อยหนึ่งจังหวัด หรือกดปุ่ม 'รีเซ็ตตัวกรอง' เพื่อแสดงผลกลุ่มตัวอย่างเต็ม"
        )
        return

    # 3. KPI Cards
    st.markdown("#### 📊 ข้อมูลกลุ่มตัวอย่าง Balanced Panel และสรุปทิศทาง")
    kpi_c1, kpi_c2, kpi_c3, kpi_c4, kpi_c5 = st.columns(5)

    sel_tambons = filtered_diff["tambon_code_6"].nunique()
    sel_provinces_cnt = filtered_diff["province_name"].nunique()
    
    # นับทิศทางผลผลิต
    yield_inc = (filtered_diff["delta_yield"] > 0).sum()
    yield_dec = (filtered_diff["delta_yield"] < 0).sum()
    yield_zero = (filtered_diff["delta_yield"] == 0).sum()
    
    # ทิศทางฝน
    rain_col = "delta_hrdi" if "HRDI" in rain_source_option else "delta_hii"
    rain_dec = (filtered_diff[rain_col] < 0).sum()

    with kpi_c1:
        render_metric_card(
            title="จำนวนตำบลวิเคราะห์",
            value=f"{sel_tambons}",
            subtext=f"จาก Balanced Panel 25 ตำบล ({round(sel_tambons/25*100)}%)"
        )
    with kpi_c2:
        render_metric_card(
            title="จำนวนจังหวัด",
            value=f"{sel_provinces_cnt}",
            subtext="จาก 5 จังหวัดที่มีข้อมูลครบ"
        )
    with kpi_c3:
        render_metric_card(
            title="ระเบียนตำบล–ปี",
            value=f"{len(filtered_rice)}",
            subtext=f"ปี 2022 และ 2023 (ครบ 100%)"
        )
    with kpi_c4:
        render_metric_card(
            title="ทิศทางผลผลิต (2023 - 2022)",
            value=f"+{yield_inc} | -{yield_dec}",
            subtext=f"เพิ่มขึ้น {yield_inc}, ลดลง {yield_dec}, คงที่ {yield_zero}",
            delta="กระจายตัวทั้งสองทิศทาง",
            delta_color="normal"
        )
    with kpi_c5:
        src_label = "HRDI" if "HRDI" in rain_source_option else "HII"
        render_metric_card(
            title=f"ทิศทางฝน {src_label} (ก.พ.–ก.ค.)",
            value=f"ลดลง {rain_dec}/{sel_tambons}",
            subtext=f"ลดลง 100% ในทุกตำบล",
            delta="ลดลงทั้งกลุ่มตัวอย่าง",
            delta_color="amber"
        )

    st.markdown("---")

    # 4. Tab Views
    tab_view1, tab_view2, tab_view3, tab_view4 = st.tabs([
        "📊 การกระจายตัวกลุ่มตัวอย่างและการเปรียบเทียบระหว่างปี",
        "🔍 Scatter การเปลี่ยนแปลงระดับตำบล (n=25)",
        "🗺️ Scatter การเปลี่ยนแปลงระดับจังหวัด (n=5)",
        "📋 สหสัมพันธ์ Spearman และการทดสอบความไว (Sensitivity)"
    ])

    # -------------------------------------------------------------
    # มุมมองที่ 1: การกระจายตัวและเปรียบเทียบระหว่างปี
    # -------------------------------------------------------------
    with tab_view1:
        st.markdown("##### โครงสร้างกลุ่มตัวอย่างรายจังหวัดและการเปรียบเทียบค่า 2022 vs 2023")
        
        col_g1, col_g2 = st.columns([1.8, 2.2])

        with col_g1:
            # กราฟแท่งแสดงการกระจายตัวตำบลรายจังหวัด (ชี้ให้เห็นเชียงใหม่ 56%)
            prov_dist = filtered_diff.groupby("province_name", as_index=False).agg(
                tambon_count=("tambon_code_6", "count")
            ).sort_values("tambon_count", ascending=False)
            prov_dist["percentage"] = (prov_dist["tambon_count"] / 25 * 100).round(1)

            fig_dist = px.bar(
                prov_dist,
                x="province_name",
                y="tambon_count",
                text="tambon_count",
                labels={"province_name": "จังหวัด", "tambon_count": "จำนวนตำบลที่ศึกษาวิจัย"},
                title="จำนวนตำบลในกลุ่มตัวอย่าง Balanced Panel (เชียงใหม่ 14 จาก 25 ตำบล = 56%)",
                color="province_name"
            )
            fig_dist.update_traces(textposition="outside")
            fig_dist.update_layout(showlegend=False, margin=dict(l=40, r=40, t=50, b=40))
            st.plotly_chart(fig_dist, use_container_width=True)

        with col_g2:
            # กราฟเปรียบเทียบผลผลิตเฉลี่ยและฝนเฉลี่ยรายจังหวัดระหว่าง 2 ปี
            p_comp = filtered_rice.groupby(["province_name", "year"], as_index=False).agg(
                mean_yield=("rice_yield_per_harvest_area", "mean"),
                mean_hrdi=("hrdi_feb_jul", "mean"),
                mean_hii=("hii_feb_jul", "mean")
            )
            p_comp["year"] = p_comp["year"].astype(str)

            val_to_plot = "mean_yield"
            val_title = "ผลผลิตต่อพื้นที่เก็บเกี่ยวเฉลี่ย (หน่วยรอยืนยัน)"
            if "HII" in rain_source_option:
                val_to_plot = "mean_hii"
                val_title = "ฝน HII เฉลี่ย ก.พ.–ก.ค. (นิยามและหน่วยรอยยืนยัน)"
            elif "HRDI" in rain_source_option and st.checkbox("แสดงฝน HRDI แทนผลผลิต", value=False):
                val_to_plot = "mean_hrdi"
                val_title = "ฝน HRDI เฉลี่ย ก.พ.–ก.ค. (หน่วยรอยืนยัน)"

            fig_pcomp = px.bar(
                p_comp,
                x="province_name",
                y=val_to_plot,
                color="year",
                barmode="group",
                labels={"province_name": "จังหวัด", val_to_plot: val_title, "year": "ปี"},
                title=f"เปรียบเทียบ {val_title} ระหว่างปี 2022 กับ 2023",
                color_discrete_map={"2022": "#0284c7", "2023": "#f59e0b"}
            )
            fig_pcomp.update_layout(margin=dict(l=40, r=40, t=50, b=40))
            st.plotly_chart(fig_pcomp, use_container_width=True)

        st.markdown("##### กราฟเปรียบเทียบผลผลิตรายตำบลระหว่างปี 2022 กับ 2023 (ตำบลเดิม)")
        
        # Slope chart / Paired dot chart รายตำบล
        fig_paired = go.Figure()
        for idx, row in filtered_diff.iterrows():
            fig_paired.add_trace(go.Scatter(
                x=["2022", "2023"],
                y=[row["yield_2022"], row["yield_2023"]],
                mode="lines+markers",
                name=row["label"],
                hoverinfo="text",
                hovertext=f"<b>{row['label']}</b><br>ปี 2022: {row['yield_2022']:.2f}<br>ปี 2023: {row['yield_2023']:.2f}<br>ผลต่าง: {row['delta_yield']:+.2f}",
                line=dict(
                    color="#16a34a" if row["delta_yield"] > 0 else ("#dc2626" if row["delta_yield"] < 0 else "#94a3b8"),
                    width=2
                ),
                marker=dict(size=7),
                showlegend=False
            ))

        fig_paired.update_layout(
            title="การเปลี่ยนแปลงผลผลิตต่อพื้นที่เก็บเกี่ยวรายตำบล (เขียว=เพิ่มขึ้น 10 ตำบล, แดง=ลดลง 10 ตำบล, เทา=เท่าเดิม 5 ตำบล)",
            xaxis_title="ปีที่เก็บข้อมูล",
            yaxis_title="ผลผลิตต่อพื้นที่เก็บเกี่ยว (หน่วยรอยืนยัน)",
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_paired, use_container_width=True)

    # -------------------------------------------------------------
    # มุมมองที่ 2: Scatter การเปลี่ยนแปลงระดับตำบล (n=25)
    # -------------------------------------------------------------
    with tab_view2:
        st.markdown("##### ความสัมพันธ์เชิงสำรวจระดับตำบล: การเปลี่ยนแปลงฝน HRDI vs การเปลี่ยนแปลงผลผลิตข้าวนาปี")

        # ตรวจสอบว่าผู้ใช้เลือกโหมดปีเดี่ยวหรือไม่
        if "เฉพาะปี" in year_mode:
            render_notice_box(
                text=f"คุณเลือกมุมมอง '{year_mode}' อยู่ แต่การวิเคราะห์การเปลี่ยนแปลง (Δ) และสหสัมพันธ์อันดับ Spearman "
                     "<strong>จำเป็นต้องใช้ข้อมูลทั้งปี 2022 และ 2023 ร่วมกัน</strong> (คำนวณผลต่าง 2023 ลบ 2022) "
                     "กราฟ Scatter ด้านล่างจึงยังคงใช้ข้อมูลผลต่างของทั้งสองปี",
                box_type="warning"
            )

        # ตรวจสอบการเลือกจังหวัดเดียวเพื่อป้องกันความเข้าใจผิดเรื่อง rho
        is_single_prov = sel_provinces_cnt == 1
        if is_single_prov:
            render_notice_box(
                text=f"<strong>ข้อควรระวัง:</strong> ปัจจุบันคุณเลือกดูเฉพาะ <strong>{selected_provinces[0]}</strong> ({sel_tambons} ตำบล) "
                     "ค่าสหสัมพันธ์ Spearman $\\rho = -0.173427$ ที่แสดงเป็น<strong>ค่าอ้างอิงของกลุ่มตัวอย่างเต็ม 25 ตำบล (5 จังหวัด)</strong> "
                     "ระบบไม่ได้คำนวณค่า $\\rho$ ใหม่จากจังหวัดที่เลือก เนื่องจากจำนวนจุดน้อยเกินกว่าจะประเมินได้อย่างมีนัยสำคัญ",
                box_type="warning"
            )

        # Plotly Scatter ระดับตำบล
        fig_scatter_t = px.scatter(
            filtered_diff,
            x="delta_hrdi",
            y="delta_yield",
            color="province_name",
            symbol="yield_change_direction",
            hover_name="label",
            hover_data={
                "delta_hrdi": ":.2f",
                "delta_yield": ":.2f",
                "yield_2022": ":.2f",
                "yield_2023": ":.2f",
                "hrdi_2022": ":.2f",
                "hrdi_2023": ":.2f"
            },
            labels={
                "delta_hrdi": "การเปลี่ยนแปลงฝน HRDI ก.พ.–ก.ค. (2023 ลบ 2022) [หน่วยรอยืนยัน]",
                "delta_yield": "การเปลี่ยนแปลงผลผลิตต่อพื้นที่เก็บเกี่ยว (2023 ลบ 2022) [หน่วยรอยืนยัน]",
                "province_name": "จังหวัด",
                "yield_change_direction": "ทิศทางผลผลิต"
            },
            title="Scatter Plot ระดับตำบล: Δ ฝน HRDI vs Δ ผลผลิตข้าวนาปี (n=25 จุด)"
        )

        # เพิ่มเส้นประอ้างอิง x=0 และ y=0
        fig_scatter_t.add_vline(x=0, line_dash="dash", line_color="#94a3b8", line_width=1)
        fig_scatter_t.add_hline(y=0, line_dash="dash", line_color="#94a3b8", line_width=1)

        # ปรับแต่งเส้นประ Trend line เชิงสำรวจ (OLS สำหรับแสดงทิศทางเท่านั้น)
        fig_scatter_t.update_traces(marker=dict(size=11, line=dict(width=1, color="#334155")))
        fig_scatter_t.update_layout(
            margin=dict(l=40, r=40, t=50, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_scatter_t, use_container_width=True)

        # กล่องสรุปค่าสถิติ Spearman ระดับตำบล
        col_st1, col_st2 = st.columns([1.5, 2.5])
        with col_st1:
            render_metric_card(
                title="Spearman rho (ระดับตำบล)",
                value="-0.1734",
                subtext="กลุ่มตัวอย่างเต็ม n = 25 ตำบล",
                delta="ความสัมพันธ์ระดับต่ำมาก (Weak Negative)",
                delta_color="normal"
            )
        with col_st2:
            st.markdown("""
                **ข้อสังเกตเชิงสถิติ:**
                - ค่า $\\rho = -0.173427$ บ่งชี้ความสัมพันธ์อันดับที่แผ่วเบามาก (Weak Negative)
                - ฝนช่วง ก.พ.–ก.ค. ลดลงในทุกตำบล (จุดทั้งหมดอยู่ฝั่ง ΔRain < 0)
                - ในขณะที่ผลผลิตข้าวมีทั้งเพิ่มขึ้น (10 ตำบล) ลดลง (10 ตำบล) และไม่เปลี่ยน (5 ตำบล) จึงไม่พบลักษณะความสัมพันธ์ที่ชัดเจนในระดับตำบล
            """)

    # -------------------------------------------------------------
    # มุมมองที่ 3: Scatter การเปลี่ยนแปลงระดับจังหวัด (n=5)
    # -------------------------------------------------------------
    with tab_view3:
        st.markdown("##### ความสัมพันธ์เชิงสำรวจระดับจังหวัด: การเปลี่ยนแปลงฝน (HRDI / HII) vs การเปลี่ยนแปลงผลผลิตเฉลี่ย (n=5)")
        
        render_notice_box(
            text="<strong>ข้อพึงระวังขั้นวิกฤต (Critical Limitation):</strong><br/>"
                 "• ขนาดตัวอย่างระดับจังหวัดมีเพียง <strong>n = 5 จังหวัด</strong> ซึ่งมีขนาดเล็กมากทางสถิติ<br/>"
                 "• <strong>ห้ามสรุปว่าข้อมูล HII แม่นยำหรือทำนายได้ดีกว่า HRDI</strong> จากค่า $\\rho = -0.9$ เพียงอย่างเดียว "
                 "เพราะขนาดตัวอย่าง 5 จุดมีความไวสูงมาก (Sensitive) ต่อการสลับหรือตัดจังหวัดออกเพียงแห่งเดียว<br/>"
                 "• ค่าฝน HII เป็นค่ารวมระดับจังหวัด จึงแสดงในระดับจังหวัดนี้เท่านั้น ไม่นำไปนับซ้ำในระดับตำบล",
            box_type="danger",
            title="ข้อควรระวังการเปรียบเทียบระดับจังหวัด (n=5)"
        )

        col_sc1, col_sc2 = st.columns(2)

        # ฝน HRDI ระดับจังหวัด
        with col_sc1:
            st.markdown("###### กราฟ 1: ฝน HRDI (เฉลี่ยสถานีในจังหวัด) vs ผลผลิตเฉลี่ย")
            fig_p_hrdi = px.scatter(
                filtered_prov_changes,
                x="mean_hrdi_change",
                y="mean_yield_change",
                text="province_name",
                hover_data=["tambons"],
                labels={
                    "mean_hrdi_change": "Δ ฝน HRDI เฉลี่ย (2023 ลบ 2022) [หน่วยรอยืนยัน]",
                    "mean_yield_change": "Δ ผลผลิตเฉลี่ย (2023 ลบ 2022) [หน่วยรอยืนยัน]",
                    "province_name": "จังหวัด",
                    "tambons": "จำนวนตำบล"
                },
                title="ระดับจังหวัด: Δ ฝน HRDI vs Δ ผลผลิต (rho = -0.7000, n=5)"
            )
            fig_p_hrdi.update_traces(textposition="top center", marker=dict(size=14, color="#0284c7"))
            fig_p_hrdi.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
            fig_p_hrdi.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
            fig_p_hrdi.update_layout(margin=dict(l=40, r=40, t=50, b=40))
            st.plotly_chart(fig_p_hrdi, use_container_width=True)

            render_metric_card(
                title="Spearman rho (HRDI จังหวัด)",
                value="-0.7000",
                subtext="ขนาดตัวอย่าง n = 5 จังหวัด",
                delta="อ้างอิงจาก 5 จังหวัด",
                delta_color="normal"
            )

        # ฝน HII ระดับจังหวัด
        with col_sc2:
            st.markdown("###### กราฟ 2: ฝน HII (สสน. ระดับจังหวัด) vs ผลผลิตเฉลี่ย")
            fig_p_hii = px.scatter(
                filtered_prov_changes,
                x="hii_change",
                y="mean_yield_change",
                text="province_name",
                hover_data=["tambons"],
                labels={
                    "hii_change": "Δ ฝน HII (2023 ลบ 2022) [นิยามและหน่วยรอยืนยัน]",
                    "mean_yield_change": "Δ ผลผลิตเฉลี่ย (2023 ลบ 2022) [หน่วยรอยืนยัน]",
                    "province_name": "จังหวัด",
                    "tambons": "จำนวนตำบล"
                },
                title="ระดับจังหวัด: Δ ฝน HII vs Δ ผลผลิต (rho = -0.9000, n=5)"
            )
            fig_p_hii.update_traces(textposition="top center", marker=dict(size=14, color="#0d9488"))
            fig_p_hii.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
            fig_p_hii.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
            fig_p_hii.update_layout(margin=dict(l=40, r=40, t=50, b=40))
            st.plotly_chart(fig_p_hii, use_container_width=True)

            render_metric_card(
                title="Spearman rho (HII จังหวัด)",
                value="-0.9000",
                subtext="ขนาดตัวอย่าง n = 5 จังหวัด",
                delta="อ้างอิงจาก 5 จังหวัด",
                delta_color="normal"
            )

    # -------------------------------------------------------------
    # มุมมองที่ 4: สหสัมพันธ์ Spearman และ Sensitivity Analysis
    # -------------------------------------------------------------
    with tab_view4:
        st.markdown("##### ตารางค่าสหสัมพันธ์อันดับ Spearman เชิงสำรวจ (Exploratory Correlations)")
        
        # แสดงตาราง Correlations จาก CSV จริง
        corr_display = corr_df.copy()
        corr_display["analysis_label"] = corr_display["analysis"].map({
            "HRDI_tambon": "ฝน HRDI ระดับตำบล (Tambon-level)",
            "HRDI_province": "ฝน HRDI ระดับจังหวัด (Province-level)",
            "HII_province": "ฝน HII ระดับจังหวัด (Province-level)"
        }).fillna(corr_display["analysis"])

        st.dataframe(
            corr_display[[
                "analysis_label", "n", "spearman_rho", "analysis_type",
                "causal_interpretation_allowed", "rain_window",
                "crop_season_verified", "source_units_verified"
            ]].rename(columns={
                "analysis_label": "การวิเคราะห์",
                "n": "ขนาดตัวอย่าง (n)",
                "spearman_rho": "Spearman rho",
                "analysis_type": "ประเภทการวิเคราะห์",
                "causal_interpretation_allowed": "อนุญาตตีความเหตุผล?",
                "rain_window": "ช่วงฝน",
                "crop_season_verified": "ยืนยันฤดูปลูกแล้ว?",
                "source_units_verified": "ยืนยันหน่วยแล้ว?"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("##### การทดสอบความไว: ตัดจังหวัดออกทีละแห่ง (Leave-One-Province-Out Sensitivity)")
        st.markdown(
            "การทดสอบความไวเพื่อประเมินว่าค่า $\\rho$ เปลี่ยนแปลงไปอย่างไรเมื่อตัดจังหวัดใดจังหวัดหนึ่งออก "
            "ผลลัพธ์แสดงให้เห็นว่าผลการวิเคราะห์มีความอ่อนไหวสูงมากต่อการเลือกตัวอย่าง:"
        )

        lopo_df = sens_reports.get("leave_one_province_out")
        if lopo_df is not None and not lopo_df.empty:
            st.dataframe(
                lopo_df[[
                    "excluded_province_name", "tambons", "hrdi_tambon_rho",
                    "hrdi_province_rho", "hii_province_rho"
                ]].rename(columns={
                    "excluded_province_name": "จังหวัดที่ตัดออก",
                    "tambons": "จำนวนตำบลที่เหลือ",
                    "hrdi_tambon_rho": "rho HRDI ตำบล",
                    "hrdi_province_rho": "rho HRDI จังหวัด",
                    "hii_province_rho": "rho HII จังหวัด"
                }),
                use_container_width=True,
                hide_index=True
            )
            st.markdown("""
                - **ช่วงการเปลี่ยนแปลง $\\rho$ เมื่อตัดจังหวัดออก:**
                  - HRDI ตำบล: $\\rho$ เปลี่ยนแปลงอยู่ในช่วง **-0.5285 ถึง +0.0303** (สามารถเปลี่ยนจากลบเป็นบวกได้เมื่อตัดเชียงใหม่ออก)
                  - HRDI จังหวัด: $\\rho$ เปลี่ยนแปลงอยู่ในช่วง **-1.0000 ถึง -0.4000**
                  - HII จังหวัด: $\\rho$ เปลี่ยนแปลงอยู่ในช่วง **-1.0000 ถึง -0.8000**
            """)
        else:
            st.info("ไม่มีไฟล์รายงาน Leave-one-province-out")

        # Yield flag sensitivity
        yflag_df = sens_reports.get("yield_flag_sensitivity")
        if yflag_df is not None and not yflag_df.empty:
            st.markdown("##### การทดสอบความไว: รายการที่ติดธงคุณภาพพื้นที่ (Yield Flag Sensitivity)")
            st.dataframe(
                yflag_df.rename(columns={
                    "scenario": "สถานการณ์ข้อมูล",
                    "tambons": "จำนวนตำบล",
                    "hrdi_tambon_rho": "rho HRDI ตำบล",
                    "hrdi_province_rho": "rho HRDI จังหวัด",
                    "hii_province_rho": "rho HII จังหวัด"
                }),
                use_container_width=True,
                hide_index=True
            )
            st.caption("บนกลุ่ม 24 ตำบลชุดเดียวกัน ค่าสหสัมพันธ์ไม่เปลี่ยนแปลงจากการตัดแถวที่ติดธงคุณภาพพื้นที่ออก")

    # 5. Source & Limitations Footer
    render_source_footer(
        sources=[
            "<strong>กรมส่งเสริมการเกษตร:</strong> ข้อมูลผลผลิตข้าวนาปีและพื้นที่เก็บเกี่ยวระดับตำบล (ปี 2565–2566 / 2022–2023) หน่วยรอยืนยัน",
            "<strong>สถาบันวิจัยและพัฒนาพื้นที่สูง (องค์การมหาชน) - HRDI:</strong> ข้อมูลฝนสะสมสถานีตรวจวัดในตำบลช่วง ก.พ.–ก.ค. หน่วยรอยืนยัน",
            "<strong>สถาบันสารสนเทศทรัพยากรน้ำ (องค์การมหาชน) - HII:</strong> ข้อมูลฝนสะสมรายจังหวัด (AvgRain) ช่วง ก.พ.–ก.ค. นิยามและหน่วยรอยยืนยัน"
        ],
        limitations=[
            "ข้อมูลมีเพียง 2 ปี (2022–2023) จึงวิเคราะห์ได้เฉพาะการเปลี่ยนแปลงเชิงสำรวจเท่านั้น",
            "กลุ่มตัวอย่างมีเพียง 25 ตำบลใน 5 จังหวัด ไม่สามารถใช้เป็นตัวแทนของพื้นที่สูง 9 จังหวัดได้",
            "เชียงใหม่มี 14 จาก 25 ตำบล (56%) ทำให้ผลการวิเคราะห์ในภาพรวมอาจสะท้อนลักษณะเฉพาะของเชียงใหม่เป็นหลัก",
            "ช่วงเดือน กุมภาพันธ์–กรกฎาคม ยังไม่ได้รับการยืนยันว่าเป็นฤดูปลูกข้าวนาปีจริง เป็นเพียงช่วงที่ข้อมูลสถานีมีความครบถ้วน",
            "ขนาดตัวอย่างระดับจังหวัด n = 5 มีขนาดเล็กมาก ไม่สามารถใช้สรุปข้อเปรียบเทียบระหว่าง HRDI และ HII ในเชิงการพยากรณ์ได้",
            "ห้ามนำผลการวิเคราะห์นี้ไปใช้เป็นโมเดลพยากรณ์หรือสรุปผลเชิงนโยบายโดยไม่มีการยืนยันข้อมูลภาคสนามเพิ่มเติม"
        ]
    )
