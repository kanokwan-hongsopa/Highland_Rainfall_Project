
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

changes = pd.read_csv(
    PROCESSED / "rice_rain_balanced_changes.csv",
    dtype={"tambon_code_6": str, "province_id": str},
    encoding="utf-8-sig"
)

rice = pd.read_csv(
    PROCESSED / "rice_tambon_year_scenarios.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

def rho(df, x, y):
    valid = df[[x, y]].dropna()
    if len(valid) < 3:
        return float("nan")
    if valid[x].nunique() < 2 or valid[y].nunique() < 2:
        return float("nan")
    return valid[x].corr(valid[y], method="spearman")

def summarize(df, label):
    province = df.groupby(
        "province_id", as_index=False
    ).agg(
        mean_yield_change=("yield_change", "mean"),
        mean_hrdi_change=("hrdi_change", "mean"),
        hii_change=("hii_change", "first")
    )

    return {
        "scenario": label,
        "tambons": len(df),
        "provinces": len(province),
        "hrdi_tambon_rho": rho(
            df, "hrdi_change", "yield_change"
        ),
        "hrdi_province_rho": rho(
            province, "mean_hrdi_change", "mean_yield_change"
        ),
        "hii_province_rho": rho(
            province, "hii_change", "mean_yield_change"
        )
    }

# 1. ตัดจังหวัดออกทีละจังหวัด
lopo = []

for excluded in sorted(changes["province_id"].unique()):
    subset = changes[
        changes["province_id"] != excluded
    ].copy()

    result = summarize(
        subset, f"exclude_province_{excluded}"
    )
    result["excluded_province"] = excluded
    lopo.append(result)

lopo = pd.DataFrame(lopo)

print("\n===== LEAVE-ONE-PROVINCE-OUT =====")
print(lopo.round(4).to_string(index=False))

# 2. ตรวจความไวต่อแถวผลผลิตที่มี flag
alternate = rice[
    rice["scenario"] == "exclude_area_flag"
][["year", "tambon_code_6", "weighted_yield"]].copy()

alternate["year"] = pd.to_numeric(alternate["year"])

# สร้างผลผลิตสองปีในสถานการณ์ทางเลือก
pivot = alternate.pivot(
    index="tambon_code_6",
    columns="year",
    values="weighted_yield"
)

pivot = pivot.dropna(subset=[2022, 2023])
pivot["yield_change_alternate"] = pivot[2023] - pivot[2022]

alt = changes.merge(
    pivot[["yield_change_alternate"]],
    left_on="tambon_code_6",
    right_index=True,
    how="inner",
    validate="one_to_one"
)

alt["yield_change"] = alt["yield_change_alternate"]

# เปรียบเทียบข้อมูลหลักบนตำบลชุดเดียวกับทางเลือก
same_codes = set(alt["tambon_code_6"])

main_matched = changes[
    changes["tambon_code_6"].isin(same_codes)
].copy()

sensitivity = pd.DataFrame([
    summarize(main_matched, "main_same_tambons"),
    summarize(alt, "exclude_area_flag")
])

print("\n===== YIELD FLAG SENSITIVITY =====")
print(sensitivity.round(4).to_string(index=False))

lopo.to_csv(
    REPORTS / "rice_rain_leave_one_province_out.csv",
    index=False,
    encoding="utf-8-sig"
)

sensitivity.to_csv(
    REPORTS / "rice_rain_yield_flag_sensitivity.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved correlation sensitivity reports.")
