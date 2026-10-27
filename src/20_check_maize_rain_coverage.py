
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"

crop = pd.read_csv(
    REPORTS / "crop_with_plant_names.csv",
    dtype=str,
    encoding="utf-8-sig"
)

matching = pd.read_csv(
    REPORTS / "hrdi_crop_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

rain = pd.read_csv(
    PROCESSED / "hrdi_clean_2022_2023.csv",
    dtype=str,
    encoding="utf-8-sig"
)

print("\n===== AVAILABLE COLUMNS =====")
print("MATCHING:", matching.columns.tolist())
print("RAINFALL:", rain.columns.tolist())

# คัดเฉพาะข้าวโพดเลี้ยงสัตว์
maize = crop[
    crop["product_id_normalized"] == "020030"
].copy()

for col in ["area_harvest", "product_harvest", "product_avg"]:
    maize[col] = pd.to_numeric(maize[col], errors="coerce")

maize = maize[
    (maize["area_harvest"] > 0)
    & (maize["product_harvest"] >= 0)
    & maize["product_avg"].notna()
    & (maize["product_avg"] >= 0)
]

# ตำบลที่มีผลผลิตทั้งสองปี
year_count = (
    maize[["tambon_code_6", "year"]]
    .drop_duplicates()
    .groupby("tambon_code_6")["year"]
    .nunique()
)

both_years = set(year_count[year_count == 2].index)

print("\n===== MAIZE BOTH YEARS =====")
print("ตำบลที่มีผลผลิตใช้ได้ทั้งสองปี:", len(both_years))

# ตรวจสถานีที่จับคู่กับตำบลเหล่านี้
matched = matching[
    matching["tambon_code_6"].isin(both_years)
].copy()

print("\n===== MATCHED HRDI AREAS =====")
print("จำนวนรายการจับคู่:", len(matched))
print("จำนวนตำบล:", matched["tambon_code_6"].nunique())

# บันทึกไว้สำหรับตรวจคีย์สถานีและข้อมูลฝน
matched.to_csv(
    REPORTS / "maize_hrdi_matched_areas.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nบันทึกไฟล์ maize_hrdi_matched_areas.csv แล้ว")
print("ขั้นนี้ยังไม่สรุปความครบถ้วนของฝน")
