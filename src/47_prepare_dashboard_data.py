
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "data" / "dashboard"
OUTPUT.mkdir(parents=True, exist_ok=True)

# 1. ข้อมูลตำบล-ปี
panel = pd.read_csv(
    PROCESSED / "rice_rain_balanced_panel.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

panel["year"] = pd.to_numeric(panel["year"]).astype(int)
panel["province_id"] = panel["tambon_code_6"].str[:2]

assert set(panel["year"]) == {2022, 2023}
assert not panel.duplicated(
    ["year", "tambon_code_6"]
).any()
assert panel["tambon_code_6"].nunique() == 25

tambon = panel[[
    "year",
    "province_id",
    "tambon_code_6",
    "weighted_yield",
    "hrdi_clean_feb_jul_total",
    "hii_feb_jul_total",
    "station_count"
]].copy()

tambon = tambon.rename(columns={
    "weighted_yield": "rice_yield_per_harvest_area",
    "hrdi_clean_feb_jul_total": "hrdi_feb_jul",
    "hii_feb_jul_total": "hii_feb_jul"
})

tambon.to_csv(
    OUTPUT / "dashboard_rice_tambon.csv",
    index=False,
    encoding="utf-8-sig"
)

# 2. ข้อมูลการเปลี่ยนแปลงระดับจังหวัด
province = pd.read_csv(
    PROCESSED / "rice_rain_province_changes.csv",
    dtype={"province_id": str},
    encoding="utf-8-sig"
)

assert province["province_id"].nunique() == 5
assert not province["province_id"].duplicated().any()

province.to_csv(
    OUTPUT / "dashboard_province_changes.csv",
    index=False,
    encoding="utf-8-sig"
)

# 3. ผลความสัมพันธ์
correlations = pd.read_csv(
    REPORTS / "rice_rain_exploratory_correlations.csv",
    encoding="utf-8-sig"
)

correlations["analysis_type"] = "exploratory"
correlations["causal_interpretation_allowed"] = False
correlations["rain_window"] = "Feb-Jul"
correlations["crop_season_verified"] = False
correlations["source_units_verified"] = False

correlations.to_csv(
    OUTPUT / "dashboard_correlations.csv",
    index=False,
    encoding="utf-8-sig"
)

# 4. ตรวจความครบถ้วนของไฟล์
print("\n===== DASHBOARD DATA VALIDATION =====")

for name, data in [
    ("Tambon-year", tambon),
    ("Province changes", province),
    ("Correlations", correlations)
]:
    print(
        f"{name}: rows={len(data)}, "
        f"columns={len(data.columns)}, "
        f"missing={int(data.isna().sum().sum())}"
    )

print("\n===== TAMBON DISTRIBUTION =====")
print(
    tambon.groupby(["year", "province_id"])
    ["tambon_code_6"]
    .nunique()
    .to_string()
)

print("\n===== CORRELATION DATA =====")
print(
    correlations[
        ["analysis", "n", "spearman_rho"]
    ].to_string(index=False)
)

print("\n===== SAVED FILES =====")
for path in sorted(OUTPUT.glob("dashboard_*.csv")):
    print(path.relative_to(ROOT))

print("\nDashboard analysis data prepared.")
