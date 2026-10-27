
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

rice = pd.read_csv(
    REPORTS / "rice_quality_validation.csv",
    dtype={"tambon_code_6": str, "year": str},
    encoding="utf-8-sig"
)

for col in ["area_plant", "area_harvest", "product_harvest"]:
    rice[col] = pd.to_numeric(rice[col], errors="coerce")

# แปลงธงจาก CSV เป็น Boolean อย่างชัดเจน
rice["harvest_exceeds_plant"] = (
    rice["harvest_exceeds_plant"]
    .astype(str).str.lower().eq("true")
)

# ไม่แก้ข้อมูลต้นฉบับ
# สร้างสองสถานการณ์เพื่อดูผลกระทบของรายการที่ต้องตรวจ
scenarios = {
    "all_valid_records": rice.copy(),
    "exclude_area_flag": rice[
        ~rice["harvest_exceeds_plant"]
    ].copy()
}

outputs = []

for scenario_name, data in scenarios.items():
    grouped = data.groupby(
        ["year", "tambon_code_6"], as_index=False
    ).agg(
        record_count=("year", "size"),
        total_plant_area=("area_plant", "sum"),
        total_harvest_area=("area_harvest", "sum"),
        total_production=("product_harvest", "sum")
    )

    grouped["weighted_yield"] = np.where(
        grouped["total_harvest_area"] > 0,
        grouped["total_production"]
        / grouped["total_harvest_area"],
        np.nan
    )

    grouped["scenario"] = scenario_name
    outputs.append(grouped)

result = pd.concat(outputs, ignore_index=True)

# เปรียบเทียบผลผลิตเฉลี่ยของแต่ละสถานการณ์
comparison = result.pivot(
    index=["year", "tambon_code_6"],
    columns="scenario",
    values="weighted_yield"
).reset_index()

comparison["yield_difference"] = (
    comparison["all_valid_records"]
    - comparison["exclude_area_flag"]
)

print("\n===== AGGREGATION SUMMARY =====")
print(
    result.groupby(["scenario", "year"]).agg(
        tambons=("tambon_code_6", "nunique"),
        source_rows=("record_count", "sum"),
        total_harvest_area=("total_harvest_area", "sum"),
        total_production=("total_production", "sum")
    ).to_string()
)

print("\n===== SCENARIO DIFFERENCES =====")
changed = comparison[
    comparison["yield_difference"].isna()
    | (comparison["yield_difference"].abs() > 0.000001)
]

if changed.empty:
    print("No differences found.")
else:
    print(changed.to_string(index=False))

result.to_csv(
    PROCESSED / "rice_tambon_year_scenarios.csv",
    index=False,
    encoding="utf-8-sig"
)

comparison.to_csv(
    REPORTS / "rice_aggregation_sensitivity.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved aggregation and sensitivity reports.")
