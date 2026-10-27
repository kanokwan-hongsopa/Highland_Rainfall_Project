
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

PROCESSED.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

PROVINCES = {
    "เชียงใหม่", "เชียงราย", "น่าน",
    "ตาก", "กำแพงเพชร", "พิษณุโลก",
    "เพชรบูรณ์", "กาญจนบุรี", "แม่ฮ่องสอน"
}

MONTHS = {
    "ม.ค.": 1, "ก.พ.": 2, "มี.ค.": 3,
    "เม.ย.": 4, "พ.ค.": 5, "มิ.ย.": 6,
    "ก.ค.": 7, "ส.ค.": 8, "ก.ย.": 9,
    "ต.ค.": 10, "พ.ย.": 11, "ธ.ค.": 12
}

# 1. อ่านข้อมูลต้นฉบับ
df = pd.read_csv(
    RAW / "HRDI_meteo.csv",
    dtype=str,
    encoding="utf-8-sig"
)
df.columns = df.columns.str.strip()
df["_original_row"] = range(1, len(df) + 1)

# 2. จัดรูปแบบปี เดือน และจังหวัด
year = pd.to_numeric(df["YEAR"], errors="coerce")
df["year"] = year.where(year < 2400, year - 543)

month_text = df["MONTH"].astype("string").str.strip()
df["month"] = pd.to_numeric(month_text, errors="coerce")
df["month"] = df["month"].fillna(month_text.map(MONTHS))

df["province_clean"] = df["PROVINCE"].astype("string").str.strip()
df["rainfall_mm"] = pd.to_numeric(
    df["RAINFALL"], errors="coerce"
)

df = df[
    df["year"].isin([2022, 2023])
    & df["province_clean"].isin(PROVINCES)
].copy()

# 3. ตรวจคุณภาพค่าฝน
df["rain_missing"] = df["rainfall_mm"].isna()
df["rain_negative"] = df["rainfall_mm"] < 0
df["rain_zero"] = df["rainfall_mm"] == 0


# จัดรูปแบบชื่อแหล่งข้อมูลก่อนจำแนก
source_text = (
    df["DATA SOURCE"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["source_type"] = pd.Series(
    pd.NA, index=df.index, dtype="string"
)

df.loc[
    source_text.eq("hrdi weather station"),
    "source_type"
] = "HRDI"

df.loc[
    source_text.str.contains(
        "openweathermap.org", na=False
    ),
    "source_type"
] = "OWM"

print("\n===== SOURCE CHECK =====")
print(df["source_type"].value_counts(dropna=False))


# 4. ตรวจรายการซ้ำตามสถานี-ปี-เดือน
key = ["STA_TH", "LAT", "LONG", "year", "month"]

df["key_duplicate"] = df.duplicated(key, keep=False)

# 5. เลือกข้อมูล HRDI ก่อน OWM
# เฉพาะแถวที่ค่าฝนไม่หายและไม่ติดลบ
df["valid_rain"] = (
    df["rainfall_mm"].notna()
    & (df["rainfall_mm"] >= 0)
)

df["source_priority"] = df["source_type"].map({
    "HRDI": 0,
    "OWM": 1
}).fillna(2)

df = df.sort_values(
    ["valid_rain", "source_priority", "_original_row"],
    ascending=[False, True, True]
)

selected = df.drop_duplicates(
    subset=key,
    keep="first"
).copy()

# 6. ระบุกรณีที่ควรตรวจเพิ่มเติม
selected["needs_review"] = (
    selected["rain_zero"]
    | selected["rain_missing"]
    | selected["rain_negative"]
    | selected["month"].isna()
    | selected["source_type"].isna()
)

# 7. บันทึกข้อมูลและรายงาน
selected.sort_values(key).to_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    index=False,
    encoding="utf-8-sig"
)

df[df["key_duplicate"]].sort_values(key).to_csv(
    REPORTS / "hrdi_duplicate_review.csv",
    index=False,
    encoding="utf-8-sig"
)

selected[selected["needs_review"]].to_csv(
    REPORTS / "hrdi_rain_review.csv",
    index=False,
    encoding="utf-8-sig"
)

# 8. สรุปผล
print("\n===== HRDI CLEANING =====")
print("จำนวนแถวก่อนจัดการซ้ำ:", len(df))
print("จำนวนแถวหลังจัดการซ้ำ:", len(selected))
print("แถวที่ถูกคัดออกจากชุดวิเคราะห์:", len(df) - len(selected))
print("ฝน Missing:", selected["rain_missing"].sum())
print("ฝนติดลบ:", selected["rain_negative"].sum())
print("ฝนเท่ากับ 0:", selected["rain_zero"].sum())
print("รายการที่ต้องตรวจเพิ่มเติม:", selected["needs_review"].sum())
print("\nบันทึกผลใน data/processed/ และ reports/")
