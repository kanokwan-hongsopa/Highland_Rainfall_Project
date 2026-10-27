
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

df = pd.read_csv(
    REPORTS / "crop_with_plant_names.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# ตรวจข้อมูลที่ไม่มีชื่อพืช
unmatched = df[df["plant_name"].isna()].copy()

print("\n===== UNMATCHED PLANTS =====")
print("จำนวนแถวที่จับคู่ไม่ได้:", len(unmatched))

columns = [
    "source_file", "year", "tambon_code_6",
    "product_id_original", "product_id_normalized",
    "product_group_id", "product_breed_id"
]

available = [c for c in columns if c in df.columns]

if not unmatched.empty:
    print(unmatched[available].to_string(index=False))

unmatched.to_csv(
    REPORTS / "unmatched_plant_rows.csv",
    index=False,
    encoding="utf-8-sig"
)

# ตรวจความพร้อมของพืชหลัก
print("\n===== MAIN CROP COVERAGE =====")

for code in ["011000", "020030", "013000"]:
    crop = df[
        df["product_id_normalized"] == code
    ].copy()

    print(f"\nรหัสพืช: {code}")

    if crop.empty:
        print("ไม่พบข้อมูล")
        continue

    print("ชื่อพืช:", crop["plant_name"].dropna().unique().tolist())

    for col in ["area_harvest", "product_harvest", "product_avg"]:
        crop[col] = pd.to_numeric(crop[col], errors="coerce")

    crop["valid_yield"] = (
        (crop["area_harvest"] > 0)
        & (crop["product_harvest"] >= 0)
        & crop["product_avg"].notna()
        & (crop["product_avg"] >= 0)
    )

    summary = crop.groupby("year").agg(
        rows=("year", "size"),
        tambons=("tambon_code_6", "nunique"),
        valid_rows=("valid_yield", "sum")
    )

    print(summary.to_string())

    valid = crop[crop["valid_yield"]]

    t2022 = set(
        valid.loc[valid["year"] == "2022", "tambon_code_6"]
    )
    t2023 = set(
        valid.loc[valid["year"] == "2023", "tambon_code_6"]
    )

    print("ตำบลที่มีผลผลิตใช้ได้ทั้งสองปี:", len(t2022 & t2023))

print("\nตรวจสอบขั้นที่ 19 เรียบร้อยแล้ว")
