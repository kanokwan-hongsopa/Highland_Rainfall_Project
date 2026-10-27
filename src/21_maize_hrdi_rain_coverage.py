
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

matching = pd.read_csv(
    REPORTS / "maize_hrdi_matched_areas.csv",
    dtype=str,
    encoding="utf-8-sig"
)

rain = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# ใช้เฉพาะรายการที่จับคู่พื้นที่สำเร็จ
matching = matching[
    matching["match_status"].eq("matched")
].copy()

# ปรับคีย์สถานีให้ตรงกัน
for df in [matching, rain]:
    df["CODE_REF"] = (
        df["CODE_REF"].astype("string").str.strip()
    )

matching = matching[
    matching["CODE_REF"].notna()
].copy()

# ตรวจสถานีที่อยู่ในพื้นที่ข้าวโพด
stations = matching[
    ["CODE_REF", "tambon_code_6"]
].drop_duplicates()

print("\n===== MATCHED STATIONS =====")
print("จำนวนสถานี:", stations["CODE_REF"].nunique())
print("จำนวนตำบล:", stations["tambon_code_6"].nunique())

multiple = (
    stations.groupby("tambon_code_6")["CODE_REF"]
    .nunique()
    .reset_index(name="station_count")
)

print("\n===== MULTIPLE STATIONS PER TAMBON =====")
print(
    multiple[multiple["station_count"] > 1]
    .to_string(index=False)
)

# ตรวจฝนปี 2022-2023
rain = rain[
    rain["year"].isin(["2022", "2023"])
].copy()

rain["month"] = pd.to_numeric(
    rain["month"], errors="coerce"
)
rain["rainfall_mm"] = pd.to_numeric(
    rain["rainfall_mm"], errors="coerce"
)

rain["usable_rain"] = (
    rain["rainfall_mm"].notna()
    & (rain["rainfall_mm"] >= 0)
    & rain["month"].between(1, 12)
)

# เลือกเฉพาะสถานีที่เกี่ยวข้อง
rain = rain[
    rain["CODE_REF"].isin(stations["CODE_REF"])
].copy()

# ตรวจสถานี-เดือนที่ซ้ำ
duplicates = rain.duplicated(
    ["CODE_REF", "year", "month"],
    keep=False
)

print("\n===== DUPLICATE STATION MONTHS =====")
print("แถวที่มีคีย์สถานี-ปี-เดือนซ้ำ:", duplicates.sum())

if duplicates.any():
    raise ValueError(
        "พบสถานี-เดือนซ้ำ กรุณาตรวจสอบก่อนสรุปฝน"
    )

# สรุปความครบถ้วน
coverage = (
    rain.groupby(["CODE_REF", "year"])
    .agg(
        months_present=("month", "nunique"),
        valid_months=("usable_rain", "sum")
    )
    .reset_index()
)

# เติมรายการสถานี-ปีที่ไม่มีข้อมูลเลย
all_pairs = stations[["CODE_REF"]].drop_duplicates().merge(
    pd.DataFrame({"year": ["2022", "2023"]}),
    how="cross"
)

coverage = all_pairs.merge(
    coverage,
    on=["CODE_REF", "year"],
    how="left"
)

coverage[["months_present", "valid_months"]] = (
    coverage[["months_present", "valid_months"]]
    .fillna(0).astype(int)
)

coverage["missing_months"] = (
    12 - coverage["months_present"]
)

coverage["invalid_months"] = (
    coverage["months_present"] - coverage["valid_months"]
)

coverage["complete_12_months"] = (
    coverage["valid_months"] == 12
)

print("\n===== RAIN COVERAGE BY YEAR =====")
print(
    coverage.groupby("year").agg(
        stations=("CODE_REF", "nunique"),
        valid_months=("valid_months", "sum"),
        complete_stations=("complete_12_months", "sum")
    ).to_string()
)

print("\n===== VALID MONTH DISTRIBUTION =====")
print(
    coverage.groupby(["year", "valid_months"])
    .size()
    .to_string()
)

coverage.to_csv(
    REPORTS / "maize_hrdi_rain_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
