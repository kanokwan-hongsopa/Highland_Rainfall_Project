
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

analysis = pd.read_csv(
    PROCESSED / "rice_rain_analysis_feb_jul.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

sensitivity = pd.read_csv(
    PROCESSED / "rice_hrdi_rain_sensitivity.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

# ใช้ผลผลิตข้าวนาปีสถานการณ์หลัก
analysis = analysis[
    analysis["scenario"] == "all_valid_records"
].copy()

# ใช้ฝน HRDI แบบ complete-case
clean_rain = sensitivity[
    sensitivity["rain_scenario"] == "complete_case"
][
    ["year", "tambon_code_6", "rain_total", "valid_months"]
].copy()

clean_rain = clean_rain.rename(
    columns={"rain_total": "hrdi_clean_feb_jul_total"}
)

keys = ["year", "tambon_code_6"]

assert not analysis.duplicated(keys).any()
assert not clean_rain.duplicated(keys).any()

merged = analysis.merge(
    clean_rain,
    on=keys,
    how="left",
    validate="one_to_one"
)

# ต้องมีฝน HRDI หลังตรวจครบ 6 เดือน
eligible = merged[
    merged["hrdi_clean_feb_jul_total"].notna()
    & (merged["valid_months"] == 6)
].copy()

print("\n===== ELIGIBLE ROWS BY YEAR =====")
print(
    eligible.groupby("year")["tambon_code_6"]
    .nunique().to_string()
)

# เลือกเฉพาะตำบลที่มีข้อมูลครบทั้งสองปี
years_per_tambon = eligible.groupby(
    "tambon_code_6"
)["year"].nunique()

balanced_codes = years_per_tambon[
    years_per_tambon == 2
].index

balanced = eligible[
    eligible["tambon_code_6"].isin(balanced_codes)
].copy()

print("\n===== BALANCED PANEL SUMMARY =====")
print("Tambons:", balanced["tambon_code_6"].nunique())
print("Rows:", len(balanced))

print("\nBy year:")
print(
    balanced.groupby("year").agg(
        tambons=("tambon_code_6", "nunique"),
        median_yield=("weighted_yield", "median"),
        median_hrdi=("hrdi_clean_feb_jul_total", "median"),
        median_hii=("hii_feb_jul_total", "median")
    ).to_string()
)

# ตรวจความครบถ้วน
required = [
    "weighted_yield",
    "hrdi_clean_feb_jul_total",
    "hii_feb_jul_total"
]

assert balanced[required].notna().all().all()
assert not balanced.duplicated(keys).any()

# แสดงตำบลที่ไม่ผ่านเงื่อนไข
excluded = sorted(
    set(analysis["tambon_code_6"])
    - set(balanced_codes)
)

print("\n===== EXCLUDED TAMBONS =====")
print(excluded)

balanced.to_csv(
    PROCESSED / "rice_rain_balanced_panel.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame({
    "excluded_tambon_code": excluded
}).to_csv(
    REPORTS / "rice_rain_excluded_tambons.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved balanced rice-rain panel.")
