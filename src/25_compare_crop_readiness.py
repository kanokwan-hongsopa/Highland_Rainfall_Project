
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# อ่านข้อมูลพืชและข้อมูลสถานีที่จับคู่พื้นที่แล้ว
crop = pd.read_csv(
    REPORTS / "crop_with_plant_names.csv",
    dtype=str,
    encoding="utf-8-sig"
)

stations = pd.read_csv(
    REPORTS / "hrdi_crop_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

# พืชที่ต้องการเปรียบเทียบ
plants = {
    "011000": "ข้าวนาปี",
    "020030": "ข้าวโพดเลี้ยงสัตว์",
    "013000": "ข้าวไร่"
}

# เลือกเฉพาะข้อมูลที่จับคู่พื้นที่สำเร็จ
stations = stations[
    stations["tambon_code_6"].notna()
].copy()

# ตรวจผลผลิตที่สามารถคำนวณได้
crop["yield_value"] = pd.to_numeric(
    crop["product_avg"], errors="coerce"
)

crop["harvest_area"] = pd.to_numeric(
    crop["area_harvest"], errors="coerce"
)

crop["valid_yield"] = (
    crop["yield_value"].notna()
    & (crop["yield_value"] > 0)
    & (crop["harvest_area"] > 0)
)

results = []
matched_details = []

for code, name in plants.items():

    data = crop[
        (crop["product_id_normalized"] == code)
        & crop["year"].isin(["2022", "2023"])
        & crop["valid_yield"]
    ].copy()

    # หาตำบลที่มีผลผลิตทั้งสองปี
    tambon_years = data.groupby(
        "tambon_code_6"
    )["year"].nunique()

    both_years = set(
        tambon_years[tambon_years == 2].index
    )

    # หาสถานีที่ตรงกับตำบลเหล่านั้น
    matched = stations[
        stations["tambon_code_6"].isin(both_years)
    ].copy()

    matched["plant_code"] = code
    matched["plant_name"] = name

    matched_details.append(matched)

    results.append({
        "plant_code": code,
        "plant_name": name,
        "valid_rows": len(data),
        "tambons_2022": data[
            data["year"] == "2022"
        ]["tambon_code_6"].nunique(),
        "tambons_2023": data[
            data["year"] == "2023"
        ]["tambon_code_6"].nunique(),
        "tambons_both_years": len(both_years),
        "matched_tambons": matched[
            "tambon_code_6"
        ].nunique(),
        "matched_stations": matched[
            "CODE_REF"
        ].nunique()
    })

summary = pd.DataFrame(results)

print("\n===== CROP READINESS COMPARISON =====")
print(summary.to_string(index=False))

# บันทึกผล
summary.to_csv(
    REPORTS / "crop_readiness_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)

if matched_details:
    pd.concat(
        matched_details,
        ignore_index=True
    ).to_csv(
        REPORTS / "crop_readiness_matched_stations.csv",
        index=False,
        encoding="utf-8-sig"
    )

print("\nSaved comparison reports.")
