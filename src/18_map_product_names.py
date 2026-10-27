
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
REFERENCE = ROOT / "data" / "reference"

REPORTS.mkdir(exist_ok=True)

# 1. โหลดข้อมูลที่ปรับรหัสพืชแล้วจากขั้นที่ 17
crop = pd.read_csv(
    REPORTS / "crop_product_codes_normalized.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# 2. โหลดตารางชื่อพืชจากกรมส่งเสริมการเกษตร
plants = pd.read_csv(
    REFERENCE / "production_plant.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# 3. ตรวจสอบคอลัมน์ที่จำเป็น
required_crop = {
    "product_id_normalized",
    "tambon_code_6",
    "year"
}

required_plants = {
    "plant_code",
    "plant_name",
    "group_plant_code",
    "group_plant_name"
}

missing_crop = required_crop - set(crop.columns)
missing_plants = required_plants - set(plants.columns)

if missing_crop or missing_plants:
    raise ValueError(
        f"Missing crop columns: {missing_crop}\n"
        f"Missing plant columns: {missing_plants}"
    )

# 4. ปรับรหัสให้เป็นรูปแบบเดียวกัน
crop["product_id_normalized"] = (
    crop["product_id_normalized"]
    .astype("string")
    .str.strip()
    .str.zfill(6)
)

plants["plant_code_normalized"] = (
    plants["plant_code"]
    .astype("string")
    .str.strip()
    .str.zfill(6)
)

# 5. ตรวจว่ารหัสเดียวกันมีหลายชื่อหรือไม่
dictionary = plants[
    [
        "plant_code_normalized",
        "plant_name",
        "group_plant_code",
        "group_plant_name"
    ]
].drop_duplicates()

conflicts = (
    dictionary.groupby("plant_code_normalized")
    .agg(
        plant_names=("plant_name", "nunique"),
        group_names=("group_plant_name", "nunique")
    )
    .reset_index()
)

conflicts = conflicts[
    (conflicts["plant_names"] > 1)
    | (conflicts["group_names"] > 1)
]

print("\n===== DICTIONARY CONFLICTS =====")
print("รหัสที่มีชื่อหรือกลุ่มขัดแย้ง:", len(conflicts))

conflicts.to_csv(
    REPORTS / "plant_dictionary_conflicts.csv",
    index=False,
    encoding="utf-8-sig"
)

if not conflicts.empty:
    raise ValueError(
        "พบรหัสพืชที่มีชื่อหรือกลุ่มขัดแย้ง "
        "กรุณาตรวจรายงานก่อนเชื่อมข้อมูล"
    )

dictionary = dictionary.drop_duplicates(
    subset=["plant_code_normalized"]
)

# 6. เชื่อมชื่อพืชกับข้อมูลผลผลิต
merged = crop.merge(
    dictionary,
    left_on="product_id_normalized",
    right_on="plant_code_normalized",
    how="left",
    validate="many_to_one",
    indicator=True
)

merged["plant_match_status"] = merged["_merge"].map({
    "both": "matched",
    "left_only": "unmatched",
    "right_only": "unused"
}).astype(str)

# 7. สรุปผลการจับคู่
print("\n===== PLANT NAME MATCHING =====")
print("แถวข้อมูลผลผลิต:", len(merged))
print("จับคู่ชื่อพืชได้:", (merged["plant_match_status"] == "matched").sum())
print("จับคู่ไม่ได้:", (merged["plant_match_status"] == "unmatched").sum())

print("\n===== TOP 3 PRODUCT CODES =====")

for code in ["011000", "020030", "013000"]:
    subset = merged[
        merged["product_id_normalized"] == code
    ]

    names = sorted(
        subset["plant_name"].dropna().unique().tolist()
    )

    print(
        f"{code}: "
        f"ชื่อพืช={names}, "
        f"จำนวนแถว={len(subset)}"
    )

# 8. บันทึกรหัสที่ยังไม่มีชื่อ
unmatched = merged[
    merged["plant_match_status"] == "unmatched"
][["product_id_normalized"]].drop_duplicates()

unmatched.to_csv(
    REPORTS / "unmatched_product_codes.csv",
    index=False,
    encoding="utf-8-sig"
)

# 9. บันทึกข้อมูลพร้อมชื่อพืช
merged = merged.drop(
    columns=["_merge", "plant_code_normalized"]
)

merged.to_csv(
    REPORTS / "crop_with_plant_names.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
