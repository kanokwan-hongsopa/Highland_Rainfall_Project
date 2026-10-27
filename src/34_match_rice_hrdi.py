
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

rice = pd.read_csv(
    PROCESSED / "rice_tambon_year_scenarios.csv",
    dtype={"tambon_code_6": str, "year": int},
    encoding="utf-8-sig"
)

stations = pd.read_csv(
    REPORTS / "hrdi_crop_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

rain = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# เลือกสถานีที่มีรหัสตำบลจับคู่สำเร็จ
stations = stations[
    stations["tambon_code_6"].notna()
].copy()

station_cols = [
    "tambon_code_6", "CODE_REF", "STA_TH",
    "province", "district", "subdistrict"
]

stations = stations[station_cols].drop_duplicates()

rain["year"] = pd.to_numeric(
    rain["year"], errors="coerce"
)
rain["month"] = pd.to_numeric(
    rain["month"], errors="coerce"
)
rain["rainfall_mm"] = pd.to_numeric(
    rain["rainfall_mm"], errors="coerce"
)

# เก็บค่าฝนที่ใช้ได้เท่านั้น
valid_rain = rain[
    rain["year"].isin([2022, 2023])
    & rain["month"].between(1, 12)
    & rain["rainfall_mm"].notna()
    & (rain["rainfall_mm"] >= 0)
].copy()

# ตรวจสถานี-ปี-เดือนซ้ำ
dup = valid_rain.duplicated(
    ["CODE_REF", "year", "month"]
).sum()

print("\n===== SOURCE VALIDATION =====")
print("Duplicate station-month keys:", dup)

if dup:
    raise ValueError("Duplicate HRDI station-month keys")

# จับคู่ผลผลิตกับสถานีในตำบลเดียวกัน
rice_stations = rice.merge(
    stations,
    on="tambon_code_6",
    how="left",
    validate="many_to_many",
    indicator=True
)

print("\n===== RICE-STATION MATCH =====")
print(rice_stations["_merge"].value_counts().to_string())

unmatched = rice_stations[
    rice_stations["_merge"] != "both"
].copy()

if not unmatched.empty:
    print("\nUnmatched rice tambons:")
    print(
        unmatched[
            ["scenario", "year", "tambon_code_6"]
        ].drop_duplicates().to_string(index=False)
    )

rice_stations = rice_stations.drop(columns="_merge")

# จับคู่ข้อมูลฝนรายเดือนของแต่ละสถานี
matched = rice_stations.merge(
    valid_rain[
        ["CODE_REF", "year", "month",
         "rainfall_mm", "source_type"]
    ],
    on=["CODE_REF", "year"],
    how="left",
    validate="many_to_many"
)

print("\n===== HRDI MATCH SUMMARY =====")
print("Rows after merge:", len(matched))
print("Matched rainfall rows:", matched["rainfall_mm"].notna().sum())

coverage = matched.groupby(
    ["scenario", "year", "tambon_code_6", "CODE_REF"]
).agg(
    valid_months=("month", "nunique"),
    total_rain_mm=("rainfall_mm", "sum")
).reset_index()

# ฝนรวมใช้แสดงประกอบเท่านั้น
# ห้ามเปรียบเทียบข้ามปีหากเดือนที่มีข้อมูลไม่เท่ากัน
print("\n===== COVERAGE SUMMARY =====")
print(
    coverage.groupby(["scenario", "year"]).agg(
        stations=("CODE_REF", "nunique"),
        station_years=("CODE_REF", "size"),
        complete_12_months=(
            "valid_months",
            lambda x: int((x == 12).sum())
        ),
        incomplete_station_years=(
            "valid_months",
            lambda x: int((x < 12).sum())
        )
    ).to_string()
)

print("\n===== MONTHLY STATION COVERAGE =====")
monthly = matched.groupby(
    ["scenario", "year", "month"]
)["CODE_REF"].nunique().reset_index(
    name="stations_with_rain"
)

print(
    monthly.pivot_table(
        index=["scenario", "month"],
        columns="year",
        values="stations_with_rain",
        fill_value=0
    ).to_string()
)

matched.to_csv(
    PROCESSED / "rice_hrdi_station_monthly.csv",
    index=False,
    encoding="utf-8-sig"
)

coverage.to_csv(
    REPORTS / "rice_hrdi_station_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved HRDI matching reports.")
