
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# อ่านข้อมูล HRDI ที่ผ่านการคัดเลือกแล้ว
df = pd.read_csv(
    DATA / "hrdi_clean_2022_2023.csv",
    encoding="utf-8-sig",
    dtype=str
)

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["month"] = pd.to_numeric(df["month"], errors="coerce")
df["rainfall_mm"] = pd.to_numeric(
    df["rainfall_mm"], errors="coerce"
)

# ใช้รหัสสถานีร่วมกับพิกัด
station_cols = [
    "CODE_REF", "STA_TH", "PROVINCE",
    "AMPHOE", "TAMBON", "LAT", "LONG"
]

# รายการสถานีทั้งหมด
stations = df[station_cols].drop_duplicates()

# สร้างตารางเดือนที่ควรมี: 12 เดือน x 2 ปี
periods = pd.MultiIndex.from_product(
    [[2022, 2023], range(1, 13)],
    names=["year", "month"]
).to_frame(index=False)

# จับคู่ทุกสถานีกับทุกเดือนที่ควรมี
expected = stations.merge(periods, how="cross")

# ตรวจว่ามีข้อมูลในเดือนนั้นหรือไม่
actual = df[station_cols + [
    "year", "month", "rainfall_mm", "source_type"
]].copy()

coverage = expected.merge(
    actual,
    on=station_cols + ["year", "month"],
    how="left",
    indicator=True,
    validate="one_to_one"
)

coverage["status"] = "AVAILABLE"
coverage.loc[
    coverage["_merge"] == "left_only", "status"
] = "MISSING_MONTH"
coverage.loc[
    (coverage["_merge"] == "both")
    & coverage["rainfall_mm"].isna(), "status"
] = "MISSING_RAINFALL"

# บันทึกผลรายสถานี-เดือน
coverage.to_csv(
    REPORTS / "hrdi_monthly_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

# สรุปความครบถ้วนรายสถานี-ปี
summary = coverage.groupby(
    station_cols + ["year"], dropna=False
).agg(
    expected_months=("month", "count"),
    available_months=(
        "status",
        lambda s: (s == "AVAILABLE").sum()
    ),
    missing_months=(
        "status",
        lambda s: (s == "MISSING_MONTH").sum()
    ),
    missing_rainfall=(
        "status",
        lambda s: (s == "MISSING_RAINFALL").sum()
    )
).reset_index()

summary["completeness_percent"] = (
    summary["available_months"]
    / summary["expected_months"] * 100
).round(2)

summary.to_csv(
    REPORTS / "hrdi_station_coverage_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n===== HRDI COVERAGE =====")
print("จำนวนสถานี:", len(stations))
print("จำนวนเดือนที่คาดหวัง:", len(expected))
print("เดือนที่มีค่าฝน:", (coverage["status"] == "AVAILABLE").sum())
print("เดือนที่ไม่มีแถวข้อมูล:", (coverage["status"] == "MISSING_MONTH").sum())
print("เดือนที่มีแถวแต่ฝน Missing:",
      (coverage["status"] == "MISSING_RAINFALL").sum())

print("\n===== COMPLETENESS =====")
print(summary["completeness_percent"].describe())

print("\nบันทึกรายงานไว้ใน reports/ แล้ว")
