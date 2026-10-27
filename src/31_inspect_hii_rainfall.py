
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

path = RAW / "spatial-rain-hii.csv"

# รองรับ encoding ที่พบบ่อยในไฟล์ CSV ภาษาไทย
df = None
for encoding in ["utf-8-sig", "utf-8", "cp874"]:
    try:
        df = pd.read_csv(path, encoding=encoding)
        print("Encoding:", encoding)
        break
    except UnicodeDecodeError:
        continue

if df is None:
    raise ValueError("Cannot decode HII CSV")

print("\n===== HII COLUMNS =====")
for col in df.columns:
    print(f"- {col}: {df[col].dtype}")

print("\n===== FIRST 10 ROWS =====")
print(df.head(10).to_string(index=False))

print("\n===== DATA SUMMARY =====")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Exact duplicate rows:", df.duplicated().sum())

print("\n===== MISSING VALUES =====")
print(df.isna().sum().to_string())

print("\n===== COLUMN VALUE EXAMPLES =====")
for col in df.columns:
    print(f"\n{col}")
    print(
        df[col].dropna()
        .astype(str)
        .unique()[:12]
    )

# บันทึกเฉพาะรายงานตรวจสอบ
summary = pd.DataFrame({
    "column": df.columns,
    "dtype": [str(df[c].dtype) for c in df.columns],
    "missing_count": [int(df[c].isna().sum()) for c in df.columns],
    "unique_count": [int(df[c].nunique()) for c in df.columns]
})

summary.to_csv(
    REPORTS / "hii_column_audit.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved HII column audit.")
