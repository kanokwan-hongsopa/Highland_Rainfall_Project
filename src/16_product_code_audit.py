
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

hrdi = pd.read_csv(
    REPORTS / "hrdi_crop_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

codes = set(
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
        df["tambon_code_6"].isin(codes)
        & df["year"].isin(["2022", "2023"])
    ].copy()

    for col in ["area_harvest", "product_harvest", "product_avg"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["valid_yield"] = (
        (df["area_harvest"] > 0)
        & (df["product_harvest"] >= 0)
        & df["product_avg"].notna()
        & (df["product_avg"] >= 0)
    )

    frames.append(df)

combined = pd.concat(frames, ignore_index=True)

summary = combined.groupby(
    ["year", "product_id"]
).agg(
    rows=("product_id", "size"),
    tambons=("tambon_code_6", "nunique"),
    valid_rows=("valid_yield", "sum"),
    valid_tambons=(
        "tambon_code_6",
        lambda s: s[
            combined.loc[s.index, "valid_yield"]
        ].nunique()
    )
).reset_index()

codes_2022 = set(
    summary.loc[summary["year"] == "2022", "product_id"]
)
codes_2023 = set(
    summary.loc[summary["year"] == "2023", "product_id"]
)

shared = sorted(codes_2022 & codes_2023)

print("\n===== SHARED PRODUCT CODES =====")
print("รหัสที่พบทั้งสองปี:", shared)

print("\n===== SHARED CODE DETAILS =====")
print(
    summary[
        summary["product_id"].isin(shared)
    ].sort_values(
        ["product_id", "year"]
    ).to_string(index=False)
)

print("\n===== TOP PRODUCTS 2022 =====")
print(
    summary[summary["year"] == "2022"]
    .sort_values("valid_tambons", ascending=False)
    .head(10).to_string(index=False)
)

print("\n===== TOP PRODUCTS 2023 =====")
print(
    summary[summary["year"] == "2023"]
    .sort_values("valid_tambons", ascending=False)
    .head(10).to_string(index=False)
)

summary.to_csv(
    REPORTS / "product_code_audit.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
