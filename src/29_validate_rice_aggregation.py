
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลข้าวนาปีจากขั้นที่ 27
df = pd.read_csv(
    REPORTS / "crop_timing_three_plants.csv",
    dtype=str,
    encoding="utf-8-sig"
)

rice = df[
    df["product_id_normalized"] == "011000"
].copy()

# แปลงตัวเลข
numeric_cols = [
    "area_plant",
    "area_harvest",
    "product_harvest",
    "product_avg"
]

for col in numeric_cols:
    rice[col] = pd.to_numeric(
        rice[col], errors="coerce"
    )

# ตรวจความผิดปกติของแต่ละรายการ
rice["missing_value"] = rice[
    numeric_cols
].isna().any(axis=1)

rice["negative_value"] = (
    rice[numeric_cols] < 0
).any(axis=1)

rice["harvest_exceeds_plant"] = (
    rice["area_harvest"] > rice["area_plant"]
)

rice["invalid_area"] = (
    rice["area_harvest"].isna()
    | (rice["area_harvest"] <= 0)
)

# คำนวณผลผลิตเฉลี่ยจากผลผลิตและพื้นที่
rice["calculated_yield"] = np.where(
    rice["area_harvest"] > 0,
    rice["product_harvest"] / rice["area_harvest"],
    np.nan
)

# ตรวจความต่างระหว่างค่าที่รายงานกับค่าที่คำนวณ
rice["yield_difference_pct"] = np.where(
    rice["product_avg"] > 0,
    abs(
        rice["calculated_yield"] - rice["product_avg"]
    ) / rice["product_avg"] * 100,
    np.nan
)

rice["yield_mismatch"] = (
    rice["yield_difference_pct"] > 1
)

# ค่าสูงผิดกลุ่ม ใช้สำหรับแจ้งเตือนเท่านั้น
q1 = rice["calculated_yield"].quantile(0.25)
q3 = rice["calculated_yield"].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

rice["yield_outlier"] = (
    (rice["calculated_yield"] < lower)
    | (rice["calculated_yield"] > upper)
)

# ตรวจรหัสพันธุ์ซ้ำภายในตำบลและปี
rice["same_breed_multiple_rows"] = rice.duplicated(
    subset=[
        "year",
        "tambon_code_6",
        "product_breed_id"
    ],
    keep=False
)

flags = [
    "missing_value",
    "negative_value",
    "harvest_exceeds_plant",
    "invalid_area",
    "yield_mismatch",
    "yield_outlier",
    "same_breed_multiple_rows"
]

print("\n===== RICE QUALITY SUMMARY =====")
print("Total rows:", len(rice))
print("Tambons:", rice["tambon_code_6"].nunique())

for flag in flags:
    print(f"{flag}: {int(rice[flag].sum())}")

# แสดงรายการที่ต้องตรวจเพิ่มเติม
rice["needs_review"] = rice[flags].any(axis=1)

review = rice[rice["needs_review"]].copy()

show_cols = [
    "year",
    "tambon_code_6",
    "db_month",
    "product_breed_id",
    "area_plant",
    "area_harvest",
    "product_harvest",
    "product_avg",
    "calculated_yield",
    "yield_difference_pct"
] + flags

print("\n===== RECORDS NEEDING REVIEW =====")

if review.empty:
    print("No flagged records.")
else:
    print(
        review[show_cols].to_string(index=False)
    )

# สรุประดับตำบล-ปีเพื่อดูจำนวนรายการ
# ยังไม่รวมค่าพื้นที่หรือผลผลิต
group_summary = rice.groupby(
    ["year", "tambon_code_6"]
).agg(
    rows=("year", "size"),
    breeds=("product_breed_id", "nunique"),
    months=("db_month", "nunique"),
    flagged_rows=("needs_review", "sum")
).reset_index()

print("\n===== TAMBON-YEAR SUMMARY =====")
print(group_summary.to_string(index=False))

# บันทึกผล
rice.to_csv(
    REPORTS / "rice_quality_validation.csv",
    index=False,
    encoding="utf-8-sig"
)

review.to_csv(
    REPORTS / "rice_quality_review.csv",
    index=False,
    encoding="utf-8-sig"
)

group_summary.to_csv(
    REPORTS / "rice_tambon_year_validation.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved validation reports.")
