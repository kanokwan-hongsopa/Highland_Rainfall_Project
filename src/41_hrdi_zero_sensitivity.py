
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

keys = ["year", "tambon_code_6", "CODE_REF"]

assert not df.duplicated(keys + ["month"]).any()

# ระบุค่าศูนย์จาก HRDI ที่ต้องตรวจสอบ
df["suspect_zero"] = (
    (df["source_type"] == "HRDI")
    & (df["rainfall_mm"] == 0)
)

# สถานการณ์ 1: เก็บค่าต้นฉบับ
df["rain_original"] = df["rainfall_mm"]

# สถานการณ์ 2: แยกค่าศูนย์ HRDI เป็น missing
df["rain_flagged_zero"] = df["rainfall_mm"].mask(
    df["suspect_zero"]
)

# สถานการณ์ 3: ใช้สถานี-ปีที่ครบ 6 เดือนหลัง flag
station = df.groupby(keys).agg(
    original_months=("rain_original", "count"),
    clean_months=("rain_flagged_zero", "count"),
    suspect_zero_months=("suspect_zero", "sum")
).reset_index()

station["complete_case"] = (
    (station["original_months"] == 6)
    & (station["clean_months"] == 6)
)

print("\n===== STATION-YEAR QUALITY =====")
print(
    station.groupby("year").agg(
        station_years=("CODE_REF", "size"),
        complete_original=("original_months", lambda x: int((x == 6).sum())),
        complete_after_flag=("complete_case", "sum"),
        affected_station_years=("suspect_zero_months", lambda x: int((x > 0).sum()))
    ).to_string()
)

print("\n===== AFFECTED STATIONS =====")
print(
    station[station["suspect_zero_months"] > 0]
    .sort_values(["year", "CODE_REF"])
    .to_string(index=False)
)

# รวมผลตามตำบล-ปี โดยเก็บจำนวนสถานีที่ใช้
def aggregate_scenario(data, value_col, label, require_complete=False):
    temp = data.copy()

    if require_complete:
        allowed = station.loc[
            station["complete_case"],
            keys
        ]
        temp = temp.merge(
            allowed,
            on=keys,
            how="inner",
            validate="many_to_one"
        )

    # เฉลี่ยสถานีในตำบลเดียวกันรายเดือน
    monthly = temp.groupby(
        ["year", "tambon_code_6", "month"],
        as_index=False
    ).agg(
        rain=(value_col, "mean"),
        stations_with_value=(value_col, "count")
    )

    monthly.loc[
        monthly["stations_with_value"] == 0, "rain"
    ] = float("nan")

    result = monthly.groupby(
        ["year", "tambon_code_6"],
        as_index=False
    ).agg(
        rain_total=("rain", lambda x: x.sum(min_count=1)),
        valid_months=("rain", "count")
    )

    # ไม่รายงานผลรวมที่มีเดือนขาดเป็นผลรวม 6 เดือน
    result.loc[
        result["valid_months"] != 6,
        "rain_total"
    ] = float("nan")

    result["rain_scenario"] = label
    return result

original = aggregate_scenario(
    df, "rain_original", "original"
)

flagged = aggregate_scenario(
    df, "rain_flagged_zero", "flagged_zero"
)

complete = aggregate_scenario(
    df, "rain_flagged_zero", "complete_case",
    require_complete=True
)

result = pd.concat(
    [original, flagged, complete],
    ignore_index=True
)

print("\n===== SCENARIO COVERAGE =====")
print(
    result.groupby(["rain_scenario", "year"]).agg(
        tambons=("tambon_code_6", "nunique"),
        complete_tambons=("rain_total", "count"),
        median_rain=("rain_total", "median")
    ).to_string()
)

station.to_csv(
    REPORTS / "hrdi_station_year_zero_quality.csv",
    index=False,
    encoding="utf-8-sig"
)

result.to_csv(
    PROCESSED / "rice_hrdi_rain_sensitivity.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved HRDI sensitivity datasets.")
