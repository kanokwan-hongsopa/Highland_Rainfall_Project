
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

df = df[
    (df["scenario"] == "all_valid_records")
    & (df["month"].isin([2, 3, 4, 5, 6, 7]))
].copy()

df["rainfall_mm"] = pd.to_numeric(
    df["rainfall_mm"], errors="coerce"
)

# ตรวจค่าฝนศูนย์รายเดือน
zero = df[df["rainfall_mm"] == 0].copy()

print("\n===== ZERO RAINFALL SUMMARY =====")
print("Total rows:", len(df))
print("Zero rainfall rows:", len(zero))

print("\nZero rainfall by year:")
print(
    zero.groupby("year").size().to_string()
)

print("\n===== ZERO RAINFALL DETAILS =====")
columns = [
    "year", "month", "tambon_code_6",
    "CODE_REF", "STA_TH",
    "rainfall_mm", "source_type"
]

print(
    zero[columns]
    .sort_values(["year", "tambon_code_6", "month"])
    .to_string(index=False)
)

# ตรวจผลรวมฝนระดับสถานี
station_total = df.groupby(
    ["year", "tambon_code_6", "CODE_REF"],
    as_index=False
).agg(
    total_rain=("rainfall_mm", "sum"),
    zero_months=("rainfall_mm", lambda x: int((x == 0).sum())),
    valid_months=("rainfall_mm", "count"),
    source_types=("source_type", lambda x: ", ".join(
        sorted(set(x.dropna().astype(str)))
    ))
)

print("\n===== LOW RAINFALL STATIONS =====")
print(
    station_total.sort_values("total_rain")
    .head(15)
    .to_string(index=False)
)

# ตรวจสถานีที่ฝนเป็นศูนย์ครบ 6 เดือน
all_zero = station_total[
    (station_total["zero_months"] == 6)
    & (station_total["valid_months"] == 6)
]

print("\n===== ALL-ZERO STATIONS =====")
if all_zero.empty:
    print("None")
else:
    print(all_zero.to_string(index=False))

# ตรวจสัดส่วนแหล่งข้อมูล
print("\n===== SOURCE TYPE DISTRIBUTION =====")
print(
    df.groupby(["year", "source_type"])
    .agg(
        rows=("rainfall_mm", "size"),
        zero_rows=("rainfall_mm", lambda x: int((x == 0).sum()))
    )
    .to_string()
)

zero.to_csv(
    REPORTS / "hrdi_zero_rain_details.csv",
    index=False,
    encoding="utf-8-sig"
)

station_total.to_csv(
    REPORTS / "hrdi_station_rain_totals_audit.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved HRDI zero-rain audit reports.")
