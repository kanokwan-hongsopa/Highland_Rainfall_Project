
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# 1. อ่านข้อมูล HRDI
df = pd.read_csv(
    RAW / "HRDI_meteo.csv",
    dtype=str,
    encoding="utf-8-sig"
)
df.columns = df.columns.str.strip()

# 2. แปลงปี พ.ศ. / ค.ศ.
year = pd.to_numeric(df["YEAR"], errors="coerce")
df["_year"] = year.where(year < 2400, year - 543)

# 3. แปลงเดือนภาษาไทยและภาษาอังกฤษ
thai_month_map = {
    "ม.ค.": 1, "ก.พ.": 2, "มี.ค.": 3,
    "เม.ย.": 4, "พ.ค.": 5, "มิ.ย.": 6,
    "ก.ค.": 7, "ส.ค.": 8, "ก.ย.": 9,
    "ต.ค.": 10, "พ.ย.": 11, "ธ.ค.": 12
}

english_month_map = {
    "JAN": 1, "FEB": 2, "MAR": 3,
    "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9,
    "OCT": 10, "NOV": 11, "DEC": 12
}

month_text = (
    df["MONTH"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["_month"] = pd.to_numeric(
    month_text, errors="coerce"
)

df["_month"] = df["_month"].fillna(
    month_text.map(thai_month_map)
)

df["_month"] = df["_month"].fillna(
    month_text.str[:3].map(english_month_map)
)

# 4. กรองเฉพาะปีและจังหวัดที่ศึกษา
PROVINCES = {
    "เชียงใหม่", "เชียงราย", "น่าน",
    "ตาก", "กำแพงเพชร", "พิษณุโลก",
    "เพชรบูรณ์", "กาญจนบุรี", "แม่ฮ่องสอน"
}

df = df[
    df["_year"].isin([2022, 2023])
    & df["PROVINCE"].str.strip().isin(PROVINCES)
].copy()

print("\n===== MONTH VALIDATION =====")
print("จำนวนแถวที่ศึกษา:", len(df))
print("เดือนที่แปลงไม่ได้:", df["_month"].isna().sum())
print(
    "เดือนที่พบ:",
    sorted(df["_month"].dropna().unique().tolist())
)

# 5. ตรวจจำนวนข้อมูลจากแต่ละแหล่ง
print("\n===== DATA SOURCES =====")
print(df["DATA SOURCE"].value_counts(dropna=False))

# 6. ตรวจข้อมูลซ้ำตามสถานี-ปี-เดือน
station_key = [
    "STA_TH", "LAT", "LONG", "_year", "_month"
]

duplicates = df[
    df.duplicated(station_key, keep=False)
].sort_values(station_key)

print("\n===== DUPLICATES =====")
print(f"แถวที่คีย์ซ้ำ: {len(duplicates):,}")

if not duplicates.empty:
    print(
        duplicates[[
            "STA_TH", "PROVINCE", "_year",
            "_month", "DATA SOURCE", "RAINFALL"
        ]].head(20).to_string(index=False)
    )

# 7. แยกตรวจว่าซ้ำภายในแหล่งเดียวกันหรือข้ามแหล่ง
source_key = station_key + ["DATA SOURCE"]

same_source_dups = df[
    df.duplicated(source_key, keep=False)
]

print("\n===== SOURCE DUPLICATES =====")
print("แถวที่คีย์ซ้ำภายในแหล่งเดียวกัน:", len(same_source_dups))

# 8. บันทึกรายงาน
duplicates.to_csv(
    REPORTS / "hrdi_source_duplicates.csv",
    index=False,
    encoding="utf-8-sig"
)

same_source_dups.to_csv(
    REPORTS / "hrdi_same_source_duplicates.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลตรวจเรียบร้อยแล้ว")
