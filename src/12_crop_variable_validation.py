
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

files = {
    "CROP_2022": "crop_2022_normalized.csv",
    "CROP_2023": "crop_2023_normalized.csv"
}

results = []

for name, filename in files.items():
    df = pd.read_csv(
        REPORTS / filename,
        dtype=str,
        encoding="utf-8-sig"
    )

    for col in [
        "area_harvest",
        "product_harvest",
        "product_avg"
    ]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    area = df["area_harvest"]
    production = df["product_harvest"]
    avg = df["product_avg"]

    calculated = production.div(
        area.where(area > 0)
    )

    comparable = (
        (area > 0)
        & production.notna()
        & avg.notna()
    )

    # ตรวจค่าที่ต่างจากการคำนวณเกิน 1%
    difference = (
        calculated - avg
    ).abs()

    tolerance = np.maximum(
        avg.abs() * 0.01, 0.01
    )

    inconsistent = (
        comparable
        & (difference > tolerance)
    )

    results.append({
        "dataset": name,
        "rows": len(df),
        "area_missing": int(area.isna().sum()),
        "area_zero": int((area == 0).sum()),
        "area_negative": int((area < 0).sum()),
        "production_missing": int(
            production.isna().sum()
        ),
        "production_negative": int(
            (production < 0).sum()
        ),
        "avg_missing": int(avg.isna().sum()),
        "avg_negative": int((avg < 0).sum()),
        "comparable_rows": int(
            comparable.sum()
        ),
        "inconsistent_avg_rows": int(
            inconsistent.sum()
        )
    })

    review = df.loc[
        inconsistent,
        [
            "year", "tambon_code_6",
            "product_id", "area_harvest",
            "product_harvest", "product_avg"
        ]
    ].copy()

    review["calculated_avg"] = (
        calculated.loc[inconsistent]
    )

    review.to_csv(
        REPORTS / f"{name.lower()}_yield_review.csv",
        index=False,
        encoding="utf-8-sig"
    )

summary = pd.DataFrame(results)

print("\n===== CROP VARIABLE VALIDATION =====")
print(summary.to_string(index=False))

summary.to_csv(
    REPORTS / "crop_variable_validation.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกรายงานใน reports/ เรียบร้อยแล้ว")
