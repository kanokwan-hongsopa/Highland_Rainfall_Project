
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลพืชที่จับคู่ชื่อแล้ว
df = pd.read_csv(
    REPORTS / "crop_with_plant_names.csv",
    dtype=str,
    encoding="utf-8-sig"
)

plants = {
    "011000": "ข้าวนาปี",
    "020030": "ข้าวโพดเลี้ยงสัตว์",
    "013000": "ข้าวไร่"
}

# เลือกพืช 3 ชนิด ในปี 2022–2023
df = df[
    df["product_id_normalized"].isin(plants)
    & df["year"].isin(["2022", "2023"])
].copy()

df["plant_label"] = df["product_id_normalized"].map(plants)

# ตรวจผลผลิตที่ใช้ได้
df["yield_value"] = pd.to_numeric(
    df["product_avg"], errors="coerce"
)
df["harvest_area"] = pd.to_numeric(
    df["area_harvest"], errors="coerce"
)

df["valid_yield"] = (
    df["yield_value"].notna()
    & (df["yield_value"] > 0)
    & (df["harvest_area"] > 0)
)

# จำกัดเฉพาะตำบลที่มีผลผลิตใช้ได้ทั้งสองปี
valid = df[df["valid_yield"]].copy()

year_counts = valid.groupby(
    ["plant_label", "tambon_code_6"]
)["year"].nunique().reset_index(name="year_count")

both = year_counts[
    year_counts["year_count"] == 2
][["plant_label", "tambon_code_6"]]

selected = df.merge(
    both,
    on=["plant_label", "tambon_code_6"],
    how="inner"
)

print("\n===== CROP TIMING COMPARISON =====")

for code, name in plants.items():
    part = selected[
        selected["product_id_normalized"] == code
    ].copy()

    print(f"\n--- {name} ---")

    print("\nMONTH DISTRIBUTION")
    print(
        part.groupby(
            ["year", "db_month"],
            dropna=False
        ).agg(
            rows=("year", "size"),
            tambons=("tambon_code_6", "nunique"),
            valid_yield_rows=("valid_yield", "sum")
        ).to_string()
    )

    print("\nSEASON DISTRIBUTION")
    print(
        part.groupby(
            ["year", "db_season"],
            dropna=False
        ).size().to_string()
    )

print("\n===== DATA QUALITY SUMMARY =====")

summary = selected.groupby(
    ["plant_label", "year"]
).agg(
    rows=("year", "size"),
    tambons=("tambon_code_6", "nunique"),
    valid_yield_rows=("valid_yield", "sum"),
    months_recorded=("db_month", "nunique")
).reset_index()

print(summary.to_string(index=False))

# บันทึกผล
selected.to_csv(
    REPORTS / "crop_timing_three_plants.csv",
    index=False,
    encoding="utf-8-sig"
)

summary.to_csv(
    REPORTS / "crop_timing_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved reports successfully.")
