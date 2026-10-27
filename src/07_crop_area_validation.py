
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

FILES = {
    "CROP_2022": "plant01_65.csv",
    "CROP_2023": "5.-01-2566.csv"
}

PROVINCE_CODES = {
    50: "เชียงใหม่",
    57: "เชียงราย",
    55: "น่าน",
    63: "ตาก",
    62: "กำแพงเพชร",
    65: "พิษณุโลก",
    67: "เพชรบูรณ์",
    71: "กาญจนบุรี",
    58: "แม่ฮ่องสอน"
}

# 1. อ่านข้อมูลสถานี HRDI
hrdi = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

hrdi["year"] = pd.to_numeric(
    hrdi["year"], errors="coerce"
)

station_areas = hrdi[
    ["CODE_REF", "STA_TH", "PROVINCE",
     "AMPHOE", "TAMBON", "LAT", "LONG"]
].drop_duplicates()

print("\n===== HRDI AREAS =====")
print("จำนวนสถานี/พื้นที่ที่แตกต่างกัน:", len(station_areas))
print("จำนวนจังหวัด:", station_areas["PROVINCE"].nunique())
print("จำนวนอำเภอ:", station_areas[
    ["PROVINCE", "AMPHOE"]
].drop_duplicates().shape[0])
print("จำนวนตำบล:", station_areas[
    ["PROVINCE", "AMPHOE", "TAMBON"]
].drop_duplicates().shape[0])

station_areas.to_csv(
    REPORTS / "hrdi_station_areas.csv",
    index=False,
    encoding="utf-8-sig"
)

# 2. ตรวจรหัสพื้นที่ของผลผลิต
all_results = []

for label, filename in FILES.items():
    df = pd.read_csv(
        RAW / filename,
        dtype=str,
        encoding="utf-8-sig",
        low_memory=False
    )

    year = pd.to_numeric(df["db_year"], errors="coerce")
    df["year"] = year.where(year < 2400, year - 543)

    province_code = pd.to_numeric(
        df["code_province_id"], errors="coerce"
    )

    df["province_name"] = province_code.map(
        PROVINCE_CODES
    )

    df = df[
        df["year"].isin([2022, 2023])
        & df["province_name"].notna()
    ].copy()

    print(f"\n===== {label} =====")
    print("จำนวนแถว:", len(df))
    print("จำนวนจังหวัด:", df["province_name"].nunique())
    print("จำนวนรหัสอำเภอ:",
          df["code_amphur_id"].nunique())
    print("จำนวนรหัสตำบล:",
          df["code_tambon_id"].nunique())

    # ตรวจตัวอย่างรหัสจริง โดยไม่สมมติรูปแบบ
    example = df[
        ["province_name", "code_province_id",
         "code_amphur_id", "code_tambon_id",
         "year", "product_id"]
    ].drop_duplicates().head(20)

    print("\nตัวอย่างรหัสพื้นที่:")
    print(example.to_string(index=False))

    # ตรวจการตรงกันระดับจังหวัดก่อน
    hrdi_provinces = set(
        station_areas["PROVINCE"].dropna().str.strip()
    )

    df["province_match"] = (
        df["province_name"].isin(hrdi_provinces)
    )

    all_results.append({
        "dataset": label,
        "rows": len(df),
        "years": ",".join(
            map(str, sorted(df["year"].dropna().unique()))
        ),
        "provinces": df["province_name"].nunique(),
        "rows_matching_hrdi_province":
            int(df["province_match"].sum()),
        "unique_products": df["product_id"].nunique()
    })

    df.to_csv(
        REPORTS / f"{label.lower()}_area_scope.csv",
        index=False,
        encoding="utf-8-sig"
    )

summary = pd.DataFrame(all_results)
summary.to_csv(
    REPORTS / "crop_area_validation_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n===== SUMMARY =====")
print(summary.to_string(index=False))
print("\nบันทึกรายงานใน reports/ เรียบร้อยแล้ว")
