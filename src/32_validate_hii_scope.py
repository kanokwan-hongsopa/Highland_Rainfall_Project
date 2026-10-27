
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

df = pd.read_csv(
    RAW / "spatial-rain-hii.csv",
    encoding="utf-8-sig"
)

provinces = {
    50: "เชียงใหม่",
    57: "เชียงราย",
    55: "น่าน",
    63: "ตาก",
    62: "กำแพงเพชร",
    65: "พิษณุโลก",
    67: "เพชรบูรณ์",
    71: "กาญจนบุรี",
    58: "แม่ฮ่องสอน"
}

scope = df[
    df["YEAR"].isin([2022, 2023])
    & df["PROV_ID"].isin(provinces)
].copy()

print("\n===== HII SCOPE SUMMARY =====")
print("Rows:", len(scope))
print("Provinces:", scope["PROV_ID"].nunique())
print("Years:", sorted(scope["YEAR"].unique()))

# ตรวจรหัสจังหวัดกับชื่อจังหวัด
scope["expected_name"] = scope["PROV_ID"].map(provinces)
scope["name_mismatch"] = (
    scope["PROV_T"].str.strip()
    != scope["expected_name"]
)

# ตรวจคีย์จังหวัด-ปี-เดือนซ้ำ
keys = ["PROV_ID", "YEAR", "MONTH"]
duplicates = scope[
    scope.duplicated(subset=keys, keep=False)
]

# ตรวจความครบถ้วนเทียบกับ 9 x 2 x 12
expected = pd.MultiIndex.from_product(
    [provinces.keys(), [2022, 2023], range(1, 13)],
    names=keys
).to_frame(index=False)

coverage = expected.merge(
    scope[keys].drop_duplicates().assign(present=True),
    on=keys,
    how="left"
)

missing = coverage[
    coverage["present"].isna()
].copy()

# ตรวจค่าฝน
rain_cols = ["MinRain", "MaxRain", "AvgRain"]

for col in rain_cols:
    scope[col] = pd.to_numeric(
        scope[col], errors="coerce"
    )

scope["negative_rain"] = (
    scope[rain_cols] < 0
).any(axis=1)

scope["rain_order_issue"] = (
    (scope["MinRain"] > scope["AvgRain"])
    | (scope["AvgRain"] > scope["MaxRain"])
)

scope["missing_rain"] = scope[rain_cols].isna().any(axis=1)

print("\n===== VALIDATION RESULTS =====")
print("Expected province-months:", len(expected))
print("Missing province-months:", len(missing))
print("Duplicate-key rows:", len(duplicates))
print("Province name mismatches:", int(scope["name_mismatch"].sum()))
print("Negative rain rows:", int(scope["negative_rain"].sum()))
print("Rain order issues:", int(scope["rain_order_issue"].sum()))
print("Missing rain rows:", int(scope["missing_rain"].sum()))

print("\n===== MONTHLY COVERAGE =====")
print(
    scope.groupby(["YEAR", "MONTH"])["PROV_ID"]
    .nunique()
    .unstack(0, fill_value=0)
    .to_string()
)

if not missing.empty:
    print("\n===== MISSING KEYS =====")
    print(missing[keys].to_string(index=False))

if not duplicates.empty:
    print("\n===== DUPLICATE KEYS =====")
    print(duplicates.to_string(index=False))

scope.to_csv(
    REPORTS / "hii_scope_validation.csv",
    index=False,
    encoding="utf-8-sig"
)

missing.to_csv(
    REPORTS / "hii_missing_province_months.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved HII validation reports.")
