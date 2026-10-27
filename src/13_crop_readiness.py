
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
    ("crop_file_2022", "crop_2022_normalized.csv"),
    ("crop_file_2023", "crop_2023_normalized.csv")
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
        & (df["product_avg"].notna())
        & (df["product_avg"] >= 0)
    )

    frames.append(df)

combined = pd.concat(
    frames, ignore_index=True
)

print("\n===== CROP READINESS =====")

summary = combined.groupby(
    ["source_file", "year"]
).agg(
    rows=("product_id", "size"),
    tambons=("tambon_code_6", "nunique"),
    products=("product_id", "nunique"),
    valid_yield_rows=("valid_yield", "sum")
).reset_index()

print(summary.to_string(index=False))

key_cols = [
    "year",
    "db_month",
    "tambon_code_6",
    "product_group_id",
    "product_id",
    "product_breed_id",
    "db_season"
]

duplicates = combined[
    combined.duplicated(
        subset=key_cols,
        keep=False
    )
].sort_values(key_cols)

print("\n===== POSSIBLE DUPLICATES =====")
print("แถวที่มีคีย์ซ้ำ:", len(duplicates))

if not duplicates.empty:
    print(
        duplicates[
            ["source_file"] + key_cols
        ].head(20).to_string(index=False)
    )

summary.to_csv(
    REPORTS / "crop_readiness_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

duplicates.to_csv(
    REPORTS / "crop_possible_duplicates.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
