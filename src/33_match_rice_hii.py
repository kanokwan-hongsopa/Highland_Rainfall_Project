
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

rice = pd.read_csv(
    PROCESSED / "rice_tambon_year_scenarios.csv",
    dtype={"tambon_code_6": str, "year": int},
    encoding="utf-8-sig"
)

hii = pd.read_csv(
    REPORTS / "hii_scope_validation.csv",
    encoding="utf-8-sig"
)

# ใช้รหัสจังหวัดสองหลักแรกจากรหัสตำบล 6 หลัก
rice["province_id"] = pd.to_numeric(
    rice["tambon_code_6"].str[:2],
    errors="coerce"
)

# แยกปีและเดือนของ HII
hii["YEAR"] = pd.to_numeric(
    hii["YEAR"], errors="coerce"
)
hii["MONTH"] = pd.to_numeric(
    hii["MONTH"], errors="coerce"
)

# ใช้เฉพาะคอลัมน์ที่จำเป็น
hii_monthly = hii[
    ["YEAR", "MONTH", "PROV_ID", "PROV_T", "AvgRain"]
].copy()

# ตรวจคีย์ HII ก่อน merge
assert not hii_monthly.duplicated(
    ["YEAR", "MONTH", "PROV_ID"]
).any(), "Duplicate HII province-month keys"

# จับคู่ปีและจังหวัด
# แต่ละตำบล-ปีจะมีข้อมูลฝน 12 เดือน
merged = rice.merge(
    hii_monthly,
    left_on=["year", "province_id"],
    right_on=["YEAR", "PROV_ID"],
    how="left",
    validate="many_to_many",
    indicator=True
)

print("\n===== MATCH SUMMARY =====")
print("Rice tambon-year rows:", len(rice))
print("Expected merged rows:", len(rice) * 12)
print("Actual merged rows:", len(merged))
print("\nMerge status:")
print(merged["_merge"].value_counts().to_string())

# ตรวจเดือนครบต่อแต่ละตำบล-ปีและสถานการณ์
coverage = merged.groupby(
    ["scenario", "year", "tambon_code_6"]
).agg(
    months=("MONTH", "nunique"),
    valid_rain_months=("AvgRain", "count")
).reset_index()

print("\n===== HII COVERAGE PER TAMBON-YEAR =====")
print(
    coverage.groupby(["scenario", "year"]).agg(
        tambons=("tambon_code_6", "nunique"),
        complete_12_months=("months", lambda s: int((s == 12).sum())),
        incomplete=("months", lambda s: int((s < 12).sum()))
    ).to_string()
)

# ตรวจความถูกต้องของจำนวนแถว
if len(merged) != len(rice) * 12:
    raise ValueError("Unexpected merged row count")

if (merged["_merge"] != "both").any():
    raise ValueError("Unmatched HII records found")

merged = merged.drop(columns=["_merge"])

merged.to_csv(
    PROCESSED / "rice_hii_monthly_matched.csv",
    index=False,
    encoding="utf-8-sig"
)

coverage.to_csv(
    REPORTS / "rice_hii_monthly_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved matched rice-HII monthly dataset.")
