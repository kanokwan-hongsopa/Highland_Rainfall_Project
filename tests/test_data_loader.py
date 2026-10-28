"""
Highland Rainfall Project - Unit Tests for Data Loader and QA Verification
รันเพื่อทดสอบความถูกต้องของข้อมูลตามเกณฑ์ BRD และ HANDOFF
"""

import sys
from pathlib import Path
# Standard library imports

# เพิ่ม Root Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dashboard.data_loader import (
    load_climate_data,
    get_climate_completeness_summary,
    load_rice_tambon_data,
    load_province_changes_data,
    load_correlations_data,
    load_sensitivity_reports,
    load_tambon_geo_mapping,
    get_within_tambon_changes,
)


def test_climate_data_shape_and_columns():
    df = load_climate_data()
    assert len(df) == 983, f"Expected 983 rows, got {len(df)}"
    assert df["STA_TH"].nunique() == 50, f"Expected 50 stations, got {df['STA_TH'].nunique()}"
    assert df["province_clean"].nunique() == 9, f"Expected 9 provinces, got {df['province_clean'].nunique()}"
    
    # ฝนใช้งานได้ 976 แถว ขาด 7 แถว
    valid_rain = df["rainfall_mm"].notna().sum()
    assert valid_rain == 976, f"Expected 976 valid rain rows, got {valid_rain}"
    assert df["rainfall_mm"].isna().sum() == 7, "Expected 7 missing rain values"


def test_climate_missing_rows_vs_missing_values():
    df = load_climate_data()
    summary = get_climate_completeness_summary(df)
    
    assert summary["num_stations"] == 50
    assert summary["expected_station_months"] == 1200
    assert summary["actual_rows"] == 983
    assert summary["missing_rows"] == 217, f"Expected 217 missing rows, got {summary['missing_rows']}"
    assert summary["rain_missing_values"] == 7
    assert summary["rain_valid_values"] == 976
    assert len(summary["grid_matrix"]) == 1200


def test_rice_tambon_qa_metrics():
    df = load_rice_tambon_data()
    assert len(df) == 52, "Expected 52 rows in dashboard_rice_tambon"
    assert df["tambon_code_6"].nunique() == 26, "Expected 26 tambons"
    assert set(df["year"]) == {2022, 2023}, "Expected years 2022 and 2023"
    assert df.isna().sum().sum() == 0, "Expected 0 missing values"

    # การกระจายตัวรายจังหวัด
    p_counts = df[df["year"] == 2022]["province_id"].value_counts().to_dict()
    assert p_counts.get("50") == 14, f"Expected 14 for Chiang Mai, got {p_counts.get('50')}"
    assert p_counts.get("55") == 5, f"Expected 5 for Nan, got {p_counts.get('55')}"
    assert p_counts.get("58") == 3, f"Expected 3 for Mae Hong Son, got {p_counts.get('58')}"
    assert p_counts.get("63") == 2, f"Expected 2 for Tak, got {p_counts.get('63')}"
    assert p_counts.get("57") == 1, f"Expected 1 for Chiang Rai, got {p_counts.get('57')}"
    assert p_counts.get("62") == 1, f"Expected 1 for Kamphaeng Phet, got {p_counts.get('62')}"


def test_within_tambon_changes_qa():
    rice = load_rice_tambon_data()
    geo = load_tambon_geo_mapping()
    diff = get_within_tambon_changes(rice, geo)

    assert len(diff) == 26, "Expected 26 tambons in diff"
    
    # ฝนลดลงทั้ง 26 ตำบล
    assert (diff["delta_hrdi"] < 0).all(), "HRDI rain should decrease for all 26 tambons"
    assert (diff["delta_hii"] < 0).all(), "HII rain should decrease for all 26 tambons"

    # ผลผลิต เพิ่ม 11, ลด 10, เท่าเดิม 5
    inc = (diff["delta_yield"] > 0).sum()
    dec = (diff["delta_yield"] < 0).sum()
    zero = (diff["delta_yield"] == 0).sum()
    assert inc == 11, f"Expected 11 yield increases, got {inc}"
    assert dec == 10, f"Expected 10 yield decreases, got {dec}"
    assert zero == 5, f"Expected 5 unchanged yield, got {zero}"


def test_correlations_qa():
    corrs = load_correlations_data()
    assert len(corrs) == 3
    
    hrdi_t = corrs[corrs["analysis"] == "HRDI_tambon"].iloc[0]
    assert hrdi_t["n"] == 26
    assert abs(hrdi_t["spearman_rho"] - (-0.076513)) < 1e-4
    assert hrdi_t["ci95_low"] < 0 < hrdi_t["ci95_high"]

    hrdi_p = corrs[corrs["analysis"] == "HRDI_province"].iloc[0]
    assert hrdi_p["n"] == 6
    assert abs(hrdi_p["spearman_rho"] - (-0.371429)) < 1e-4

    hii_p = corrs[corrs["analysis"] == "HII_province"].iloc[0]
    assert hii_p["n"] == 6
    assert abs(hii_p["spearman_rho"] - (0.142857)) < 1e-4


def test_sensitivity_reports_exist():
    reports = load_sensitivity_reports()
    assert reports["leave_one_province_out"] is not None
    assert len(reports["leave_one_province_out"]) == 6
    assert reports["yield_flag_sensitivity"] is not None
    assert len(reports["yield_flag_sensitivity"]) == 2


def test_tambon_geo_mapping():
    geo = load_tambon_geo_mapping()
    assert not geo.empty
    rice = load_rice_tambon_data()
    tambons = set(rice["tambon_code_6"].unique())
    geo_tambons = set(geo["tambon_code_6"].unique())
    # ทั้ง 26 ตำบลต้องอยู่ใน geo_tambons
    assert tambons.issubset(geo_tambons), f"Missing geo for: {tambons - geo_tambons}"


if __name__ == "__main__":
    print("Running tests manually...")
    test_climate_data_shape_and_columns()
    print("✓ test_climate_data_shape_and_columns passed")
    test_climate_missing_rows_vs_missing_values()
    print("✓ test_climate_missing_rows_vs_missing_values passed")
    test_rice_tambon_qa_metrics()
    print("✓ test_rice_tambon_qa_metrics passed")
    test_within_tambon_changes_qa()
    print("✓ test_within_tambon_changes_qa passed")
    test_correlations_qa()
    print("✓ test_correlations_qa passed")
    test_sensitivity_reports_exist()
    print("✓ test_sensitivity_reports_exist passed")
    test_tambon_geo_mapping()
    print("✓ test_tambon_geo_mapping passed")
    print("\nALL 7 UNIT TESTS PASSED SUCCESSFULLY!")
