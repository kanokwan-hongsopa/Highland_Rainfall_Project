
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

df = pd.read_csv(
    PROCESSED / "rice_hrdi_hii_monthly_comparison.csv",
    dtype={"tambon_code_6": str, "CODE_REF": str},
    encoding="utf-8-sig"
)

df = df[df["month"].isin([2, 3, 4, 5, 6, 7])].copy()

for col in ["rainfall_mm", "AvgRain", "year", "month"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ตรวจคีย์สถานี-ปี-เดือน
key = ["year", "CODE_REF", "month"]
duplicate_rows = int(df.duplicated(key).sum())

print("\n===== DATA INTEGRITY =====")
print("Rows:", len(df))
print("Duplicate station-year-month rows:", duplicate_rows)
print("Missing HRDI:", int(df["rainfall_mm"].isna().sum()))
print("Missing HII:", int(df["AvgRain"].isna().sum()))

# เปรียบเทียบการกระจายของค่าฝน
print("\n===== RAINFALL DISTRIBUTION =====")
summary = df.groupby("year").agg(
    hrdi_min=("rainfall_mm", "min"),
    hrdi_median=("rainfall_mm", "median"),
    hrdi_max=("rainfall_mm", "max"),
    hii_min=("AvgRain", "min"),
    hii_median=("AvgRain", "median"),
    hii_max=("AvgRain", "max")
).reset_index()

print(summary.to_string(index=False))

# ตรวจสถานีหลายแห่งในตำบลเดียวกัน
station_counts = (
    df.groupby("tambon_code_6")["CODE_REF"]
    .nunique()
    .reset_index(name="stations")
)

multi = station_counts[station_counts["stations"] > 1]

print("\n===== MULTI-STATION TAMBONS =====")
if multi.empty:
    print("None")
else:
    print(multi.to_string(index=False))

# ตรวจความครบถ้วนของ 6 เดือนต่อสถานี-ปี
coverage = df.groupby(
    ["year", "tambon_code_6", "CODE_REF"]
).agg(
    months=("month", "nunique"),
    hrdi_months=("rainfall_mm", "count"),
    hii_months=("AvgRain", "count")
).reset_index()

print("\n===== SIX-MONTH COVERAGE =====")
print(
    coverage.groupby("year").agg(
        station_years=("CODE_REF", "size"),
        complete_hrdi=("hrdi_months", lambda x: int((x == 6).sum())),
        complete_hii=("hii_months", lambda x: int((x == 6).sum()))
    ).to_string()
)

df.to_csv(
    REPORTS / "rice_rain_common_feb_jul.csv",
    index=False,
    encoding="utf-8-sig"
)

summary.to_csv(
    REPORTS / "rice_rain_distribution.csv",
    index=False,
    encoding="utf-8-sig"
)

multi.to_csv(
    REPORTS / "rice_multi_station_tambons.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved rainfall comparability reports.")
