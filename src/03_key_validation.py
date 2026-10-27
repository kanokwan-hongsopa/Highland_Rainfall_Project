
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

PROVINCE_CODES = {50, 57, 55, 63, 62, 65, 67, 71, 58}
PROVINCES = {
    "เชียงใหม่", "เชียงราย", "น่าน",
    "ตาก", "กำแพงเพชร", "พิษณุโลก",
    "เพชรบูรณ์", "กาญจนบุรี", "แม่ฮ่องสอน"
}

def load_csv(filename):
    return pd.read_csv(
        RAW / filename,
        encoding="utf-8-sig",
        dtype=str,
        low_memory=False
    )

def normalize_year(series):
    y = pd.to_numeric(series, errors="coerce")
    return y.where(y < 2400, y - 543)

def normalize_month(series):
    return pd.to_numeric(series, errors="coerce")

# โหลดและกรอง HRDI
hrdi = load_csv("HRDI_meteo.csv")
hrdi["_year"] = normalize_year(hrdi["YEAR"])
hrdi["_month"] = normalize_month(hrdi["MONTH"])
hrdi = hrdi[
    hrdi["_year"].isin([2022, 2023])
    & hrdi["PROVINCE"].str.strip().isin(PROVINCES)
].copy()

# ตรวจคีย์สถานี-ปี-เดือน
hrdi_key = ["CODE_REF", "_year", "_month"]
hrdi_dups = hrdi[
    hrdi.duplicated(hrdi_key, keep=False)
].sort_values(hrdi_key)

hrdi_dups.to_csv(
    REPORTS / "hrdi_duplicate_keys.csv",
    index=False,
    encoding="utf-8-sig"
)

# โหลดและกรอง HII
hii = load_csv("spatial-rain-hii.csv")
hii["_year"] = normalize_year(hii["YEAR"])
hii["_month"] = normalize_month(hii["MONTH"])
hii = hii[
    hii["_year"].isin([2022, 2023])
    & hii["PROV_T"].str.strip().isin(PROVINCES)
].copy()

hii_key = ["PROV_T", "_year", "_month"]
hii_dups = hii[
    hii.duplicated(hii_key, keep=False)
].sort_values(hii_key)

hii_dups.to_csv(
    REPORTS / "hii_duplicate_keys.csv",
    index=False,
    encoding="utf-8-sig"
)

# โหลดและกรองข้อมูลผลผลิต
def load_crop(filename):
    df = load_csv(filename)
    df["_year"] = normalize_year(df["db_year"])
    df["_month"] = normalize_month(df["db_month"])
    df["_province"] = pd.to_numeric(
        df["code_province_id"], errors="coerce"
    )
    return df[
        df["_year"].isin([2022, 2023])
        & df["_province"].isin(PROVINCE_CODES)
    ].copy()

crop22 = load_crop("plant01_65.csv")
crop23 = load_crop("5.-01-2566.csv")

# ตรวจการซ้ำภายในไฟล์แต่ละปี
crop_key = [
    "_year", "_month", "code_province_id",
    "code_amphur_id", "code_tambon_id",
    "product_id", "product_breed_id", "db_season"
]

crop22_dups = crop22[
    crop22.duplicated(crop_key, keep=False)
]
crop23_dups = crop23[
    crop23.duplicated(crop_key, keep=False)
]

crop22_dups.to_csv(
    REPORTS / "crop2022_duplicate_keys.csv",
    index=False,
    encoding="utf-8-sig"
)
crop23_dups.to_csv(
    REPORTS / "crop2023_duplicate_keys.csv",
    index=False,
    encoding="utf-8-sig"
)

# ปี 2022 ใช้รหัสย่อย ส่วนปี 2023 ใช้รหัสเต็ม
# แปลงเป็นรหัสมาตรฐาน 6 หลักเพื่อเทียบข้ามไฟล์
def make_area_code(df, is_2022):
    province = pd.to_numeric(
        df["code_province_id"], errors="coerce"
    )
    amphur = pd.to_numeric(
        df["code_amphur_id"], errors="coerce"
    )
    tambon = pd.to_numeric(
        df["code_tambon_id"], errors="coerce"
    )

    if is_2022:
        full_code = (
            province * 10000 + amphur * 100 + tambon
        )
    else:
        full_code = tambon

    return full_code.astype("Int64").astype("string").str.zfill(6)

crop22["_area_code"] = make_area_code(crop22, True)
crop23["_area_code"] = make_area_code(crop23, False)

# ตรวจข้อมูลปี 2023 ที่ปรากฏในทั้งสองไฟล์
overlap22 = crop22[crop22["_year"] == 2023].copy()
overlap23 = crop23[crop23["_year"] == 2023].copy()

compare_key = [
    "_year", "_month", "_area_code",
    "product_id", "product_breed_id", "db_season"
]

overlap = overlap22.merge(
    overlap23,
    on=compare_key,
    how="inner",
    suffixes=("_file22", "_file23")
)

overlap.to_csv(
    REPORTS / "crop_2023_overlap.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n===== KEY VALIDATION =====")
print(f"HRDI แถวที่คีย์ซ้ำ: {len(hrdi_dups):,}")
print(f"HII แถวที่คีย์ซ้ำ: {len(hii_dups):,}")
print(f"CROP_2022 แถวที่คีย์ซ้ำ: {len(crop22_dups):,}")
print(f"CROP_2023 แถวที่คีย์ซ้ำ: {len(crop23_dups):,}")
print(f"คู่ข้อมูลปี 2023 ที่ทับซ้อนกัน: {len(overlap):,}")

print("\nบันทึกรายงานใน reports/ เรียบร้อยแล้ว")
