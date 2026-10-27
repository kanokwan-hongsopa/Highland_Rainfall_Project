
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "data" / "reference"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# 1. อ่าน GeoThai
with open(REF / "geo.json", "r", encoding="utf-8-sig") as f:
    geo = json.load(f)

records = []

for province in geo:
    for district in province.get("districts", []):
        for subdistrict in district.get("subdistricts", []):
            records.append({
                "province": province["name_th"],
                "district": district["name_th"],
                "subdistrict": subdistrict["name_th"],
                "tambon_code_6": str(subdistrict["code"]).zfill(6)
            })

geo_df = pd.DataFrame(records)

# 2. ปรับรูปแบบชื่อให้เทียบกันได้
def normalize_name(value):
    if pd.isna(value):
        return ""
    value = unicodedata.normalize("NFC", str(value))
    value = re.sub(r"\s+", "", value.strip())
    value = re.sub(
        r"^(จังหวัด|จ\.|อำเภอ|อ\.|เขต|ตำบล|ต\.|แขวง)",
        "", value
    )
    return value

def add_name_keys(df, cols):
    df = df.copy()
    for col in cols:
        df[col + "_key"] = df[col].map(normalize_name)
    return df

geo_df = add_name_keys(
    geo_df, ["province", "district", "subdistrict"]
)

# 3. อ่านพื้นที่สถานี HRDI
hrdi = pd.read_csv(
    REPORTS / "hrdi_station_areas.csv",
    dtype=str,
    encoding="utf-8-sig"
)

hrdi = hrdi.rename(columns={
    "PROVINCE": "province",
    "AMPHOE": "district",
    "TAMBON": "subdistrict"
})

hrdi = add_name_keys(
    hrdi, ["province", "district", "subdistrict"]
)

keys = [
    "province_key",
    "district_key",
    "subdistrict_key"
]

# ป้องกันการจับคู่หลายรหัสต่อชื่อพื้นที่เดียวกัน
ambiguous = geo_df[
    geo_df.duplicated(keys, keep=False)
].copy()

ambiguous.to_csv(
    REPORTS / "geo_ambiguous_names.csv",
    index=False,
    encoding="utf-8-sig"
)

geo_unique = geo_df[
    ~geo_df.duplicated(keys, keep=False)
]

# 4. จับคู่ HRDI กับรหัสตำบล
matched = hrdi.merge(
    geo_unique[keys + ["tambon_code_6"]],
    on=keys,
    how="left",
    validate="many_to_one",
    indicator=True
)

matched["match_status"] = matched["_merge"].map({
    "both": "matched",
    "left_only": "unmatched",
    "right_only": "unused"
}).astype(str)

matched = matched.drop(columns="_merge")

matched.to_csv(
    REPORTS / "hrdi_geo_matching.csv",
    index=False,
    encoding="utf-8-sig"
)

# 5. ตรวจว่าตำบลที่จับคู่ได้มีข้อมูลผลผลิตหรือไม่
crop_files = {
    "CROP_2022_FILE": "crop_2022_normalized.csv",
    "CROP_2023_FILE": "crop_2023_normalized.csv"
}

crop_codes = {}

for label, filename in crop_files.items():
    crop = pd.read_csv(
        REPORTS / filename,
        dtype=str,
        encoding="utf-8-sig"
    )

    valid = crop["code_valid"].str.lower().eq("true")

    crop_codes[label] = set(
        crop.loc[valid, "tambon_code_6"].dropna()
    )

    matched[label + "_has_crop"] = (
        matched["tambon_code_6"].isin(crop_codes[label])
    )

matched.to_csv(
    REPORTS / "hrdi_crop_matching.csv",
    index=False,
    encoding="utf-8-sig"
)

# 6. สรุปผล
unique_areas = matched[
    ["province_key", "district_key", "subdistrict_key",
     "tambon_code_6", "match_status",
     "CROP_2022_FILE_has_crop",
     "CROP_2023_FILE_has_crop"]
].drop_duplicates()

print("\n===== GEO REFERENCE =====")
print("จำนวนรหัสตำบลใน GeoThai:", len(geo_df))
print("รายการชื่อพื้นที่กำกวม:", len(ambiguous))

print("\n===== HRDI MATCHING =====")
print("จำนวนสถานี HRDI:", len(matched))
print("สถานีที่จับคู่ได้:",
      int(matched["tambon_code_6"].notna().sum()))
print("สถานีที่จับคู่ไม่ได้:",
      int(matched["tambon_code_6"].isna().sum()))

print("\n===== UNIQUE TAMBON MATCHING =====")
print("ตำบล HRDI ทั้งหมด:", len(unique_areas))
print("ตำบลที่จับคู่รหัสได้:",
      int(unique_areas["tambon_code_6"].notna().sum()))

for label in crop_files:
    col = label + "_has_crop"
    print(f"ตำบลที่มีผลผลิตใน {label}:",
          int(unique_areas[col].sum()))

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
