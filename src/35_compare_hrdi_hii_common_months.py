
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

hrdi = pd.read_csv(
    PROCESSED / "rice_hrdi_station_monthly.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

hii = pd.read_csv(
    REPORTS / "hii_scope_validation.csv",
    encoding="utf-8-sig"
)

# เลือกสถานการณ์หลัก ไม่รวมข้อมูลซ้ำจาก sensitivity analysis
hrdi = hrdi[
    hrdi["scenario"] == "all_valid_records"
].copy()

hrdi["year"] = pd.to_numeric(hrdi["year"])
hrdi["month"] = pd.to_numeric(hrdi["month"])
hrdi["rainfall_mm"] = pd.to_numeric(
    hrdi["rainfall_mm"], errors="coerce"
)

hrdi["province_id"] = pd.to_numeric(
    hrdi["tambon_code_6"].str[:2],
    errors="coerce"
)

hii["YEAR"] = pd.to_numeric(hii["YEAR"])
hii["MONTH"] = pd.to_numeric(hii["MONTH"])
hii["PROV_ID"] = pd.to_numeric(hii["PROV_ID"])

# จับคู่ตามปี เดือน และจังหวัด
combined = hrdi.merge(
    hii[["YEAR", "MONTH", "PROV_ID", "AvgRain"]],
    left_on=["year", "month", "province_id"],
    right_on=["YEAR", "MONTH", "PROV_ID"],
    how="left",
    validate="many_to_one",
    indicator=True
)

print("\n===== HRDI-HII MATCH =====")
print(combined["_merge"].value_counts().to_string())

# ตรวจช่วงเดือนที่มีข้อมูลครบทั้งสองปีทุกสถานี
station_month = combined.groupby(
    ["CODE_REF", "year", "month"]
).agg(
    hrdi_present=("rainfall_mm", lambda x: x.notna().any()),
    hii_present=("AvgRain", lambda x: x.notna().any())
).reset_index()

station_month["both_present"] = (
    station_month["hrdi_present"]
    & station_month["hii_present"]
)

station_count = station_month["CODE_REF"].nunique()

monthly = station_month.groupby(
    ["year", "month"]
)["both_present"].sum().reset_index(
    name="matched_stations"
)

monthly["coverage_pct"] = (
    monthly["matched_stations"] / station_count * 100
).round(2)

print("\n===== MONTHLY COMMON COVERAGE =====")
print(
    monthly.pivot(
        index="month",
        columns="year",
        values="matched_stations"
    ).to_string()
)

print("\nTotal stations:", station_count)

# ตรวจเดือนที่ครบทุกสถานีทั้งสองปี
full = monthly[
    monthly["matched_stations"] == station_count
]

common_months = (
    set(full[full["year"] == 2022]["month"])
    & set(full[full["year"] == 2023]["month"])
)

print("\n===== COMMON COMPLETE MONTHS =====")
print(sorted(common_months))

# บันทึกผล
combined.to_csv(
    PROCESSED / "rice_hrdi_hii_monthly_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)

monthly.to_csv(
    REPORTS / "rice_hrdi_hii_common_month_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved common-month comparison reports.")
