
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

PROVINCES = [
    "เชียงใหม่", "เชียงราย", "น่าน",
    "ตาก", "กำแพงเพชร", "พิษณุโลก",
    "เพชรบูรณ์", "กาญจนบุรี", "แม่ฮ่องสอน"
]

# รหัสจังหวัดตามระบบกรมการปกครอง
PROVINCE_CODES = {
    "เชียงใหม่": 50,
    "เชียงราย": 57,
    "น่าน": 55,
    "ตาก": 63,
    "กำแพงเพชร": 62,
    "พิษณุโลก": 65,
    "เพชรบูรณ์": 67,
    "กาญจนบุรี": 71,
    "แม่ฮ่องสอน": 58
}

FILES = {
    "HRDI": "HRDI_meteo.csv",
    "HII": "spatial-rain-hii.csv",
    "CROP_2022": "plant01_65.csv",
    "CROP_2023": "5.-01-2566.csv"
}

def read_file(filename):
    return pd.read_csv(
        RAW / filename,
        encoding="utf-8-sig",
        low_memory=False
    )

def normalize_year(series):
    years = pd.to_numeric(series, errors="coerce")
    return years.where(years < 2400, years - 543)

results = []
scoped = {}

for name, filename in FILES.items():
    df = read_file(filename)
    df.columns = df.columns.str.strip()

    year_col = "YEAR" if name in ("HRDI", "HII") else "db_year"
    df["_year"] = normalize_year(df[year_col])

    if name == "HRDI":
        province = df["PROVINCE"].astype("string").str.strip()
        province_mask = province.isin(PROVINCES)
    elif name == "HII":
        province = df["PROV_T"].astype("string").str.strip()
        province_mask = province.isin(PROVINCES)
    else:
        codes = pd.to_numeric(
            df["code_province_id"], errors="coerce"
        )
        province_mask = codes.isin(PROVINCE_CODES.values())

    year_mask = df["_year"].isin([2022, 2023])
    selected = df.loc[province_mask & year_mask].copy()
    scoped[name] = selected

    results.append({
        "dataset": name,
        "total_rows": len(df),
        "rows_in_scope": len(selected),
        "rows_2022": int((selected["_year"] == 2022).sum()),
        "rows_2023": int((selected["_year"] == 2023).sum()),
        "out_of_scope": len(df) - len(selected),
        "missing_cells_in_scope": int(
            selected.drop(columns=["_year"]).isna().sum().sum()
        )
    })

    print(f"\n===== {name} =====")
    print(f"ข้อมูลทั้งหมด: {len(df):,}")
    print(f"ข้อมูลในขอบเขต: {len(selected):,}")
    print(f"ปี 2022: {(selected['_year'] == 2022).sum():,}")
    print(f"ปี 2023: {(selected['_year'] == 2023).sum():,}")

summary = pd.DataFrame(results)
summary.to_csv(
    REPORTS / "scope_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

# ตรวจข้อมูลฝน HII ว่าครบจังหวัด-ปี-เดือนหรือไม่
hii = scoped["HII"].copy()
hii["MONTH"] = pd.to_numeric(hii["MONTH"], errors="coerce")

hii_keys = hii.groupby(
    ["PROV_T", "_year", "MONTH"], dropna=False
).size().reset_index(name="row_count")

hii_keys.to_csv(
    REPORTS / "hii_month_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

# ตรวจ HRDI ตามสถานี-ปี-เดือน
hrdi = scoped["HRDI"].copy()
hrdi["MONTH"] = pd.to_numeric(hrdi["MONTH"], errors="coerce")

hrdi_keys = hrdi.groupby(
    ["CODE_REF", "_year", "MONTH"], dropna=False
).size().reset_index(name="row_count")

hrdi_keys.to_csv(
    REPORTS / "hrdi_station_month_coverage.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nตรวจสอบขอบเขตข้อมูลเสร็จแล้ว")
print("รายงานอยู่ใน reports/")
