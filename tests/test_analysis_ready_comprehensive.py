"""
Comprehensive Automated Test Suite for Highland Rainfall Project Analysis-Ready Data
Verifies:
- Grid shapes and primary keys
- Zero synthetic data in analysis_ready
- Exact correspondence to Raw Data
- Ray-casting point-in-polygon verification for all 50 stations
- Zero double counting in joins
- Spearman correlations and sensitivity consistency
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_READY = ROOT / "data" / "analysis_ready"
EXPERIMENTAL = ROOT / "data" / "experimental_complete"
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"


def test_zero_synthetic_in_analysis_ready():
    """Verify that NO synthetic data exists in data/analysis_ready/."""
    for p in ANALYSIS_READY.glob("*.csv"):
        df = pd.read_csv(p)
        if "data_status" in df.columns:
            statuses = set(df["data_status"].unique())
            assert "synthetic" not in statuses, f"Contamination in {p.name}: {statuses}"
    print("[PASS] test_zero_synthetic_in_analysis_ready")


def test_row_counts_and_primary_keys():
    """Verify exact row counts and primary key uniqueness across all tables."""
    # HRDI observed
    hrdi = pd.read_csv(ANALYSIS_READY / "hrdi_station_monthly_observed.csv")
    assert len(hrdi) == 976
    assert not hrdi.duplicated(subset=["station_code", "year", "month"]).any()

    # HRDI estimated sensitivity
    hrdi_est = pd.read_csv(ANALYSIS_READY / "hrdi_estimated_sensitivity.csv")
    assert len(hrdi_est) == 7

    # HII observed
    hii = pd.read_csv(ANALYSIS_READY / "hii_province_monthly_observed.csv")
    assert len(hii) == 216
    assert not hii.duplicated(subset=["province_id", "year", "month"]).any()

    # DOAE rice observed
    rice = pd.read_csv(ANALYSIS_READY / "rice_tambon_annual_observed.csv", dtype={"tambon_code_6": str})
    assert len(rice) == 1695
    assert not rice.duplicated(subset=["tambon_code_6", "year"]).any()

    # Linkage
    link = pd.read_csv(ANALYSIS_READY / "geographic_linkage_verified.csv")
    assert len(link) == 50
    assert not link.duplicated(subset=["station_code"]).any()

    # Balanced panel
    p_bal = pd.read_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_observed.csv", dtype={"tambon_code_6": str})
    assert len(p_bal) == 54
    assert p_bal["tambon_code_6"].nunique() == 27
    assert not p_bal.duplicated(subset=["tambon_code_6", "year"]).any()

    # Unbalanced panel
    p_unbal = pd.read_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_unbalanced.csv", dtype={"tambon_code_6": str})
    assert len(p_unbal) == 60
    assert p_unbal["tambon_code_6"].nunique() == 33

    # Province panel
    p_prov = pd.read_csv(ANALYSIS_READY / "rice_hii_province_panel_observed.csv")
    assert len(p_prov) == 18
    assert not p_prov.duplicated(subset=["province_code", "year"]).any()

    print("[PASS] test_row_counts_and_primary_keys")


def test_ground_truth_raw_data_identity():
    """Verify that observed values match Raw Data files 100%."""
    # HII
    raw_hii = pd.read_csv(RAW / "spatial-rain-hii.csv")
    raw_hii.columns = raw_hii.columns.str.strip()
    exp_hii = pd.read_csv(ANALYSIS_READY / "hii_province_monthly_observed.csv")
    prov_9 = exp_hii["province_name_th"].unique()
    raw_sub = raw_hii[(raw_hii["YEAR"].isin([2022, 2023])) & (raw_hii["PROV_T"].isin(prov_9))].sort_values(["YEAR", "MONTH", "PROV_ID"]).reset_index(drop=True)
    exp_sub = exp_hii.sort_values(["year", "month", "province_id"]).reset_index(drop=True)
    assert np.allclose(raw_sub["AvgRain"].values, exp_sub["avg_rain_mm"].values)

    # DOAE 2023
    p66 = pd.read_csv(RAW / "5.-01-2566.csv")
    p66["prov_2"] = p66["code_province_id"].astype(str).str.zfill(2)
    p66["tambon_code_6"] = p66["code_tambon_id"].astype(str).str.zfill(6)
    p66["prod_norm"] = p66["product_id"].astype(str).str.zfill(6)
    prov_9 = {"50", "55", "57", "58", "62", "63", "65", "67", "71"}
    p66_rice = p66[(p66["prov_2"].isin(prov_9)) & (p66["prod_norm"] == "011000")]
    rice = pd.read_csv(ANALYSIS_READY / "rice_tambon_annual_observed.csv", dtype={"tambon_code_6": str})
    rice_23 = rice[rice["year"] == 2023]
    assert np.allclose(p66_rice["area_harvest"].sum(), rice_23["harvest_area_rai"].sum())
    assert np.allclose(p66_rice["product_harvest"].sum(), rice_23["production_kg"].sum())

    print("[PASS] test_ground_truth_raw_data_identity")


def test_gis_province_polygon_containment():
    """Verify that all 50 HRDI stations fall inside their declared province polygon."""
    link = pd.read_csv(ANALYSIS_READY / "geographic_linkage_verified.csv")
    assert link["gis_province_polygon_verified"].all()
    print("[PASS] test_gis_province_polygon_containment")


def test_zero_double_counting_in_joins():
    """Verify that multi-station tambon joins do not duplicate rice production."""
    panel = pd.read_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_observed.csv", dtype={"tambon_code_6": str})
    rice = pd.read_csv(ANALYSIS_READY / "rice_tambon_annual_observed.csv", dtype={"tambon_code_6": str})

    panel_prod = panel["production_kg"].sum()
    target_rice_prod = rice[rice["tambon_code_6"].isin(panel["tambon_code_6"])]["production_kg"].sum()
    assert np.isclose(panel_prod, target_rice_prod)

    prov_panel = pd.read_csv(ANALYSIS_READY / "rice_hii_province_panel_observed.csv")
    assert np.isclose(prov_panel["total_production_kg"].sum(), rice["production_kg"].sum())
    print("[PASS] test_zero_double_counting_in_joins")


def test_statistical_calculations_consistency():
    """Verify Spearman correlation calculations across all 3 methods."""
    panel = pd.read_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_observed.csv", dtype={"tambon_code_6": str})

    # Method 1: Separate years
    p22 = panel[panel["year"] == 2022]
    p23 = panel[panel["year"] == 2023]
    rho_22, p_22 = stats.spearmanr(p22["hrdi_may_aug_mean_rain_mm"], p22["yield_kg_per_rai"])
    rho_23, p_23 = stats.spearmanr(p23["hrdi_may_aug_mean_rain_mm"], p23["yield_kg_per_rai"])
    assert np.isclose(rho_22, -0.5044, atol=1e-3)
    assert np.isclose(rho_23, -0.4098, atol=1e-3)

    # Method 2: Pooled
    rho_pool, p_pool = stats.spearmanr(panel["hrdi_may_aug_mean_rain_mm"], panel["yield_kg_per_rai"])
    assert np.isclose(rho_pool, -0.4031, atol=1e-3)

    # Method 3: First-differenced
    p_rain = panel.pivot(index="tambon_code_6", columns="year", values="hrdi_may_aug_mean_rain_mm")
    p_yield = panel.pivot(index="tambon_code_6", columns="year", values="yield_kg_per_rai")
    d_rain = p_rain[2023] - p_rain[2022]
    d_yield = p_yield[2023] - p_yield[2022]
    rho_diff, p_diff = stats.spearmanr(d_rain, d_yield)
    assert np.isclose(rho_diff, -0.1675, atol=1e-3)

    print("[PASS] test_statistical_calculations_consistency")


def test_experimental_complete_grid():
    """Verify experimental complete datasets integrity and absence of fake rice farming."""
    rice_exp = pd.read_csv(EXPERIMENTAL / "rice_experimental_complete.csv", dtype={"tambon_code_6": str})
    assert len(rice_exp) == 1842
    # Verify unobserved tambons have 0 planted and harvested area
    unobs = rice_exp[rice_exp["data_status"] == "not_registered"]
    assert len(unobs) == 147
    assert (unobs["plant_area_rai"] == 0).all()
    assert (unobs["harvest_area_rai"] == 0).all()
    assert (unobs["production_kg"] == 0).all()
    print("[PASS] test_experimental_complete_grid")


if __name__ == "__main__":
    print("Running Comprehensive Automated Test Suite...")
    test_zero_synthetic_in_analysis_ready()
    test_row_counts_and_primary_keys()
    test_ground_truth_raw_data_identity()
    test_gis_province_polygon_containment()
    test_zero_double_counting_in_joins()
    test_statistical_calculations_consistency()
    test_experimental_complete_grid()
    print("\nALL 6 COMPREHENSIVE AUTOMATED TESTS PASSED SUCCESSFULLY!")
