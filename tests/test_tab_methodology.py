"""
Highland Rainfall Project - Unit Tests for Tab Methodology
ทดสอบการทำงานของข้อมูลและการแสดงผลในแท็บ C (ระเบียบวิธีวิจัยและ QA)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from dashboard.data_loader import (
    load_correlations_data,
    load_sensitivity_reports,
    load_tambon_geo_mapping,
    load_rice_tambon_data,
)


def test_tambon_mapping_table_integrity():
    geo_df = load_tambon_geo_mapping()
    rice_df = load_rice_tambon_data()
    tambons_25 = sorted(rice_df["tambon_code_6"].unique().tolist())
    
    assert len(tambons_25) == 25
    matched_count = 0
    for t in tambons_25:
        match = geo_df[geo_df["tambon_code_6"] == t]
        if not match.empty:
            matched_count += 1
            
    assert matched_count == 25, f"Expected all 25 tambons matched, got {matched_count}"


def test_sensitivity_reports_in_methodology():
    sens = load_sensitivity_reports()
    assert sens["leave_one_province_out"] is not None
    assert sens["yield_flag_sensitivity"] is not None


if __name__ == "__main__":
    print("Testing Tab Methodology logic...")
    test_tambon_mapping_table_integrity()
    print("✓ test_tambon_mapping_table_integrity passed")
    test_sensitivity_reports_in_methodology()
    print("✓ test_sensitivity_reports_in_methodology passed")
    print("\nALL TAB METHODOLOGY TESTS PASSED SUCCESSFULLY!")
