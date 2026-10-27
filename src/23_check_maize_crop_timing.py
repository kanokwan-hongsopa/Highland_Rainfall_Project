
from pathlib import Path
import pandas as pd

# กำหนดตำแหน่งไฟล์
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลพืชที่จับคู่ชื่อเรียบร้อยแล้ว
df = pd.read_csv(
    REPORTS / "crop_with_plant_names.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# เลือกเฉพาะข้าวโพดเลี้ยงสัตว์ ปี 2022–2023
maize = df[
    (df["product_id_normalized"] == "020030")
    & (df["year"].isin(["2022", "2023"]))
].copy()

print("\n===== AVAILABLE TIME COLUMNS =====")
time_cols = [
    "source_file", "year", "db_year",
    "db_month", "db_season"
]
print([c for c in time_cols if c in maize.columns])

# ตรวจจำนวนข้อมูลแต่ละปี
print("\n===== YEAR AND SOURCE =====")
print(
    maize.groupby(
        ["year", "source_file"],
        dropna=False
    ).size().to_string()
)

# ตรวจเดือนที่มีการบันทึกข้อมูลข้าวโพด
if "db_month" in maize.columns:
    print("\n===== CROP MONTH DISTRIBUTION =====")
    print(
        maize.groupby(
            ["year", "db_month"],
            dropna=False
        ).agg(
            rows=("product_id_normalized", "size"),
            tambons=("tambon_code_6", "nunique")
        ).to_string()
    )

# ตรวจฤดูเพาะปลูก
if "db_season" in maize.columns:
    print("\n===== CROP SEASON DISTRIBUTION =====")
    print(
        maize.groupby(
            ["year", "db_season"],
            dropna=False
        ).agg(
            rows=("product_id_normalized", "size"),
            tambons=("tambon_code_6", "nunique")
        ).to_string()
    )

# ตรวจเดือนและฤดูเพาะปลูกร่วมกัน
if {"db_month", "db_season"}.issubset(maize.columns):
    print("\n===== MONTH AND SEASON COMBINATIONS =====")
    print(
        maize.groupby(
            ["year", "db_month", "db_season"],
            dropna=False
        ).size().to_string()
    )

# บันทึกผลไว้ตรวจสอบต่อ
maize.to_csv(
    REPORTS / "maize_crop_timing_review.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
