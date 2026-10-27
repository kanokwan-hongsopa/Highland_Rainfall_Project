
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

df = pd.read_csv(
    REPORTS / "rice_rain_common_feb_jul.csv",
    dtype={"tambon_code_6": str, "CODE_REF": str},
    encoding="utf-8-sig"
)

# ใช้เฉพาะข้อมูลปี 2022–2023 เดือน ก.พ.–ก.ค.
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["month"] = pd.to_numeric(df["month"], errors="coerce")

for col in ["rainfall_mm", "AvgRain"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df[
    df["year"].isin([2022, 2023])
    & df["month"].between(2, 7)
].copy()

# ตรวจความครบถ้วนก่อนรวมข้อมูล
assert not df.duplicated(
    ["year", "month", "CODE_REF"]
).any(), "Duplicate station-month keys"

assert df["rainfall_mm"].notna().all()
assert df["AvgRain"].notna().all()

# ขั้นแรก: เฉลี่ย HRDI ของสถานีในตำบลเดียวกัน
# HII เป็นข้อมูลระดับจังหวัด จึงใช้ค่าเดิม ไม่เฉลี่ยซ้ำตามจำนวนสถานี
monthly = df.groupby(
    ["year", "month", "tambon_code_6"],
    as_index=False
).agg(
    hrdi_mean_rain=("rainfall_mm", "mean"),
    hii_avg_rain=("AvgRain", "first"),
    station_count=("CODE_REF", "nunique")
)

# ตรวจว่า HII จังหวัดเดียวกันไม่ขัดแย้งกัน
hii_check = df.groupby(
    ["year", "month", "tambon_code_6"]
)["AvgRain"].nunique()

assert (hii_check == 1).all(), (
    "Inconsistent HII values within tambon-month"
)

# ขั้นที่สอง: รวมค่าฝน 6 เดือน
annual_window = monthly.groupby(
    ["year", "tambon_code_6"],
    as_index=False
).agg(
    hrdi_feb_jul_total=("hrdi_mean_rain", "sum"),
    hii_feb_jul_total=("hii_avg_rain", "sum"),
    months=("month", "nunique"),
    station_count=("station_count", "max")
)

# ต้องครบ 6 เดือน
assert (annual_window["months"] == 6).all(), (
    "Incomplete Feb-Jul rainfall window"
)

print("\n===== TAMBON-YEAR RAIN SUMMARY =====")
print(
    annual_window.groupby("year").agg(
        tambons=("tambon_code_6", "nunique"),
        total_rows=("year", "size"),
        multi_station_tambons=(
            "station_count",
            lambda x: int((x > 1).sum())
        ),
        hrdi_median=("hrdi_feb_jul_total", "median"),
        hii_median=("hii_feb_jul_total", "median")
    ).to_string()
)

print("\n===== MULTI-STATION TAMBONS =====")
print(
    annual_window[
        annual_window["station_count"] > 1
    ].to_string(index=False)
)

monthly.to_csv(
    PROCESSED / "rice_rain_tambon_month_feb_jul.csv",
    index=False,
    encoding="utf-8-sig"
)

annual_window.to_csv(
    PROCESSED / "rice_rain_tambon_year_feb_jul.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved tambon-month and tambon-year rainfall data.")
