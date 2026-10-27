
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลข้าวโพดจากขั้นที่ 23
df = pd.read_csv(
    REPORTS / "maize_crop_timing_review.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# คอลัมน์ที่ต้องการตรวจ
columns = [
    "source_file",
    "year",
    "db_year",
    "db_month",
    "db_season",
    "tambon_code_6",
    "product_id_normalized",
    "plant_name",
    "area_plant",
    "area_harvest",
    "product_harvest",
    "product_avg"
]

available = [c for c in columns if c in df.columns]

print("\n===== AVAILABLE COLUMNS =====")
print(available)

# เรียงตามปี เดือน และตำบล
sort_cols = [
    c for c in ["year", "db_month", "tambon_code_6"]
    if c in df.columns
]

df = df.sort_values(sort_cols)

print("\n===== MAIZE RECORD DETAILS =====")
print(df[available].to_string(index=False))

# ตรวจรูปแบบปีและเดือน
print("\n===== YEAR / MONTH / SEASON =====")
print(
    df.groupby(
        ["year", "db_year", "db_month", "db_season"],
        dropna=False
    ).size().to_string()
)

# ตรวจข้อมูลเดือนที่ขาด
print("\n===== MISSING TIME VALUES =====")
for col in ["db_year", "db_month", "db_season"]:
    print(f"{col}: {df[col].isna().sum()} missing")

# บันทึกผลสำหรับตรวจสอบ
output = REPORTS / "maize_timing_detail.csv"

df[available].to_csv(
    output,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nSaved: {output}")
