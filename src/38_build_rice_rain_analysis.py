
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

rice = pd.read_csv(
    PROCESSED / "rice_tambon_year_scenarios.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

rain = pd.read_csv(
    PROCESSED / "rice_rain_tambon_year_feb_jul.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

rice["year"] = pd.to_numeric(rice["year"])
rain["year"] = pd.to_numeric(rain["year"])

keys = ["year", "tambon_code_6"]

# ตรวจว่าแต่ละสถานการณ์มีหนึ่งแถวต่อตำบล-ปี
assert not rice.duplicated(
    ["scenario"] + keys
).any(), "Duplicate rice tambon-year keys"

assert not rain.duplicated(
    keys
).any(), "Duplicate rain tambon-year keys"

# จับคู่ผลผลิตกับฝน
merged = rice.merge(
    rain,
    on=keys,
    how="left",
    validate="many_to_one",
    indicator=True
)

print("\n===== MATCH SUMMARY =====")
print("Rice rows:", len(rice))
print("Matched rows:", len(merged))
print("Unmatched rows:", int((merged["_merge"] != "both").sum()))

if (merged["_merge"] != "both").any():
    print(
        merged.loc[
            merged["_merge"] != "both",
            ["scenario", "year", "tambon_code_6"]
        ].to_string(index=False)
    )
    raise ValueError("Unmatched rice-rain records")

merged = merged.drop(columns="_merge")

# ตรวจค่าว่างและความครบถ้วน
required = [
    "weighted_yield",
    "hrdi_feb_jul_total",
    "hii_feb_jul_total"
]

print("\n===== MISSING VALUES =====")
print(merged[required].isna().sum().to_string())

print("\n===== ANALYSIS DATA SUMMARY =====")
summary = merged.groupby(
    ["scenario", "year"]
).agg(
    tambons=("tambon_code_6", "nunique"),
    rows=("year", "size"),
    median_yield=("weighted_yield", "median"),
    median_hrdi=("hrdi_feb_jul_total", "median"),
    median_hii=("hii_feb_jul_total", "median")
).reset_index()

print(summary.to_string(index=False))

# ตรวจว่ามีข้อมูลครบสองปีในแต่ละสถานการณ์กี่ตำบล
both_years = merged.groupby(
    ["scenario", "tambon_code_6"]
)["year"].nunique().reset_index(name="years")

print("\n===== TWO-YEAR PANEL COVERAGE =====")
print(
    both_years.groupby("scenario").agg(
        tambons=("tambon_code_6", "size"),
        complete_two_years=(
            "years",
            lambda x: int((x == 2).sum())
        )
    ).to_string()
)

# เก็บข้อจำกัดของช่วงฝนไว้ในข้อมูล
merged["rain_window"] = "February-July"
merged["rain_window_confirmed_crop_season"] = False
merged["rain_source_comparability_verified"] = False

merged.to_csv(
    PROCESSED / "rice_rain_analysis_feb_jul.csv",
    index=False,
    encoding="utf-8-sig"
)

summary.to_csv(
    REPORTS / "rice_rain_analysis_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved preliminary rice-rain analysis dataset.")
