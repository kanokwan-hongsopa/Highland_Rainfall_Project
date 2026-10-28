"""
Highland Rainfall Project - Unit Tests for Tab Rice Rain
ทดสอบการทำงานของฟังก์ชันและตรรกะในแท็บ B (ข้าวนาปีและฝน 5 จังหวัด)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from dashboard.data_loader import (
    load_rice_tambon_data,
    load_province_changes_data,
    load_correlations_data,
    load_sensitivity_reports,
    load_tambon_geo_mapping,
    get_within_tambon_changes,
)


def test_rice_panel_invariants():
    rice = load_rice_tambon_data()
    assert len(rice) == 52
    assert rice["tambon_code_6"].nunique() == 26
    assert rice["province_id"].nunique() == 6
    assert set(rice["year"]) == {2022, 2023}
    assert rice.isna().sum().sum() == 0


def test_delta_within_tambon_invariants():
    rice = load_rice_tambon_data()
    geo = load_tambon_geo_mapping()
    diff = get_within_tambon_changes(rice, geo)
    assert len(diff) == 26

    # QA: ฝน พ.ค.–ส.ค. ลดลงทั้ง 26 ตำบล ทั้ง HRDI และ HII
    assert (diff["delta_hrdi"] < 0).all()
    assert (diff["delta_hii"] < 0).all()

    # QA: ผลผลิต เพิ่ม 11 ลด 10 เท่าเดิม 5
    assert (diff["delta_yield"] > 0).sum() == 11
    assert (diff["delta_yield"] < 0).sum() == 10
    assert (diff["delta_yield"] == 0).sum() == 5


def test_correlations_and_sensitivity_ranges():
    corrs = load_correlations_data()
    sens = load_sensitivity_reports()

    # QA: Rho values
    t_rho = corrs.loc[corrs["analysis"] == "HRDI_tambon", "spearman_rho"].values[0]
    p_hrdi_rho = corrs.loc[corrs["analysis"] == "HRDI_province", "spearman_rho"].values[0]
    p_hii_rho = corrs.loc[corrs["analysis"] == "HII_province", "spearman_rho"].values[0]

    assert abs(t_rho - (-0.076513)) < 1e-4
    assert abs(p_hrdi_rho - (-0.371429)) < 1e-4
    assert abs(p_hii_rho - (0.142857)) < 1e-4

    # QA: Leave-one-province-out ranges
    lopo = sens["leave_one_province_out"]
    assert len(lopo) == 6
    min_t, max_t = lopo["hrdi_tambon_rho"].min(), lopo["hrdi_tambon_rho"].max()
    min_p_hrdi, max_p_hrdi = lopo["hrdi_province_rho"].min(), lopo["hrdi_province_rho"].max()
    min_p_hii, max_p_hii = lopo["hii_province_rho"].min(), lopo["hii_province_rho"].max()

    assert min_t >= -0.51 and max_t <= 0.02
    assert min_p_hrdi >= -0.71 and max_p_hrdi <= 0.11
    assert min_p_hii >= -0.31 and max_p_hii <= 0.61


def test_single_province_filter_behavior():
    rice = load_rice_tambon_data()
    geo = load_tambon_geo_mapping()
    diff = get_within_tambon_changes(rice, geo)

    # กรองเฉพาะน่าน
    nan_diff = diff[diff["province_id"] == "55"]
    assert len(nan_diff) == 5

    # กรองเฉพาะเชียงใหม่ (ต้องได้ 14 ตำบล คิดเป็น 53.8%)
    cm_diff = diff[diff["province_id"] == "50"]
    assert len(cm_diff) == 14
    assert round(len(cm_diff) / len(diff) * 100, 1) == 53.8


if __name__ == "__main__":
    print("Testing Tab Rice Rain logic...")
    test_rice_panel_invariants()
    print("✓ test_rice_panel_invariants passed")
    test_delta_within_tambon_invariants()
    print("✓ test_delta_within_tambon_invariants passed")
    test_correlations_and_sensitivity_ranges()
    print("✓ test_correlations_and_sensitivity_ranges passed")
    test_single_province_filter_behavior()
    print("✓ test_single_province_filter_behavior passed")
    print("\nALL TAB RICE RAIN TESTS PASSED SUCCESSFULLY!")
