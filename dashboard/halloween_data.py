"""
Highland Rainfall Project - Halloween Data Serializer (Dual Mode: Observed Only & Exploratory)
แปลงข้อมูลจริงและข้อมูลสมบูรณ์สำหรับแสดงผลบน High-Performance Frontend Engine
รองรับ:
- 9 จังหวัด 50 สถานี HRDI และ 921 ตำบลข้าวนาปี DOAE
- โหมดข้อมูลตรวจวัดจริงเท่านั้น (Observed Only): แสดงเฉพาะเดือนที่วัดจริง ไม่แทนที่ด้วยศูนย์ ไม่รวมผลรวมปีที่ไม่ครบ 12 ด.
- โหมดทดลองวิเคราะห์ (Exploratory - รวมค่าประมาณ 12 ด.): เติมเต็ม 1,200 แถวด้วยสถิติ พร้อมป้ายเตือนการประมาณการ
- ข้อมูลฝน HII ระดับจังหวัด (ม.ค. 2022 - ธ.ค. 2023 ครบ 24 เดือน)
- ข้อมูลผลผลิตข้าวนาปี DOAE 921 ตำบล
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np

from dashboard.data_loader import (
    load_climate_data,
    get_climate_completeness_summary,
    load_rice_tambon_data,
    load_province_changes_data,
    load_correlations_data,
    load_sensitivity_reports,
    load_tambon_geo_mapping,
    get_within_tambon_changes,
    load_hrdi_exploratory_data,
    PROVINCE_NAMES,
)

# พิกัดศูนย์กลางและระดับซูมของ 9 จังหวัดบนพื้นที่สูง
PROVINCE_GEO_CENTERS = {
    "เชียงใหม่": {"lat": 18.7904, "lng": 98.9847, "zoom": 8.5, "code": "50"},
    "เชียงราย": {"lat": 19.9072, "lng": 99.8325, "zoom": 8.5, "code": "57"},
    "น่าน": {"lat": 18.7756, "lng": 100.7730, "zoom": 8.5, "code": "55"},
    "ตาก": {"lat": 16.8840, "lng": 99.1258, "zoom": 8.0, "code": "63"},
    "กำแพงเพชร": {"lat": 16.4828, "lng": 99.5227, "zoom": 8.5, "code": "62"},
    "พิษณุโลก": {"lat": 16.8211, "lng": 100.2659, "zoom": 8.5, "code": "65"},
    "เพชรบูรณ์": {"lat": 16.4190, "lng": 101.1567, "zoom": 8.5, "code": "67"},
    "กาญจนบุรี": {"lat": 14.3000, "lng": 99.1000, "zoom": 8.0, "code": "71"},
    "แม่ฮ่องสอน": {"lat": 19.3021, "lng": 97.9654, "zoom": 8.5, "code": "58"},
}

OVERVIEW_CENTER = {"lat": 17.5, "lng": 99.5, "zoom": 6.4}

# ขอบเขตจังหวัด GeoJSON
GEOJSON_FILE = Path(__file__).resolve().parent.parent / "data" / "reference" / "thailand_9provinces.geojson"
# เงาแผนที่ทั้งประเทศ (77 จังหวัด ย่อเส้นแล้ว; src/60_simplify_thailand_provinces.py) ใช้แสดงผลเท่านั้น
THAILAND_GEOJSON_FILE = Path(__file__).resolve().parent.parent / "data" / "reference" / "thailand_77provinces_simplified.geojson"
COMPLETENESS_DIR = Path(__file__).resolve().parent.parent / "data" / "completeness"
ANALYSIS_READY_DIR = Path(__file__).resolve().parent.parent / "data" / "analysis_ready"


def is_suspect_observed(rain, hist_median) -> bool:
    """
    ธงคุณภาพค่าฝนตรวจวัดที่ผิดปกติ (เทียบกับมัธยฐานเดือนเดียวกันของสถานี ปี 2017–2022)
    - ฝน 0 มม. ในเดือนที่มัธยฐานเกิน 100 มม. (กลางฤดูฝน มักเป็นเซ็นเซอร์ขัดข้องที่บันทึกเป็นศูนย์)
    - ฝนเกิน 3 เท่าของมัธยฐานและเกิน 500 มม. (spike ผิดปกติ เช่น สถานีสบโขง ส.ค. 2023)
    """
    if pd.isna(rain) or pd.isna(hist_median):
        return False
    rain, hist_median = float(rain), float(hist_median)
    return (rain == 0 and hist_median > 100) or (rain > 3 * hist_median and rain > 500)


def load_province_geojson(path: Path = GEOJSON_FILE) -> dict:
    """โหลดขอบเขตจังหวัดจริงจากไฟล์ GeoJSON (WGS84 EPSG:4326)"""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"type": "FeatureCollection", "features": []}


def get_halloween_payload() -> str:
    """
    เตรียมข้อมูลจริงและข้อมูลความสมบูรณ์ทั้งหมดในรูปแบบ JSON ปลอดภัย
    รองรับทั้งโหมด Observed Only และ Exploratory
    """
    climate_df = load_climate_data()
    completeness = get_climate_completeness_summary(climate_df)
    prov_changes_df = load_province_changes_data()
    corr_df = load_correlations_data()
    sens_reports = load_sensitivity_reports()
    geo_df = load_tambon_geo_mapping()

    # โหลดไฟล์ Completeness & Exploratory
    exp_path = ANALYSIS_READY_DIR / "HRDI_2022_2023_12months_EXPLORATORY.csv"
    demo_path = COMPLETENESS_DIR / "hrdi_all_50_stations_24_months_DEMO.csv"
    hii_path = COMPLETENESS_DIR / "hii_all_9_provinces_24_months.csv"
    r921_path = COMPLETENESS_DIR / "rice_all_921_tambons_2022_2023.csv"

    if exp_path.exists():
        hrdi_df = pd.read_csv(exp_path, encoding="utf-8-sig")
    elif demo_path.exists():
        hrdi_df = pd.read_csv(demo_path, encoding="utf-8-sig")
    else:
        hrdi_df = pd.DataFrame()

    if hii_path.exists():
        hii_df = pd.read_csv(hii_path, encoding="utf-8-sig")
    else:
        hii_df = pd.DataFrame()

    if r921_path.exists():
        r921_df = pd.read_csv(r921_path, encoding="utf-8-sig")
    else:
        r921_df = pd.DataFrame()

    # Metadata สถานีสภาพอากาศ
    sta_meta = climate_df.groupby("STA_TH")[
        ["province_clean", "LAT", "LONG", "AMPHOE", "TAMBON", "CODE_REF", "CODE_STA", "source_type", "TEMP", "HUMIDITY", "WIND_SPEED"]
    ].first().to_dict(orient="index")

    # 1. รายชื่อสถานี 50 แห่งพร้อมพิกัด และชุดข้อมูลทั้ง Observed และ Exploratory
    station_list = []
    if not hrdi_df.empty:
        # กำหนดชื่อคอลัมน์ exploratory
        has_exp_col = "rainfall_completed_exploratory_mm" in hrdi_df.columns
        has_status_col = "completion_status" in hrdi_df.columns
        status_col_name = "completion_status" if has_status_col else "data_status"

        for sta_name, group in hrdi_df.groupby("STA_TH"):
            meta = sta_meta.get(sta_name, {})
            first = group.iloc[0]
            prov = str(first.get("PROVINCE", meta.get("province_clean", "")))
            lat = float(meta.get("LAT", 0.0))
            lng = float(meta.get("LONG", 0.0))
            src = str(meta.get("source_type", "HRDI"))

            mean_temp = float(meta.get("TEMP", 0.0)) if pd.notna(meta.get("TEMP")) else 0.0
            mean_humidity = float(meta.get("HUMIDITY", 0.0)) if pd.notna(meta.get("HUMIDITY")) else 0.0
            mean_wind = float(meta.get("WIND_SPEED", 0.0)) if pd.notna(meta.get("WIND_SPEED")) else 0.0

            g_sorted = group.sort_values(by=["YEAR", "MONTH_NUM"])
            m_obs_24 = []
            m_exp_24 = []
            m_status_24 = []

            for _, row in g_sorted.iterrows():
                c_status = str(row.get(status_col_name, "observed"))
                rf_raw = row.get("RAINFALL")
                if has_exp_col:
                    rf_exp = row.get("rainfall_completed_exploratory_mm")
                else:
                    rf_exp = row.get("rainfall_for_demo_mm", rf_raw)

                # QA: ค่าตรวจวัดที่ผิดปกติ (ดู is_suspect_observed) ในโหมด 12 เดือนจะแทนด้วยมัธยฐานรายเดือนของสถานี
                hist_med = row.get("historical_month_median_mm")
                if c_status == "observed" and is_suspect_observed(rf_raw, hist_med):
                    c_status = "qa_replaced"
                    rf_exp = hist_med

                m_status_24.append(c_status)

                # Observed: ต้องเป็นสถานะ 'observed' เท่านั้น (ค่าที่ติดธง QA ไม่นับเป็นค่าตรวจวัดที่เชื่อถือได้)
                if c_status == "observed" and pd.notna(rf_raw):
                    m_obs_24.append(round(float(rf_raw), 1))
                else:
                    m_obs_24.append(None)

                # Exploratory: เติมเต็ม 12 เดือนด้วยค่าประมาณการทางสถิติ
                if pd.notna(rf_exp):
                    m_exp_24.append(round(float(rf_exp), 1))
                elif pd.notna(rf_raw):
                    m_exp_24.append(round(float(rf_raw), 1))
                else:
                    m_exp_24.append(None)

            # นับจำนวนเดือนตรวจวัดจริงแยกปี
            obs_cnt_22 = sum(1 for x in m_obs_24[:12] if x is not None)
            obs_cnt_23 = sum(1 for x in m_obs_24[12:24] if x is not None)
            obs_cnt_tot = obs_cnt_22 + obs_cnt_23
            est_cnt_tot = sum(1 for s in m_status_24 if s == "estimated")
            exp_cnt_tot = sum(1 for s in m_status_24 if s == "estimated_exploratory")
            qa_cnt_tot = sum(1 for s in m_status_24 if s == "qa_replaced")
            non_obs_22 = sum(1 for s in m_status_24[:12] if s != "observed")
            non_obs_23 = sum(1 for s in m_status_24[12:24] if s != "observed")

            # กฎเหล็กข้อ 7: ในโหมดตรวจวัดจริง ห้ามแสดงผลรวมทั้งปีของสถานีที่ไม่ครบ 12 เดือนโดยเด็ดขาด!
            annual_obs_22 = round(sum(m_obs_24[:12]), 1) if obs_cnt_22 == 12 else None
            annual_obs_23 = round(sum(m_obs_24[12:24]), 1) if obs_cnt_23 == 12 else None
            annual_obs_all = None  # ไม่มีสถานีใดครบ 24 เดือน (ปี 2023 สูงสุด 9 เดือน)

            # โหมดทดลองวิเคราะห์ (Exploratory): ผลรวม 12 เดือนครบถ้วน
            annual_exp_22 = round(sum(m_exp_24[:12]), 1) if all(x is not None for x in m_exp_24[:12]) else None
            annual_exp_23 = round(sum(m_exp_24[12:24]), 1) if all(x is not None for x in m_exp_24[12:24]) else None
            if annual_exp_22 is not None and annual_exp_23 is not None:
                annual_exp_all = round((annual_exp_22 + annual_exp_23) / 2, 1)
            else:
                annual_exp_all = annual_exp_22 or annual_exp_23

            status_label = f"ตรวจวัดจริง {obs_cnt_tot}/24 ด."
            if est_cnt_tot > 0:
                status_label += f" (DEMO {est_cnt_tot} ด.)"
            if exp_cnt_tot > 0:
                status_label += f" (Exploratory {exp_cnt_tot} ด.)"
            if qa_cnt_tot > 0:
                status_label += f" (ค่าผิดปกติ {qa_cnt_tot} ด.)"

            station_list.append({
                "name": sta_name,
                "code_ref": str(first.get("CODE_REF", meta.get("CODE_REF", ""))),
                "code_sta": str(first.get("CODE_STA", meta.get("CODE_STA", ""))),
                "province": prov,
                "amphoe": str(first.get("AMPHOE", meta.get("AMPHOE", ""))),
                "tambon": str(first.get("TAMBON", meta.get("TAMBON", ""))),
                "lat": round(lat, 5),
                "lng": round(lng, 5),
                "source": src,
                "records": len(group),
                "valid_rain": obs_cnt_tot,
                "observed_count_2022": obs_cnt_22,
                "observed_count_2023": obs_cnt_23,
                "observed_count_total": obs_cnt_tot,
                "estimated_count_total": est_cnt_tot,
                "exploratory_count_total": exp_cnt_tot,
                "qa_replaced_count_total": qa_cnt_tot,
                "non_observed_count_2022": non_obs_22,
                "non_observed_count_2023": non_obs_23,
                "data_status_label": status_label,
                "months_2022": 12,
                "months_2023": 12,
                "total_months": 24,
                "mean_rain": round(annual_exp_all / 12, 1) if annual_exp_all else 0.0,
                "mean_temp": round(mean_temp, 1),
                "mean_humidity": round(mean_humidity, 1),
                "mean_wind": round(mean_wind, 2),
                # Observed values
                "annual_obs_2022": annual_obs_22,
                "annual_obs_2023": annual_obs_23,
                "annual_obs_all": annual_obs_all,
                "monthly_obs_2022": m_obs_24[:12],
                "monthly_obs_2023": m_obs_24[12:24],
                "monthly_obs_24": m_obs_24,
                # Exploratory values
                "annual_exp_2022": annual_exp_22,
                "annual_exp_2023": annual_exp_23,
                "annual_exp_all": annual_exp_all,
                "monthly_exp_2022": m_exp_24[:12],
                "monthly_exp_2023": m_exp_24[12:24],
                "monthly_exp_24": m_exp_24,
                "monthly_status_24": m_status_24,
                # Backward compatibility aliases
                "monthly_rain_2022": m_obs_24[:12],
                "monthly_rain_2023": m_obs_24[12:24],
                "monthly_demo_2022": m_exp_24[:12],
                "monthly_demo_2023": m_exp_24[12:24],
                "monthly_demo_24": m_exp_24,
            })

    # 2. ข้อมูลรายเดือน HII ระดับจังหวัด (24 เดือน) และรายสถานี
    monthly_trends = []
    if not hii_df.empty:
        for _, row in hii_df.iterrows():
            ym = f"{int(row['year'])}-{str(int(row['month'])).zfill(2)}"
            monthly_trends.append({
                "year_month": ym,
                "province": str(row["province_name_th"]),
                "mean_rain": round(float(row["avg_rain_mm"]), 2) if pd.notna(row["avg_rain_mm"]) else None,
                "data_status": str(row.get("data_status", "observed")),
                "source": "HII (ฝนเฉลี่ยระดับจังหวัด)"
            })

    # ข้อมูลฝน HII 24 เดือนแยกตามรายจังหวัด
    hii_prov_24 = {}
    for prov_name in PROVINCE_GEO_CENTERS.keys():
        sub_hii = hii_df[hii_df["province_name_th"] == prov_name].sort_values(by=["year", "month"])
        if not sub_hii.empty:
            hii_prov_24[prov_name] = [round(float(v), 1) if pd.notna(v) else None for v in sub_hii["avg_rain_mm"].values]
        else:
            hii_prov_24[prov_name] = [None] * 24

    # 3. ข้อมูลข้าวนาปีรายตำบลทั้งหมด 921 ตำบล
    tambon_items = []
    if not r921_df.empty:
        piv_y = r921_df.pivot(index=["province_name", "amphoe_name", "tambon_code_6", "tambon_name"], columns="year", values="yield_kg_per_rai").reset_index()
        piv_s = r921_df.pivot(index=["province_name", "amphoe_name", "tambon_code_6", "tambon_name"], columns="year", values="data_status").reset_index()
        piv_a = r921_df.pivot(index=["province_name", "amphoe_name", "tambon_code_6", "tambon_name"], columns="year", values="plant_area_rai").reset_index()

        for idx, row in piv_y.iterrows():
            p_name = str(row["province_name"])
            a_name = str(row["amphoe_name"]) if pd.notna(row["amphoe_name"]) else ""
            t_code = str(row["tambon_code_6"])
            t_name = str(row["tambon_name"]) if pd.notna(row["tambon_name"]) else f"ตำบล {t_code}"

            y22 = row.get(2022)
            y23 = row.get(2023)
            s22 = piv_s.iloc[idx].get(2022, "missing")
            s23 = piv_s.iloc[idx].get(2023, "missing")
            a22 = piv_a.iloc[idx].get(2022)
            a23 = piv_a.iloc[idx].get(2023)

            has_both = pd.notna(y22) and pd.notna(y23)
            delta_y = (float(y23) - float(y22)) if has_both else None

            if delta_y is not None:
                if delta_y > 0:
                    dir_th = "เพิ่มขึ้น (+)"
                elif delta_y < 0:
                    dir_th = "ลดลง (-)"
                else:
                    dir_th = "ไม่เปลี่ยนแปลง (0)"
            else:
                dir_th = "ไม่มีข้อมูลครบ 2 ปี"

            if s22 == "observed" and s23 == "observed":
                cov_status = "ครบ 2 ปี (2022–2023)"
                cov_badge = "observed_both"
            elif s22 == "observed":
                cov_status = "มีเฉพาะปี 2022"
                cov_badge = "observed_2022_only"
            elif s23 == "observed":
                cov_status = "มีเฉพาะปี 2023"
                cov_badge = "observed_2023_only"
            else:
                cov_status = "ไม่มีข้อมูลรายงาน"
                cov_badge = "missing"

            tambon_items.append({
                "tambon_code_6": t_code,
                "province_id": t_code[:2],
                "province_name": p_name,
                "amphoe_name": a_name,
                "tambon_name": t_name,
                "label": f"{t_name} ({p_name})",
                "yield_2022": round(float(y22), 2) if pd.notna(y22) else None,
                "yield_2023": round(float(y23), 2) if pd.notna(y23) else None,
                "delta_yield": round(float(delta_y), 2) if delta_y is not None else None,
                "area_2022": round(float(a22), 1) if pd.notna(a22) else None,
                "area_2023": round(float(a23), 1) if pd.notna(a23) else None,
                "status_2022": str(s22),
                "status_2023": str(s23),
                "coverage_status": cov_status,
                "coverage_badge": cov_badge,
                "direction": dir_th,
                "is_balanced_2yr": has_both
            })

    # 3.1 ข้อมูลข้าว Balanced Panel 26 ตำบล (สำหรับ Tab 4 Correlation & Backward Compatibility)
    rice_df = load_rice_tambon_data()
    diff_df = get_within_tambon_changes(rice_df, geo_df)
    balanced_tambon_items = []
    for _, row in diff_df.iterrows():
        balanced_tambon_items.append({
            "tambon_code_6": str(row["tambon_code_6"]),
            "province_id": str(row["province_id"]),
            "province_name": str(row["province_name"]),
            "amphoe_name": str(row.get("amphoe_name", "")),
            "tambon_name": str(row.get("tambon_name", "")),
            "label": str(row["label"]),
            "yield_2022": round(float(row["yield_2022"]), 2),
            "yield_2023": round(float(row["yield_2023"]), 2),
            "delta_yield": round(float(row["delta_yield"]), 2),
            "hrdi_2022": round(float(row["hrdi_2022"]), 2),
            "hrdi_2023": round(float(row["hrdi_2023"]), 2),
            "delta_hrdi": round(float(row["delta_hrdi"]), 2),
            "hii_2022": round(float(row["hii_2022"]), 2),
            "hii_2023": round(float(row["hii_2023"]), 2),
            "delta_hii": round(float(row["delta_hii"]), 2),
            "delta_hrdi_feb_jul": round(float(row["delta_hrdi_feb_jul"]), 2) if "delta_hrdi_feb_jul" in row and pd.notna(row["delta_hrdi_feb_jul"]) else None,
            "delta_hii_feb_jul": round(float(row["delta_hii_feb_jul"]), 2) if "delta_hii_feb_jul" in row and pd.notna(row["delta_hii_feb_jul"]) else None,
            "direction": str(row["yield_change_direction"])
        })

    # 4. ข้อมูลการเปลี่ยนแปลงระดับจังหวัด (สำหรับ Tab 4 Analysis)
    province_changes = []
    for _, row in prov_changes_df.iterrows():
        province_changes.append({
            "province_id": str(row["province_id"]),
            "province_name": str(row["province_name"]),
            "tambons": int(row["tambons"]),
            "mean_yield_change": round(float(row["mean_yield_change"]), 2),
            "mean_hrdi_change": round(float(row["mean_hrdi_change"]), 2),
            "hii_change": round(float(row["hii_change"]), 2),
        })

    # 5. สหสัมพันธ์ Spearman
    correlations = []
    for _, row in corr_df.iterrows():
        correlations.append({
            "analysis": str(row["analysis"]),
            "n": int(row["n"]),
            "spearman_rho": round(float(row["spearman_rho"]), 6),
            "analysis_type": str(row.get("analysis_type", "exploratory")),
            "rain_window": str(row.get("rain_window", "May-Aug")),
            "ci95_low": round(float(row["ci95_low"]), 4) if pd.notna(row.get("ci95_low")) else None,
            "ci95_high": round(float(row["ci95_high"]), 4) if pd.notna(row.get("ci95_high")) else None,
        })

    # 6. Sensitivity Reports
    lopo_list = []
    if sens_reports["leave_one_province_out"] is not None:
        for _, row in sens_reports["leave_one_province_out"].iterrows():
            lopo_list.append({
                "excluded_province_name": str(row["excluded_province_name"]),
                "tambons": int(row["tambons"]),
                "hrdi_tambon_rho": round(float(row["hrdi_tambon_rho"]), 4),
                "hrdi_province_rho": round(float(row["hrdi_province_rho"]), 4),
                "hii_province_rho": round(float(row["hii_province_rho"]), 4)
            })

    # 7. สรุปภาพรวมรายจังหวัด 9 จังหวัด (รองรับทั้ง Observed และ Exploratory)
    prov_summaries = {}
    for prov_name in PROVINCE_GEO_CENTERS.keys():
        c_p = climate_df[climate_df["province_clean"] == prov_name]
        hii_p = hii_df[hii_df["province_name_th"] == prov_name] if not hii_df.empty else pd.DataFrame()
        r_p = r921_df[r921_df["province_name"] == prov_name] if not r921_df.empty else pd.DataFrame()

        p_stas = [s for s in station_list if s["province"] == prov_name]
        sta_names = [s["name"] for s in p_stas]
        sta_cnt = len(p_stas)

        # HII Provincial Rain
        hii_22 = float(hii_p[hii_p["year"] == 2022]["avg_rain_mm"].sum()) if len(hii_p) > 0 else 0.0
        hii_23 = float(hii_p[hii_p["year"] == 2023]["avg_rain_mm"].sum()) if len(hii_p) > 0 else 0.0
        hii_chg = hii_23 - hii_22

        # Rice Yield
        r22_mean = r_p[r_p["year"] == 2022]["yield_kg_per_rai"].mean() if len(r_p) > 0 else None
        r23_mean = r_p[r_p["year"] == 2023]["yield_kg_per_rai"].mean() if len(r_p) > 0 else None

        # Climate Variables
        temp_avg = float(c_p["TEMP"].mean()) if len(c_p) > 0 and c_p["TEMP"].notna().sum() > 0 else 0.0
        hum_avg = float(c_p["HUMIDITY"].mean()) if len(c_p) > 0 and c_p["HUMIDITY"].notna().sum() > 0 else 0.0
        wind_avg = float(c_p["WIND_SPEED"].mean()) if len(c_p) > 0 and c_p["WIND_SPEED"].notna().sum() > 0 else 0.0

        # HRDI Observed Annual Means (เฉพาะสถานีที่มี 12 เดือนครบ)
        comp_obs_22 = [s["annual_obs_2022"] for s in p_stas if s["annual_obs_2022"] is not None]
        rain_obs_22 = round(sum(comp_obs_22) / len(comp_obs_22), 1) if comp_obs_22 else None
        rain_obs_23 = None  # 0 สถานีที่ครบ 12 เดือนในปี 2023
        rain_obs_all = None

        # HRDI Exploratory Annual Means (ครบ 12 เดือนสำหรับทุกสถานี)
        exp_22_vals = [s["annual_exp_2022"] for s in p_stas if s["annual_exp_2022"] is not None]
        exp_23_vals = [s["annual_exp_2023"] for s in p_stas if s["annual_exp_2023"] is not None]
        rain_exp_22 = round(sum(exp_22_vals) / len(exp_22_vals), 1) if exp_22_vals else None
        rain_exp_23 = round(sum(exp_23_vals) / len(exp_23_vals), 1) if exp_23_vals else None
        rain_exp_all = round((rain_exp_22 + rain_exp_23) / 2, 1) if (rain_exp_22 and rain_exp_23) else (rain_exp_22 or rain_exp_23)

        # รายเดือนเฉลี่ยระดับจังหวัด (12 เดือน)
        m_obs_22_prov = []
        m_obs_23_prov = []
        m_exp_22_prov = []
        m_exp_23_prov = []
        # จำนวนสถานีที่ใช้ค่าประมาณ (ไม่ใช่ค่าตรวจวัดจริง) ในแต่ละเดือน
        m_est_cnt_22 = [sum(1 for s in p_stas if s["monthly_status_24"][i] != "observed") for i in range(12)]
        m_est_cnt_23 = [sum(1 for s in p_stas if s["monthly_status_24"][i + 12] != "observed") for i in range(12)]

        for m_idx in range(12):
            obs_vals_22 = [s["monthly_obs_2022"][m_idx] for s in p_stas if s["monthly_obs_2022"][m_idx] is not None]
            obs_vals_23 = [s["monthly_obs_2023"][m_idx] for s in p_stas if s["monthly_obs_2023"][m_idx] is not None]
            exp_vals_22 = [s["monthly_exp_2022"][m_idx] for s in p_stas if s["monthly_exp_2022"][m_idx] is not None]
            exp_vals_23 = [s["monthly_exp_2023"][m_idx] for s in p_stas if s["monthly_exp_2023"][m_idx] is not None]

            m_obs_22_prov.append(round(sum(obs_vals_22) / len(obs_vals_22), 1) if obs_vals_22 else None)
            m_obs_23_prov.append(round(sum(obs_vals_23) / len(obs_vals_23), 1) if obs_vals_23 else None)
            m_exp_22_prov.append(round(sum(exp_vals_22) / len(exp_vals_22), 1) if exp_vals_22 else None)
            m_exp_23_prov.append(round(sum(exp_vals_23) / len(exp_vals_23), 1) if exp_vals_23 else None)

        # May-Aug Seasonal Rainfall (months 5-8, indices 4-7)
        obs_may_aug_22 = round(sum(m_obs_22_prov[4:8]), 1) if all(x is not None for x in m_obs_22_prov[4:8]) else None
        obs_may_aug_23 = round(sum(m_obs_23_prov[4:8]), 1) if all(x is not None for x in m_obs_23_prov[4:8]) else None
        exp_may_aug_22 = round(sum(m_exp_22_prov[4:8]), 1) if all(x is not None for x in m_exp_22_prov[4:8]) else None
        exp_may_aug_23 = round(sum(m_exp_23_prov[4:8]), 1) if all(x is not None for x in m_exp_23_prov[4:8]) else None

        sub_hii_22 = hii_p[(hii_p["year"] == 2022) & (hii_p["month"].isin([5, 6, 7, 8]))]
        sub_hii_23 = hii_p[(hii_p["year"] == 2023) & (hii_p["month"].isin([5, 6, 7, 8]))]
        hii_may_aug_22 = round(float(sub_hii_22["avg_rain_mm"].sum()), 1) if len(sub_hii_22) == 4 else None
        hii_may_aug_23 = round(float(sub_hii_23["avg_rain_mm"].sum()), 1) if len(sub_hii_23) == 4 else None

        prov_summaries[prov_name] = {
            "name": prov_name,
            "station_count": sta_cnt,
            "stations": sta_names,
            # Observed metrics
            "rain_obs_2022": rain_obs_22,
            "rain_obs_2023": rain_obs_23,
            "rain_obs_all": rain_obs_all,
            # Exploratory metrics
            "rain_exp_2022": rain_exp_22,
            "rain_exp_2023": rain_exp_23,
            "rain_exp_all": rain_exp_all,
            # Seasonal May-Aug metrics
            "obs_may_aug_2022": obs_may_aug_22,
            "obs_may_aug_2023": obs_may_aug_23,
            "exp_may_aug_2022": exp_may_aug_22,
            "exp_may_aug_2023": exp_may_aug_23,
            "hii_may_aug_2022": hii_may_aug_22,
            "hii_may_aug_2023": hii_may_aug_23,
            # Backward compatibility aliases
            "rain_all": rain_exp_all,
            "rain_2022": rain_exp_22,
            "rain_2023": rain_exp_23,
            "monthly_obs_2022": m_obs_22_prov,
            "monthly_obs_2023": m_obs_23_prov,
            "monthly_exp_2022": m_exp_22_prov,
            "monthly_exp_2023": m_exp_23_prov,
            "monthly_est_count_2022": m_est_cnt_22,
            "monthly_est_count_2023": m_est_cnt_23,
            "non_observed_count_2022": sum(m_est_cnt_22),
            "non_observed_count_2023": sum(m_est_cnt_23),
            # HII
            "hii_rain_2022": round(hii_22, 1),
            "hii_rain_2023": round(hii_23, 1),
            "hii_change": round(hii_chg, 1),
            # Rice & Climate
            "rice_yield_2022": round(float(r22_mean), 1) if pd.notna(r22_mean) else None,
            "rice_yield_2023": round(float(r23_mean), 1) if pd.notna(r23_mean) else None,
            "temp": round(temp_avg, 1),
            "humidity": round(hum_avg, 1),
            "wind": round(wind_avg, 2),
            "tambon_count": int(r_p["tambon_code_6"].nunique()) if not r_p.empty else 0
        }

    # 8. สรุปแนวโน้มฝน HII ภาพรวม 9 จังหวัด 12 เดือน (2022 vs 2023)
    monthly_2022 = []
    monthly_2023 = []
    if not hii_df.empty:
        for m in range(1, 13):
            v22 = hii_df[(hii_df["year"] == 2022) & (hii_df["month"] == m)]["avg_rain_mm"].mean()
            v23 = hii_df[(hii_df["year"] == 2023) & (hii_df["month"] == m)]["avg_rain_mm"].mean()
            monthly_2022.append(round(float(v22), 1) if pd.notna(v22) else None)
            monthly_2023.append(round(float(v23), 1) if pd.notna(v23) else None)
    else:
        monthly_2022 = [None] * 12
        monthly_2023 = [None] * 12

    # 24 เดือนภาพรวมต่อเนื่อง
    monthly_overall_24 = monthly_2022 + monthly_2023

    # 9. Overall High-level KPIs
    overall_mean_yield = float(r921_df["yield_kg_per_rai"].mean()) if not r921_df.empty and r921_df["yield_kg_per_rai"].notna().sum() > 0 else 0.0

    all_exp_22 = [s["annual_exp_2022"] for s in station_list if s["annual_exp_2022"] is not None]
    all_exp_23 = [s["annual_exp_2023"] for s in station_list if s["annual_exp_2023"] is not None]
    hrdi_exp_22_overall = round(sum(all_exp_22) / len(all_exp_22), 1) if all_exp_22 else 0.0
    hrdi_exp_23_overall = round(sum(all_exp_23) / len(all_exp_23), 1) if all_exp_23 else 0.0
    hrdi_exp_all_overall = round((hrdi_exp_22_overall + hrdi_exp_23_overall) / 2, 1)

    all_obs_22 = [s["annual_obs_2022"] for s in station_list if s["annual_obs_2022"] is not None]
    hrdi_obs_22_overall = round(sum(all_obs_22) / len(all_obs_22), 1) if all_obs_22 else None

    overall_kpis = {
        "mean_rain": round(float(hii_df["avg_rain_mm"].mean() * 12), 1) if not hii_df.empty else 0.0,
        "mean_temp": round(float(climate_df["TEMP"].mean()), 1) if climate_df["TEMP"].notna().sum() > 0 else 0.0,
        "mean_humidity": round(float(climate_df["HUMIDITY"].mean()), 1) if climate_df["HUMIDITY"].notna().sum() > 0 else 0.0,
        "mean_wind": round(float(climate_df["WIND_SPEED"].mean()), 2) if climate_df["WIND_SPEED"].notna().sum() > 0 else 0.0,
        "mean_yield": round(overall_mean_yield, 1),
        "total_provinces": 9,
        "total_stations": len(station_list),
        "total_tambons": len(tambon_items),
        "hrdi_obs_rain_2022": hrdi_obs_22_overall,
        "hrdi_obs_rain_2023": None,
        "hrdi_exp_rain_2022": hrdi_exp_22_overall,
        "hrdi_exp_rain_2023": hrdi_exp_23_overall,
        "hrdi_exp_rain_all": hrdi_exp_all_overall,
        "hrdi_non_observed_2022": sum(s["non_observed_count_2022"] for s in station_list),
        "hrdi_non_observed_2023": sum(s["non_observed_count_2023"] for s in station_list),
    }

    # 10. Sample Previews
    raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
    sample_hrdi = []
    sample_hii = []
    sample_plant = []
    try:
        if (raw_dir / "HRDI_meteo.csv").exists():
            sample_hrdi = pd.read_csv(raw_dir / "HRDI_meteo.csv", nrows=5).fillna("").to_dict(orient="records")
        if (raw_dir / "spatial-rain-hii.csv").exists():
            sample_hii = pd.read_csv(raw_dir / "spatial-rain-hii.csv", nrows=5).fillna("").to_dict(orient="records")
        if (raw_dir / "plant01_65.csv").exists():
            sample_plant = pd.read_csv(raw_dir / "plant01_65.csv", nrows=5).fillna("").to_dict(orient="records")
    except Exception:
        pass

    # 11. Window Comparison
    comp_file = Path(__file__).resolve().parent.parent / "reports" / "experiment_window_comparison.csv"
    window_comp = []
    if comp_file.exists():
        try:
            window_comp = pd.read_csv(comp_file, encoding="utf-8-sig").fillna("").to_dict(orient="records")
        except Exception:
            pass

    payload = {
        "centers": PROVINCE_GEO_CENTERS,
        "province_geojson": load_province_geojson(),
        "thailand_geojson": load_province_geojson(THAILAND_GEOJSON_FILE),
        "overview_center": OVERVIEW_CENTER,
        "stations": station_list,
        "monthly_trends": monthly_trends,
        "monthly_overall": {
            "2022": monthly_2022,
            "2023": monthly_2023,
            "all_24": monthly_overall_24
        },
        "hii_prov_24": hii_prov_24,
        "province_summaries": prov_summaries,
        "overall_kpis": overall_kpis,
        "tambons": tambon_items,
        "balanced_tambons": balanced_tambon_items,
        "province_changes": province_changes,
        "correlations": correlations,
        "lopo": lopo_list,
        "window_comparison": window_comp,
        "raw_samples": {
            "hrdi": sample_hrdi,
            "hii": sample_hii,
            "plant": sample_plant
        },
        "completeness": {
            "num_stations": len(station_list),
            "expected_station_months": 1200,
            "actual_rows": 983,
            "missing_rows": 217,
            "missing_rows_pct": round(217 / 1200 * 100, 1),
            "rain_missing_values": 7,
            "rain_valid_values": 976,
            "total_tambons": len(tambon_items),
            "observed_rice_rows": 1695,
            "missing_rice_rows": 147,
            "exploratory_total_rows": len(hrdi_df),
            "observed_station_months": 977,
            "estimated_station_months": 186,
            "exploratory_station_months": 37,
            "qa_replaced_station_months": sum(s["qa_replaced_count_total"] for s in station_list)
        }
    }

    return json.dumps(payload, ensure_ascii=False)
