
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

df = pd.read_csv(
    PROCESSED / "rice_rain_balanced_panel.csv",
    dtype={"tambon_code_6": str},
    encoding="utf-8-sig"
)

variables = {
    "weighted_yield": "yield",
    "hrdi_clean_feb_jul_total": "hrdi",
    "hii_feb_jul_total": "hii"
}

keys = ["tambon_code_6", "year"]

assert not df.duplicated(keys).any()
assert set(df["year"]) == {2022, 2023}

# สร้างตารางตำบลเดียวกันสองปี
panel = df.pivot(
    index="tambon_code_6",
    columns="year",
    values=list(variables.keys())
)

panel.columns = [
    f"{variables[var]}_{year}"
    for var, year in panel.columns
]

panel = panel.dropna().reset_index()

assert len(panel) == 25, "Expected 25 complete tambons"

panel["province_id"] = panel["tambon_code_6"].str[:2]

# คำนวณการเปลี่ยนแปลงปี 2023 เทียบ 2022
for var in ["yield", "hrdi", "hii"]:
    panel[f"{var}_change"] = (
        panel[f"{var}_2023"] - panel[f"{var}_2022"]
    )

def direction(series):
    return series.map(
        lambda x: "increase" if x > 0
        else "decrease" if x < 0
        else "unchanged"
    )

for var in ["yield", "hrdi", "hii"]:
    panel[f"{var}_direction"] = direction(
        panel[f"{var}_change"]
    )

print("\n===== CHANGE SUMMARY =====")
print(
    panel[
        ["yield_change", "hrdi_change", "hii_change"]
    ].describe().round(3).to_string()
)

print("\n===== CHANGE DIRECTIONS =====")
for var in ["yield", "hrdi", "hii"]:
    print(f"\n{var.upper()}")
    print(
        panel[f"{var}_direction"]
        .value_counts()
        .to_string()
    )

# ตรวจทิศทางการเปลี่ยนแปลงที่ตรงกัน
for rain_var in ["hrdi", "hii"]:
    name = f"{rain_var}_same_direction"

    panel[name] = (
        (panel["yield_direction"] == panel[f"{rain_var}_direction"])
        & (panel["yield_direction"] != "unchanged")
    )

    print(f"\n===== {rain_var.upper()} VS YIELD DIRECTION =====")
    print("Same direction:", int(panel[name].sum()))
    print(
        "Different direction:",
        int(
            (
                (panel["yield_direction"] != "unchanged")
                & (panel[f"{rain_var}_direction"] != "unchanged")
                & ~panel[name]
            ).sum()
        )
    )
    print(
        "Unchanged in either variable:",
        int(
            (
                (panel["yield_direction"] == "unchanged")
                | (panel[f"{rain_var}_direction"] == "unchanged")
            ).sum()
        )
    )

print("\n===== PROVINCE CHANGE SUMMARY =====")
print(
    panel.groupby("province_id").agg(
        tambons=("tambon_code_6", "nunique"),
        median_yield_change=("yield_change", "median"),
        median_hrdi_change=("hrdi_change", "median"),
        median_hii_change=("hii_change", "median")
    ).round(3).to_string()
)

panel.to_csv(
    PROCESSED / "rice_rain_balanced_changes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved within-tambon change dataset.")
