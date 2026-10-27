
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

df = pd.read_csv(
    PROCESSED / "rice_rain_balanced_panel.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

df["province_id"] = df["tambon_code_6"].str[:2]

# ตรวจความสมบูรณ์ของ panel
assert len(df) == 50, "Unexpected panel size"
assert df["tambon_code_6"].nunique() == 25
assert not df.duplicated(
    ["year", "tambon_code_6"]
).any()

print("\n===== PROVINCE DISTRIBUTION =====")

province = df.groupby(
    ["year", "province_id"]
).agg(
    tambons=("tambon_code_6", "nunique"),
    unique_hrdi=("hrdi_clean_feb_jul_total", "nunique"),
    unique_hii=("hii_feb_jul_total", "nunique"),
    median_yield=("weighted_yield", "median")
).reset_index()

print(province.to_string(index=False))

print("\n===== PROVINCE REPRESENTATION =====")

base = df[df["year"] == 2022]

representation = (
    base.groupby("province_id")
    ["tambon_code_6"]
    .nunique()
    .reset_index(name="tambons")
)

representation["share_pct"] = (
    representation["tambons"]
    / representation["tambons"].sum() * 100
).round(2)

print(representation.to_string(index=False))

print("\n===== HII INDEPENDENT VALUES =====")

print(
    df.groupby("year").agg(
        tambons=("tambon_code_6", "nunique"),
        provinces=("province_id", "nunique"),
        unique_hii_values=("hii_feb_jul_total", "nunique")
    ).to_string()
)

# ตรวจค่าฝน HII ว่าคงที่ภายในจังหวัด-ปี
hii_consistency = df.groupby(
    ["year", "province_id"]
)["hii_feb_jul_total"].nunique()

assert (hii_consistency == 1).all(), (
    "HII values inconsistent within province-year"
)

# บันทึกผล
province.to_csv(
    REPORTS / "rice_balanced_province_distribution.csv",
    index=False,
    encoding="utf-8-sig"
)

representation.to_csv(
    REPORTS / "rice_balanced_province_representation.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved province structure reports.")
