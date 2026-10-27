
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
    df["tambon_code_6"] = df["tambon_code_6"].str.zfill(6)

    df = df[
        df["tambon_code_6"].isin(valid_codes)
        & df["year"].isin(["2022", "2023"])
    ].copy()

    for col in ["area_harvest", "product_harvest", "product_avg"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[
        (df["area_harvest"] > 0)
        & (df["product_harvest"] >= 0)
        & (df["product_avg"].notna())
        & (df["product_avg"] >= 0)
    ].copy()

    frames.append(df)

combined = pd.concat(frames, ignore_index=True)

# ตรวจพืชที่มีข้อมูลในตำบลเดียวกันทั้งสองปี
presence = combined[
    ["product_id", "tambon_code_6", "year"]
].drop_duplicates()

year_count = presence.groupby(
    ["product_id", "tambon_code_6"]
)["year"].nunique().reset_index(name="years_present")

both_years = year_count[
    year_count["years_present"] == 2
]

summary = both_years.groupby(
    "product_id"
).agg(
    tambons_both_years=("tambon_code_6", "nunique")
).reset_index()

summary = summary.sort_values(
    "tambons_both_years",
    ascending=False
)

print("\n===== CROP OVERLAP 2022-2023 =====")
print("รหัสพืชที่มีข้อมูลทั้งสองปีในตำบลเดียวกัน:",
      len(summary))

print("\nTOP 20 PRODUCTS:")
print(summary.head(20).to_string(index=False))

summary.to_csv(
    REPORTS / "crop_overlap_2022_2023.csv",
    index=False,
    encoding="utf-8-sig"
)

both_years.to_csv(
    REPORTS / "crop_tambon_both_years.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
