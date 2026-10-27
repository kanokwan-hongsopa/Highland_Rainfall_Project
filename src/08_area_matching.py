
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

FILES = {
    "CROP_2022": "plant01_65.csv",
    "CROP_2023": "5.-01-2566.csv"
}

PROVINCE_CODES = {
    50: "เชียงใหม่", 57: "เชียงราย",
    55: "น่าน", 63: "ตาก",
    62: "กำแพงเพชร", 65: "พิษณุโลก",
    67: "เพชรบูรณ์", 71: "กาญจนบุรี",
    58: "แม่ฮ่องสอน"
}

def normalize_year(series):
    y = pd.to_numeric(series, errors="coerce")
    return y.where(y < 2400, y - 543)

def digits(series):
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
    )

results = []
area_tables = []

for label, filename in FILES.items():
    df = pd.read_csv(
        RAW / filename,
        dtype=str,
        encoding="utf-8-sig",
        low_memory=False
    )

    df["year"] = normalize_year(df["db_year"])

    province = digits(df["code_province_id"])
    amphur = digits(df["code_amphur_id"])
    tambon = digits(df["code_tambon_id"])

    province_num = pd.to_numeric(
        province, errors="coerce"
    )

    df["province_name"] = province_num.map(
        PROVINCE_CODES
    )

    df = df[
        df["year"].isin([2022, 2023])
        & df["province_name"].notna()
    ].copy()

    province = province.loc[df.index]
    amphur = amphur.loc[df.index]
    tambon = tambon.loc[df.index]

    # ไฟล์ปี 2022 ใช้รหัสย่อย
    if label == "CROP_2022":
        df["tambon_code_6"] = (
            province.str.zfill(2)
            + amphur.str.zfill(2)
            + tambon.str.zfill(2)
        )
    else:
        # ไฟล์ปี 2023 ใช้รหัสตำบล 6 หลัก
        df["tambon_code_6"] = tambon.str.zfill(6)

    # ตรวจความสอดคล้องของรหัสกับจังหวัด
    df["code_valid"] = (
        df["tambon_code_6"].str.fullmatch(
            r"\d{6}", na=False
        )
        & df["tambon_code_6"].str[:2].eq(
            province.str.zfill(2)
        )
    )

    print(f"\n===== {label} =====")
    print("จำนวนแถว:", len(df))
    print("รหัสตำบลถูกตามรูปแบบ:",
          int(df["code_valid"].sum()))
    print("รหัสไม่ผ่านการตรวจ:",
          int((~df["code_valid"]).sum()))

    print("จำนวนตำบลที่ไม่ซ้ำ:",
          df.loc[
              df["code_valid"], "tambon_code_6"
          ].nunique())

    # บันทึกรหัสพื้นที่ที่พบ
    areas = df[
        ["year", "province_name", "tambon_code_6",
         "code_valid"]
    ].drop_duplicates().copy()

    areas["dataset"] = label
    area_tables.append(areas)

    results.append({
        "dataset": label,
        "rows": len(df),
        "valid_code_rows": int(df["code_valid"].sum()),
        "invalid_code_rows": int(
            (~df["code_valid"]).sum()
        ),
        "unique_tambons": df.loc[
            df["code_valid"], "tambon_code_6"
        ].nunique()
    })

    df.to_csv(
        REPORTS / f"{label.lower()}_normalized.csv",
        index=False,
        encoding="utf-8-sig"
    )

pd.DataFrame(results).to_csv(
    REPORTS / "area_code_validation.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.concat(area_tables, ignore_index=True).to_csv(
    REPORTS / "crop_tambon_codes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nตรวจรูปแบบรหัสพื้นที่เสร็จแล้ว")
print("บันทึกรายงานไว้ใน reports/")
