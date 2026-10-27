
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

    df["valid_yield"] = (
        (df["area_harvest"] > 0)
        & (df["product_harvest"] >= 0)
        & df["product_avg"].notna()
        & (df["product_avg"] >= 0)
    )

    frames.append(df)

combined = pd.concat(frames, ignore_index=True)

print("\n===== YEAR SUMMARY =====")
print(
    combined.groupby("year").agg(
        rows=("product_id", "size"),
        tambons=("tambon_code_6", "nunique"),
        products=("product_id", "nunique"),
        valid_rows=("valid_yield", "sum")
    ).to_string()
)

# ตรวจรหัสพืชที่พบในแต่ละปี
p2022 = set(combined.loc[
    combined["year"] == "2022", "product_id"
])

p2023 = set(combined.loc[
    combined["year"] == "2023", "product_id"
])

print("\n===== PRODUCT CODE OVERLAP =====")
print("รหัสพืชปี 2022:", len(p2022))
print("รหัสพืชปี 2023:", len(p2023))
print("รหัสพืชที่ตรงกัน:", len(p2022 & p2023))

# ตรวจตำบลที่มีข้อมูลใช้ได้ทั้งสองปี
valid = combined[combined["valid_yield"]].copy()

t2022 = set(valid.loc[
    valid["year"] == "2022", "tambon_code_6"
])

t2023 = set(valid.loc[
    valid["year"] == "2023", "tambon_code_6"
])

print("\n===== VALID TAMBON OVERLAP =====")
print("ตำบลปี 2022:", len(t2022))
print("ตำบลปี 2023:", len(t2023))
print("ตำบลที่ตรงกัน:", len(t2022 & t2023))

# ตรวจคู่พืช-ตำบลที่ตรงกัน
pairs2022 = set(zip(
    valid.loc[valid["year"] == "2022", "product_id"],
    valid.loc[valid["year"] == "2022", "tambon_code_6"]
))

pairs2023 = set(zip(
    valid.loc[valid["year"] == "2023", "product_id"],
    valid.loc[valid["year"] == "2023", "tambon_code_6"]
))

print("\n===== PRODUCT-TAMBON OVERLAP =====")
print("คู่พืช-ตำบลปี 2022:", len(pairs2022))
print("คู่พืช-ตำบลปี 2023:", len(pairs2023))
print("คู่ที่ตรงกันทั้งสองปี:", len(pairs2022 & pairs2023))

# บันทึกคู่ที่ตรงกัน
overlap = pd.DataFrame(
    sorted(pairs2022 & pairs2023),
    columns=["product_id", "tambon_code_6"]
)

overlap.to_csv(
    REPORTS / "crop_overlap_diagnosis.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกผลใน reports/ เรียบร้อยแล้ว")
