
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

df = pd.read_csv(
    PROCESSED / "rice_rain_balanced_changes.csv",
    dtype={"tambon_code_6": str, "province_id": str},
    encoding="utf-8-sig"
)

def spearman_safe(data, x, y):
    valid = data[[x, y]].dropna()

    if len(valid) < 3:
        return float("nan")

    if (
        valid[x].nunique() < 2
        or valid[y].nunique() < 2
    ):
        return float("nan")

    return valid[x].corr(valid[y], method="spearman")

print("\n===== HRDI TAMBON-LEVEL ANALYSIS =====")

hrdi_rho = spearman_safe(
    df, "hrdi_change", "yield_change"
)

print("Tambons:", len(df))
print("Spearman rho:", round(hrdi_rho, 4))

# รวมผลผลิตเป็นระดับจังหวัด
# ใช้ค่าเฉลี่ยแบบไม่ถ่วงน้ำหนักของตำบลในจังหวัด
province = df.groupby(
    "province_id",
    as_index=False
).agg(
    tambons=("tambon_code_6", "nunique"),
    mean_yield_change=("yield_change", "mean"),
    mean_hrdi_change=("hrdi_change", "mean"),
    hii_change=("hii_change", "first")
)

# ตรวจว่าค่า HII เท่ากันภายในจังหวัด
assert (
    df.groupby("province_id")["hii_change"]
    .nunique() == 1
).all()

print("\n===== PROVINCE-LEVEL DATA =====")
print(province.round(3).to_string(index=False))

print("\n===== PROVINCE-LEVEL CORRELATIONS =====")

hrdi_province_rho = spearman_safe(
    province, "mean_hrdi_change", "mean_yield_change"
)

hii_province_rho = spearman_safe(
    province, "hii_change", "mean_yield_change"
)

print("Provinces:", len(province))
print("HRDI Spearman rho:", round(hrdi_province_rho, 4))
print("HII Spearman rho:", round(hii_province_rho, 4))

results = pd.DataFrame([
    {
        "analysis": "HRDI_tambon",
        "n": len(df),
        "spearman_rho": hrdi_rho
    },
    {
        "analysis": "HRDI_province",
        "n": len(province),
        "spearman_rho": hrdi_province_rho
    },
    {
        "analysis": "HII_province",
        "n": len(province),
        "spearman_rho": hii_province_rho
    }
])

results.to_csv(
    REPORTS / "rice_rain_exploratory_correlations.csv",
    index=False,
    encoding="utf-8-sig"
)

province.to_csv(
    PROCESSED / "rice_rain_province_changes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved exploratory correlation results.")
