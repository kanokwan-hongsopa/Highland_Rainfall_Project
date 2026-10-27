
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

# ข้อมูลสถานีที่จับคู่กับพืชทั้ง 3 ชนิด
matched = pd.read_csv(
    REPORTS / "crop_readiness_matched_stations.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# ข้อมูลฝน HRDI ที่ทำความสะอาดแล้ว
rain = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# เตรียมข้อมูลฝน
rain["year"] = pd.to_numeric(rain["year"], errors="coerce")
rain["month"] = pd.to_numeric(rain["month"], errors="coerce")
rain["rainfall_mm"] = pd.to_numeric(
    rain["rainfall_mm"], errors="coerce"
)

# ใช้เฉพาะค่าฝนที่ไม่ติดลบและไม่เป็นค่าว่าง
rain = rain[
    rain["year"].isin([2022, 2023])
    & rain["month"].between(1, 12)
    & rain["rainfall_mm"].notna()
    & (rain["rainfall_mm"] >= 0)
].copy()

# นับสถานีไม่ซ้ำในแต่ละพืช
stations = matched[
    ["plant_code", "plant_name", "CODE_REF"]
].dropna().drop_duplicates()

# เชื่อมสถานีกับข้อมูลฝน
combined = stations.merge(
    rain[["CODE_REF", "year", "month", "rainfall_mm"]],
    on="CODE_REF",
    how="left"
)

# จำนวนสถานีทั้งหมดของแต่ละพืช
total = stations.groupby(
    ["plant_code", "plant_name"]
)["CODE_REF"].nunique().rename("total_stations")

# นับสถานีที่มีฝนในแต่ละเดือน
coverage = combined.groupby(
    ["plant_code", "plant_name", "year", "month"]
)["CODE_REF"].nunique().rename("valid_stations")

coverage = coverage.reset_index()

# สร้างตารางครบทุกเดือน แม้เดือนนั้นไม่มีข้อมูลเลย
plants = stations[["plant_code", "plant_name"]].drop_duplicates()

calendar = pd.MultiIndex.from_product(
    [[2022, 2023], range(1, 13)],
    names=["year", "month"]
).to_frame(index=False)

full = plants.merge(calendar, how="cross")

full = full.merge(
    coverage,
    on=["plant_code", "plant_name", "year", "month"],
    how="left"
)

full["valid_stations"] = (
    full["valid_stations"].fillna(0).astype(int)
)

full = full.merge(
    total.reset_index(),
    on=["plant_code", "plant_name"],
    how="left"
)

full["coverage_pct"] = (
    full["valid_stations"] / full["total_stations"] * 100
).round(2)

# สรุปเป็นตารางเดือน
print("\n===== MONTHLY RAIN COVERAGE =====")
for name in full["plant_name"].unique():
    subset = full[full["plant_name"] == name]
    print(f"\n--- {name} ---")
    print(
        subset.pivot(
            index="month",
            columns="year",
            values="valid_stations"
        ).to_string()
    )
    print("Total stations:", subset["total_stations"].iloc[0])

# นับเดือนที่ทุกสถานีมีข้อมูลครบ
summary = full.groupby(
    ["plant_code", "plant_name", "year"]
).agg(
    total_stations=("total_stations", "first"),
    months_full=("coverage_pct", lambda x: (x == 100).sum()),
    months_with_data=("valid_stations", lambda x: (x > 0).sum())
).reset_index()

print("\n===== COVERAGE SUMMARY =====")
print(summary.to_string(index=False))

# บันทึกผล
full.to_csv(
    REPORTS / "crop_rain_monthly_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)

summary.to_csv(
    REPORTS / "crop_rain_coverage_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved comparison reports.")
