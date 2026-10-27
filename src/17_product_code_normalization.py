
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

hrdi = pd.read_csv(
    REPORTS / "hrdi_crop_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

valid_codes = set(
    hrdi["tambon_code_6"].dropna().str.zfill(6)
)

frames = []

for source, filename in [
    ("file_2022", "crop_2022_normalized.csv"),
    ("file_2023", "crop_2023_normalized.csv")
]:
    df = pd.read_csv(
        REPORTS / filename,
        dtype=str,
        encoding="utf-8-sig"
    )

    df["source_file"] = source
    df["tambon_code_6"] = (
        df["tambon_code_6"].str.zfill(6)
    )

    df = df[
        df["tambon_code_6"].isin(valid_codes)
        & df["year"].isin(["2022", "2023"])
    ].copy()

    # เก็บรหัสพืชเดิมไว้
    df["product_id_original"] = df["product_id"]

    # ปรับรหัสพืชให้เป็น 6 หลัก
    df["product_id_normalized"] = (
        df["product_id"].str.strip().str.zfill(6)
    )

    for col in [
        "area_harvest",
        "product_harvest",
        "product_avg"
    ]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    df["valid_yield"] = (
        (df["area_harvest"] > 0)
        & (df["product_harvest"] >= 0)
        & df["product_avg"].notna()
        & (df["product_avg"] >= 0)
    )

    frames.append(df)

combined = pd.concat(frames, ignore_index=True)

# ตรวจรหัสพืชที่พบทั้งสองปี
p2022 = set(combined.loc[
    combined["year"] == "2022",
    "product_id_normalized"
])

p2023 = set(combined.loc[
    combined["year"] == "2023",
    "product_id_normalized"
])

shared = sorted(p2022 & p2023)

print("\n===== NORMALIZED PRODUCT CODES =====")
print("รหัสพืชที่ตรงกันทั้งสองปี:", len(shared))
print("ตัวอย่างรหัส:", shared[:20])

# ตรวจเฉพาะแถวที่มีผลผลิตใช้ได้
valid = combined[combined["valid_yield"]].copy()

presence = valid[
    ["product_id_normalized", "tambon_code_6", "year"]
].drop_duplicates()

year_count = presence.groupby(
    ["product_id_normalized", "tambon_code_6"]
)["year"].nunique().reset_index(name="years_present")

both_years = year_count[
    year_count["years_present"] == 2
]

summary = both_years.groupby(
    "product_id_normalized"
).agg(
    tambons_both_years=("tambon_code_6", "nunique")
).reset_index()

summary = summary.sort_values(
    "tambons_both_years",
    ascending=False
)

print("\n===== MATCHED PRODUCT-TAMBON =====")
print("รหัสพืชที่มีข้อมูลใช้ได้ทั้งสองปี:",
      len(summary))
print("จำนวนคู่พืช-ตำบลที่ตรงกัน:",
      len(both_years))
print("\nTOP 20:")
print(summary.head(20).to_string(index=False))

# เก็บข้อมูลเพื่อใช้ตรวจสอบต่อ
combined.to_csv(
    REPORTS / "crop_product_codes_normalized.csv",
    index=False,
    encoding="utf-8-sig"
)

summary.to_csv(
    REPORTS / "crop_normalized_overlap.csv",
    index=False,
    encoding="utf-8-sig"
)

both_years.to_csv(
    REPORTS / "crop_normalized_tambon_overlap.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
