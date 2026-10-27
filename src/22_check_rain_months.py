
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

stations = pd.read_csv(
    REPORTS / "maize_hrdi_matched_areas.csv",
    dtype=str,
    encoding="utf-8-sig"
)

rain = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

stations = stations[
    stations["match_status"].eq("matched")
][["CODE_REF", "tambon_code_6"]].drop_duplicates()

stations["CODE_REF"] = stations["CODE_REF"].str.strip()

rain["CODE_REF"] = rain["CODE_REF"].str.strip()
rain["month"] = pd.to_numeric(
    rain["month"], errors="coerce"
)
rain["rainfall_mm"] = pd.to_numeric(
    rain["rainfall_mm"], errors="coerce"
)

rain = rain[
    rain["year"].isin(["2022", "2023"])
    & rain["CODE_REF"].isin(stations["CODE_REF"])
].copy()

rain = rain[
    rain["month"].between(1, 12)
    & rain["rainfall_mm"].notna()
    & (rain["rainfall_mm"] >= 0)
].copy()

if rain.duplicated(
    ["CODE_REF", "year", "month"]
).any():
    raise ValueError("พบข้อมูลสถานี-ปี-เดือนซ้ำ")

# จำนวนสถานีที่มีฝนใช้ได้ในแต่ละเดือน
counts = (
    rain.groupby(["year", "month"])["CODE_REF"]
    .nunique()
    .reset_index(name="stations_with_data")
)

full = pd.MultiIndex.from_product(
    [["2022", "2023"], range(1, 13)],
    names=["year", "month"]
).to_frame(index=False)

counts = full.merge(
    counts,
    on=["year", "month"],
    how="left"
)

counts["stations_with_data"] = (
    counts["stations_with_data"]
    .fillna(0)
    .astype(int)
)

pivot = counts.pivot(
    index="month",
    columns="year",
    values="stations_with_data"
)

print("\n===== STATIONS WITH VALID RAIN BY MONTH =====")
print(pivot.to_string())

# ตรวจเดือนที่สถานีเดียวกันมีข้อมูลทั้งสองปี
presence = rain[
    ["CODE_REF", "year", "month"]
].drop_duplicates()

common = (
    presence.groupby(["CODE_REF", "month"])["year"]
    .nunique()
    .reset_index(name="years_present")
)

common = common[common["years_present"] == 2]

common_counts = (
    common.groupby("month")["CODE_REF"]
    .nunique()
    .reindex(range(1, 13), fill_value=0)
)

print("\n===== SAME STATIONS WITH DATA IN BOTH YEARS =====")
print(common_counts.to_string())

counts.to_csv(
    REPORTS / "maize_hrdi_month_availability.csv",
    index=False,
    encoding="utf-8-sig"
)

common.to_csv(
    REPORTS / "maize_hrdi_common_station_months.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
