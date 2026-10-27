"""
Highland Rainfall Project - Halloween Data Serializer
แปลงข้อมูลจริงจาก Data Loader ให้เป็น JSON Payload สำหรับ High-Performance Frontend Engine
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


def get_halloween_payload() -> str:
    """
    เตรียมข้อมูลจริงทั้งหมดในรูปแบบ JSON ปลอดภัย
    """
    climate_df = load_climate_data()
    completeness = get_climate_completeness_summary(climate_df)
    rice_df = load_rice_tambon_data()
    prov_changes_df = load_province_changes_data()
    corr_df = load_correlations_data()
    sens_reports = load_sensitivity_reports()
    geo_df = load_tambon_geo_mapping()
    diff_df = get_within_tambon_changes(rice_df, geo_df)

    # 1. รายชื่อสถานี 50 แห่งพร้อมพิกัดและค่าเฉลี่ย
    station_list = []
    for sta_name, group in climate_df.groupby("STA_TH"):
        first = group.iloc[0]
        prov = first["province_clean"]
        lat = float(first["LAT"])
        lng = float(first["LONG"])
        src = str(first["source_type"])
        records_cnt = len(group)
        valid_rain_cnt = int(group["rainfall_mm"].notna().sum())
        mean_rain = float(group["rainfall_mm"].mean()) if valid_rain_cnt > 0 else 0.0
        mean_temp = float(group["TEMP"].mean()) if group["TEMP"].notna().sum() > 0 else 0.0
        mean_humidity = float(group["HUMIDITY"].mean()) if group["HUMIDITY"].notna().sum() > 0 else 0.0
        mean_wind = float(group["WIND_SPEED"].mean()) if group["WIND_SPEED"].notna().sum() > 0 else 0.0

        station_list.append({
            "name": sta_name,
            "province": prov,
            "amphoe": str(first.get("AMPHOE", "")),
            "tambon": str(first.get("TAMBON", "")),
            "lat": round(lat, 5),
            "lng": round(lng, 5),
            "source": src,
            "records": records_cnt,
            "valid_rain": valid_rain_cnt,
            "mean_rain": round(mean_rain, 1),
            "mean_temp": round(mean_temp, 1),
            "mean_humidity": round(mean_humidity, 1),
            "mean_wind": round(mean_wind, 2),
        })

    # 2. ข้อมูลรายเดือนสำหรับกราฟแนวโน้ม (2022-2023)
    monthly_trends = []
    for (ym, prov), grp in climate_df.groupby(["year_month", "province_clean"]):
        monthly_trends.append({
            "year_month": ym,
            "province": prov,
            "mean_rain": round(float(grp["rainfall_mm"].mean()), 2) if grp["rainfall_mm"].notna().any() else None,
            "mean_temp": round(float(grp["TEMP"].mean()), 2) if grp["TEMP"].notna().any() else None,
            "mean_humidity": round(float(grp["HUMIDITY"].mean()), 2) if grp["HUMIDITY"].notna().any() else None,
            "mean_wind": round(float(grp["WIND_SPEED"].mean()), 2) if grp["WIND_SPEED"].notna().any() else None,
            "stations_count": int(grp["STA_TH"].nunique())
        })

    # 3. ข้อมูลข้าวนาปีรายตำบล 25 ตำบล (Balanced Panel)
    tambon_items = []
    for _, row in diff_df.iterrows():
        tambon_items.append({
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
            "direction": str(row["yield_change_direction"])
        })

    # 4. ข้อมูลการเปลี่ยนแปลงระดับจังหวัด 5 จังหวัด
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
            "rain_window": str(row.get("rain_window", "Feb-Jul"))
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

    payload = {
        "centers": PROVINCE_GEO_CENTERS,
        "overview_center": OVERVIEW_CENTER,
        "stations": station_list,
        "monthly_trends": monthly_trends,
        "tambons": tambon_items,
        "province_changes": province_changes,
        "correlations": correlations,
        "lopo": lopo_list,
        "completeness": {
            "num_stations": completeness["num_stations"],
            "expected_station_months": completeness["expected_station_months"],
            "actual_rows": completeness["actual_rows"],
            "missing_rows": completeness["missing_rows"],
            "missing_rows_pct": completeness["missing_rows_pct"],
            "rain_missing_values": completeness["rain_missing_values"],
            "rain_valid_values": completeness["rain_valid_values"]
        }
    }

    return json.dumps(payload, ensure_ascii=False)
