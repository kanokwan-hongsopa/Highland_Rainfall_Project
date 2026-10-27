"""
Highland Rainfall Project - Unit Tests for Tab Climate
ทดสอบการทำงานของฟังก์ชันและตรรกะในแท็บ A (ภาพรวมภูมิอากาศ)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from dashboard.data_loader import load_climate_data, get_climate_completeness_summary
from dashboard.tab_climate import WEATHER_VARIABLES


def test_weather_variables_definition():
    for k, v in WEATHER_VARIABLES.items():
        assert "label" in v
        assert "unit" in v
        assert "col" in v
        assert "description" in v


def test_climate_filters_logic():
    df = load_climate_data()
    # 1. ทดสอบกรองปี 2022
    df_2022 = df[df["year"] == 2022]
    assert len(df_2022) > 0
    assert set(df_2022["year"]) == {2022}

    # 2. ทดสอบกรองจังหวัด น่าน
    df_nan = df[df["province_clean"] == "น่าน"]
    assert len(df_nan) > 0
    assert (df_nan["province_clean"] == "น่าน").all()

    # 3. ทดสอบการคำนวณ Station-Average
    prov_monthly = df.groupby(["year_month", "province_clean"], as_index=False).agg(
        mean_val=("rainfall_mm", "mean"),
        station_count=("STA_TH", "nunique")
    )
    assert not prov_monthly.empty
    assert "mean_val" in prov_monthly.columns
    assert "station_count" in prov_monthly.columns


def test_heatmap_matrix_structure():
    df = load_climate_data()
    summary = get_climate_completeness_summary(df)
    grid_df = summary["grid_matrix"].copy()
    
    # ตรวจสอบว่า grid matrix มีขนาด 1,200 แถว
    assert len(grid_df) == 1200
    grid_df["year_month"] = grid_df["year"].astype(str) + "-" + grid_df["month"].astype(str).str.zfill(2)
    piv = grid_df.pivot(index="STA_TH", columns="year_month", values="status")
    assert piv.shape[0] == 50  # 50 สถานี
    assert piv.shape[1] == 24  # 24 เดือน


if __name__ == "__main__":
    print("Testing Tab Climate logic...")
    test_weather_variables_definition()
    print("✓ test_weather_variables_definition passed")
    test_climate_filters_logic()
    print("✓ test_climate_filters_logic passed")
    test_heatmap_matrix_structure()
    print("✓ test_heatmap_matrix_structure passed")
    print("\nALL TAB CLIMATE TESTS PASSED SUCCESSFULLY!")
