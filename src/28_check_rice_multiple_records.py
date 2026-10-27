
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลที่เตรียมไว้ในขั้นที่ 27
df = pd.read_csv(
    REPORTS / "crop_timing_three_plants.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# เลือกเฉพาะข้าวนาปี
rice = df[
    df["product_id_normalized"] == "011000"
].copy()

print("\n===== RICE YEAR SUMMARY =====")
print(
    rice.groupby("year").agg(
        rows=("year", "size"),
        tambons=("tambon_code_6", "nunique")
    ).to_string()
)

# ตรวจเดือนและรหัสฤดู
print("\n===== MONTH AND SEASON =====")
print(
    rice.groupby(
        ["year", "db_month", "db_season"],
        dropna=False
    ).agg(
        rows=("year", "size"),
        tambons=("tambon_code_6", "nunique")
    ).to_string()
)

# นับรายการต่อหนึ่งตำบลในแต่ละปี
counts = rice.groupby(
    ["year", "tambon_code_6"]
).size().reset_index(name="record_count")

multiple = counts[
    counts["record_count"] > 1
].copy()

print("\n===== TAMBONS WITH MULTIPLE RECORDS =====")
print(multiple.to_string(index=False))

# ตรวจรายละเอียดของตำบลที่มีหลายรายการ
details = rice.merge(
    multiple[["year", "tambon_code_6"]],
    on=["year", "tambon_code_6"],
    how="inner"
)

columns = [
    "year",
    "tambon_code_6",
    "db_month",
    "db_season",
    "product_group_id",
    "product_id_normalized",
    "product_breed_id",
    "area_plant",
    "area_harvest",
    "product_harvest",
    "product_avg"
]

available = [c for c in columns if c in details.columns]

print("\n===== MULTIPLE RECORD DETAILS =====")
print(
    details[available]
    .sort_values(["year", "tambon_code_6", "db_month"])
    .to_string(index=False)
)

# ตรวจรายการซ้ำตามคีย์ข้อมูล
key_columns = [
    "year",
    "tambon_code_6",
    "db_month",
    "db_season",
    "product_group_id",
    "product_id_normalized",
    "product_breed_id"
]

keys = [c for c in key_columns if c in rice.columns]

duplicate_count = rice.duplicated(
    subset=keys,
    keep=False
).sum()

print("\n===== DUPLICATE KEY CHECK =====")
print("Duplicate rows by available keys:", duplicate_count)

# บันทึกผล
multiple.to_csv(
    REPORTS / "rice_multiple_tambons.csv",
    index=False,
    encoding="utf-8-sig"
)

details.to_csv(
    REPORTS / "rice_multiple_record_details.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved reports successfully.")
