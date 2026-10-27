
from pathlib import Path
import pandas as pd

# กำหนดตำแหน่งโฟลเดอร์ของโปรเจกต์
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

files = {
    "HRDI": "HRDI_meteo.csv",
    "HII": "spatial-rain-hii.csv",
    "CROP_2022": "plant01_65.csv",
    "CROP_2023": "5.-01-2566.csv",
}

def read_csv_file(path):
    # ลองอ่านไฟล์ด้วย encoding ที่ใช้บ่อย
    for encoding in ["utf-8-sig", "cp874", "tis-620"]:
        try:
            return pd.read_csv(
                path,
                encoding=encoding,
                dtype=str,
                low_memory=False
            ), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode file: {path.name}")


summary = []
missing_rows = []
column_rows = []

for name, filename in files.items():
    path = RAW / filename

    if not path.exists():
        print(f"ไม่พบไฟล์: {path}")
        continue

    df, encoding = read_csv_file(path)
    df.columns = df.columns.str.strip()

    rows, cols = df.shape
    duplicates = int(df.duplicated().sum())

    summary.append({
        "dataset": name,
        "filename": filename,
        "rows": rows,
        "columns": cols,
        "encoding": encoding,
        "duplicate_rows": duplicates,
        "total_missing_cells": int(df.isna().sum().sum())
    })

    for col in df.columns:
        missing_count = int(df[col].isna().sum())

        column_rows.append({
            "dataset": name,
            "column": col,
            "non_null": int(df[col].notna().sum()),
            "missing": missing_count,
            "missing_percent": round(
                missing_count / rows * 100, 2
            ) if rows else 0,
            "unique_values": int(df[col].nunique(dropna=True))
        })

        if missing_count > 0:
            missing_rows.append({
                "dataset": name,
                "column": col,
                "missing_count": missing_count
            })

    print(f"\n===== {name} =====")
    print(f"ไฟล์: {filename}")
    print(f"จำนวนแถว: {rows:,}")
    print(f"จำนวนคอลัมน์: {cols}")
    print(f"ข้อมูลซ้ำทั้งแถว: {duplicates:,}")
    print(f"คอลัมน์: {', '.join(df.columns)}")

pd.DataFrame(summary).to_csv(
    REPORTS / "data_audit_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame(column_rows).to_csv(
    REPORTS / "column_profile.csv",
    index=False,
    encoding="utf-8-sig"
)

pd.DataFrame(
    missing_rows,
    columns=["dataset", "column", "missing_count"]
).to_csv(
    REPORTS / "missing_values.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nตรวจสอบข้อมูลเสร็จแล้ว")
print("บันทึกรายงานไว้ในโฟลเดอร์ reports/")
