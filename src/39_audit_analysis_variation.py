
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

df = pd.read_csv(
    PROCESSED / "rice_rain_analysis_feb_jul.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

# ใช้สถานการณ์หลักก่อน
df = df[df["scenario"] == "all_valid_records"].copy()

df["province_id"] = df["tambon_code_6"].str[:2]

variables = [
    "weighted_yield",
    "hrdi_feb_jul_total",
    "hii_feb_jul_total"
]

print("\n===== VARIABLE DISTRIBUTION =====")
for year, group in df.groupby("year"):
    print(f"\nYear {year}")
    print(
        group[variables].describe().round(3).to_string()
    )

# ตรวจว่าผลผลิตมีค่าเท่ากันมากน้อยเพียงใด
print("\n===== YIELD VARIATION =====")
for year, group in df.groupby("year"):
    print(
        f"Year {year}: "
        f"rows={len(group)}, "
        f"unique_yield={group['weighted_yield'].nunique()}, "
        f"unique_hrdi={group['hrdi_feb_jul_total'].nunique()}, "
        f"unique_hii={group['hii_feb_jul_total'].nunique()}"
    )

# ตรวจการเปลี่ยนแปลงของตำบลเดียวกันระหว่างสองปี
panel = df.pivot(
    index="tambon_code_6",
    columns="year",
    values=variables
)

panel.columns = [
    f"{variable}_{year}"
    for variable, year in panel.columns
]

panel = panel.dropna().copy()

for variable in variables:
    panel[f"{variable}_change"] = (
        panel[f"{variable}_2023"]
        - panel[f"{variable}_2022"]
    )

print("\n===== WITHIN-TAMBON CHANGES =====")
change_cols = [
    f"{variable}_change"
    for variable in variables
]

print(
    panel[change_cols].describe().round(3).to_string()
)

# ตรวจว่าข้อมูล HII ซ้ำกันในระดับจังหวัด
print("\n===== PROVINCE-LEVEL HII STRUCTURE =====")
province = df.groupby(
    ["year", "province_id"]
).agg(
    tambons=("tambon_code_6", "nunique"),
    unique_hii=("hii_feb_jul_total", "nunique"),
    unique_hrdi=("hrdi_feb_jul_total", "nunique")
).reset_index()

print(province.to_string(index=False))

# ตรวจค่าผลผลิตที่ซ้ำบ่อย
print("\n===== MOST COMMON YIELD VALUES =====")
for year, group in df.groupby("year"):
    print(f"\nYear {year}")
    print(
        group["weighted_yield"]
        .round(3)
        .value_counts()
        .head(10)
        .to_string()
    )

panel.reset_index().to_csv(
    REPORTS / "rice_rain_within_tambon_changes.csv",
    index=False,
    encoding="utf-8-sig"
)

province.to_csv(
    REPORTS / "rice_rain_province_structure.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved variation audit reports.")
