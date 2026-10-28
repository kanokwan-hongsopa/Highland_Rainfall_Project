from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PROCESSED = DATA / "processed"
DASHBOARD = DATA / "dashboard"
REPORTS = ROOT / "reports"
RAW = DATA / "raw"

DASHBOARD.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

print("=== 1. PREPARING MAY-AUGUST & FEB-JUL DATA ===")

# 1.1 Load Baseline Balanced Panel (Feb-Jul)
baseline_panel = pd.read_csv(PROCESSED / "rice_rain_balanced_panel.csv", dtype={"tambon_code_6": str})
tambons_25 = sorted(baseline_panel["tambon_code_6"].unique())
assert len(tambons_25) == 25

# 1.2 Load Station Matching
matching = pd.read_csv(REPORTS / "hrdi_crop_matching.csv", dtype=str)
stations_28 = matching[matching["tambon_code_6"].isin(tambons_25)][["tambon_code_6", "CODE_REF", "STA_TH", "province"]].drop_duplicates()
assert stations_28["CODE_REF"].nunique() == 28

# 1.3 Load HRDI Clean
hrdi = pd.read_csv(PROCESSED / "hrdi_clean_2022_2023.csv")
hrdi["year"] = pd.to_numeric(hrdi["year"]).astype(int)
hrdi["month"] = pd.to_numeric(hrdi["month"]).astype(int)
hrdi["rainfall_mm"] = pd.to_numeric(hrdi["rainfall_mm"], errors="coerce")

# Calculate May-Aug HRDI
hrdi_may_aug = hrdi[hrdi["CODE_REF"].isin(stations_28["CODE_REF"]) & hrdi["month"].isin([5, 6, 7, 8])].copy()
hrdi_may_aug = hrdi_may_aug.merge(stations_28[["CODE_REF", "tambon_code_6"]], on="CODE_REF", how="left")
m_mean = hrdi_may_aug.groupby(["year", "month", "tambon_code_6"], as_index=False).agg(
    hrdi_mean_rain=("rainfall_mm", "mean"),
    station_count=("CODE_REF", "nunique")
)
annual_hrdi_may_aug = m_mean.groupby(["year", "tambon_code_6"], as_index=False).agg(
    hrdi_may_aug_total=("hrdi_mean_rain", "sum"),
    months_count=("month", "nunique"),
    station_count=("station_count", "max")
)
assert (annual_hrdi_may_aug["months_count"] == 4).all()

# 1.4 Load HII May-Aug
hii = pd.read_csv(RAW / "spatial-rain-hii.csv")
hii["YEAR"] = pd.to_numeric(hii["YEAR"]).astype(int)
hii["MONTH"] = pd.to_numeric(hii["MONTH"]).astype(int)
hii["PROV_ID"] = pd.to_numeric(hii["PROV_ID"]).astype(int)
hii["AvgRain"] = pd.to_numeric(hii["AvgRain"], errors="coerce")

hii_may_aug = hii[hii["YEAR"].isin([2022, 2023]) & hii["MONTH"].isin([5, 6, 7, 8])].groupby(["YEAR", "PROV_ID"], as_index=False).agg(
    hii_may_aug_total=("AvgRain", "sum"),
    hii_months=("MONTH", "nunique")
)
assert (hii_may_aug["hii_months"] == 4).all()

# 1.5 Load Rice Yield
rice_scenarios = pd.read_csv(PROCESSED / "rice_tambon_year_scenarios.csv", dtype={"tambon_code_6": str})
rice_valid = rice_scenarios[(rice_scenarios["scenario"] == "all_valid_records") & (rice_scenarios["tambon_code_6"].isin(tambons_25))].copy()
rice_valid["year"] = pd.to_numeric(rice_valid["year"]).astype(int)

# 1.6 Build Unified Panel (both May-Aug and Feb-Jul)
panel = rice_valid[["year", "tambon_code_6", "weighted_yield"]].copy()
panel["province_id"] = panel["tambon_code_6"].str[:2]
panel["prov_int"] = panel["province_id"].astype(int)

# Merge May-Aug
panel = panel.merge(annual_hrdi_may_aug[["year", "tambon_code_6", "hrdi_may_aug_total", "station_count"]], on=["year", "tambon_code_6"], how="left")
panel = panel.merge(hii_may_aug[["YEAR", "PROV_ID", "hii_may_aug_total"]], left_on=["year", "prov_int"], right_on=["YEAR", "PROV_ID"], how="left")
panel = panel.drop(columns=["prov_int", "YEAR", "PROV_ID"])

# Merge Feb-Jul baseline for comparison
panel = panel.merge(baseline_panel[["year", "tambon_code_6", "hrdi_clean_feb_jul_total", "hii_feb_jul_total"]], on=["year", "tambon_code_6"], how="left")

# Save Unified Balanced Panel
panel.to_csv(PROCESSED / "rice_rain_balanced_panel.csv", index=False, encoding="utf-8-sig")

# 1.7 Prepare dashboard_rice_tambon.csv
dashboard_rice = panel.rename(columns={
    "weighted_yield": "rice_yield_per_harvest_area",
    "hrdi_may_aug_total": "hrdi_may_aug",
    "hii_may_aug_total": "hii_may_aug",
    "hrdi_clean_feb_jul_total": "hrdi_feb_jul",
    "hii_clean_feb_jul_total": "hii_feb_jul"  # or hii_feb_jul_total
}).copy()

if "hii_feb_jul_total" in dashboard_rice.columns:
    dashboard_rice = dashboard_rice.rename(columns={"hii_feb_jul_total": "hii_feb_jul"})

dashboard_rice.to_csv(DASHBOARD / "dashboard_rice_tambon.csv", index=False, encoding="utf-8-sig")
print("Saved dashboard_rice_tambon.csv (50 rows, 25 tambons)")

# === 2. WITHIN-TAMBON CHANGES (2023 - 2022) ===
piv_y = panel.pivot(index="tambon_code_6", columns="year", values="weighted_yield")
piv_hrdi_ma = panel.pivot(index="tambon_code_6", columns="year", values="hrdi_may_aug_total")
piv_hii_ma = panel.pivot(index="tambon_code_6", columns="year", values="hii_may_aug_total")
piv_hrdi_fj = panel.pivot(index="tambon_code_6", columns="year", values="hrdi_clean_feb_jul_total")
piv_hii_fj = panel.pivot(index="tambon_code_6", columns="year", values="hii_feb_jul_total")

changes = pd.DataFrame(index=piv_y.index)
changes["province_id"] = changes.index.str[:2]
changes["yield_2022"] = piv_y[2022]
changes["yield_2023"] = piv_y[2023]
changes["yield_change"] = piv_y[2023] - piv_y[2022]

changes["hrdi_2022"] = piv_hrdi_ma[2022]
changes["hrdi_2023"] = piv_hrdi_ma[2023]
changes["hrdi_change"] = piv_hrdi_ma[2023] - piv_hrdi_ma[2022]

changes["hii_2022"] = piv_hii_ma[2022]
changes["hii_2023"] = piv_hii_ma[2023]
changes["hii_change"] = piv_hii_ma[2023] - piv_hii_ma[2022]

changes["hrdi_feb_jul_change"] = piv_hrdi_fj[2023] - piv_hrdi_fj[2022]
changes["hii_feb_jul_change"] = piv_hii_fj[2023] - piv_hii_fj[2022]

for v in ["yield", "hrdi", "hii"]:
    changes[f"{v}_direction"] = changes[f"{v}_change"].apply(
        lambda x: "increase" if x > 0 else ("decrease" if x < 0 else "unchanged")
    )

changes.reset_index().to_csv(PROCESSED / "rice_rain_balanced_changes.csv", index=False, encoding="utf-8-sig")
print("Saved rice_rain_balanced_changes.csv (25 tambons)")

# === 3. PROVINCIAL AGGREGATIONS & CORRELATIONS ===
prov_changes = changes.groupby("province_id", as_index=False).agg(
    tambons=("yield_change", "size"),
    mean_yield_change=("yield_change", "mean"),
    mean_hrdi_change=("hrdi_change", "mean"),
    hii_change=("hii_change", "first"),
    mean_hrdi_feb_jul_change=("hrdi_feb_jul_change", "mean"),
    hii_feb_jul_change=("hii_feb_jul_change", "first")
)

prov_changes.to_csv(PROCESSED / "rice_rain_province_changes.csv", index=False, encoding="utf-8-sig")
prov_changes.to_csv(DASHBOARD / "dashboard_province_changes.csv", index=False, encoding="utf-8-sig")
print("Saved dashboard_province_changes.csv (5 provinces)")

# Spearman Functions
def safe_rho(df, x, y):
    return df[[x, y]].dropna().corr(method="spearman").iloc[0, 1]

rho_hrdi_tambon = safe_rho(changes, "hrdi_change", "yield_change")
rho_hrdi_prov = safe_rho(prov_changes, "mean_hrdi_change", "mean_yield_change")
rho_hii_prov = safe_rho(prov_changes, "hii_change", "mean_yield_change")

# Correlations table
correlations = pd.DataFrame([
    {
        "analysis": "HRDI_tambon",
        "n": len(changes),
        "spearman_rho": float(rho_hrdi_tambon),
        "analysis_type": "exploratory",
        "causal_interpretation_allowed": False,
        "rain_window": "May-Aug",
        "crop_season_verified": "Vegetative Stage (Planting to Tillering)",
        "source_units_verified": False
    },
    {
        "analysis": "HRDI_province",
        "n": len(prov_changes),
        "spearman_rho": float(rho_hrdi_prov),
        "analysis_type": "exploratory",
        "causal_interpretation_allowed": False,
        "rain_window": "May-Aug",
        "crop_season_verified": "Vegetative Stage (Planting to Tillering)",
        "source_units_verified": False
    },
    {
        "analysis": "HII_province",
        "n": len(prov_changes),
        "spearman_rho": float(rho_hii_prov),
        "analysis_type": "exploratory",
        "causal_interpretation_allowed": False,
        "rain_window": "May-Aug",
        "crop_season_verified": "Vegetative Stage (Planting to Tillering)",
        "source_units_verified": False
    }
])

correlations.to_csv(REPORTS / "rice_rain_exploratory_correlations.csv", index=False, encoding="utf-8-sig")
correlations.to_csv(DASHBOARD / "dashboard_correlations.csv", index=False, encoding="utf-8-sig")
print("Saved dashboard_correlations.csv")

# === 4. LEAVE-ONE-PROVINCE-OUT (LOPO) ===
lopo = []
for p in sorted(changes["province_id"].unique()):
    sub_t = changes[changes["province_id"] != p]
    sub_p = prov_changes[prov_changes["province_id"] != p]
    lopo.append({
        "scenario": f"exclude_province_{p}",
        "tambons": len(sub_t),
        "provinces": len(sub_p),
        "hrdi_tambon_rho": float(safe_rho(sub_t, "hrdi_change", "yield_change")),
        "hrdi_province_rho": float(safe_rho(sub_p, "mean_hrdi_change", "mean_yield_change")),
        "hii_province_rho": float(safe_rho(sub_p, "hii_change", "mean_yield_change")),
        "excluded_province": p
    })

lopo_df = pd.DataFrame(lopo)
lopo_df.to_csv(REPORTS / "rice_rain_leave_one_province_out.csv", index=False, encoding="utf-8-sig")
print("Saved rice_rain_leave_one_province_out.csv")

print("\n=== VERIFICATION SUMMARY ===")
print("HRDI Tambon rho:", round(rho_hrdi_tambon, 4))
print("HRDI Province rho:", round(rho_hrdi_prov, 4))
print("HII Province rho:", round(rho_hii_prov, 4))
print("\nLOPO:")
print(lopo_df.to_string(index=False))
