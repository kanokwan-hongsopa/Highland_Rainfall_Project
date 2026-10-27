
import json
import re
from pathlib import Path
from difflib import get_close_matches

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
REF = ROOT / "data" / "reference"

with open(REF / "geo.json", encoding="utf-8-sig") as f:
    geo = json.load(f)

def clean_name(value):
    if pd.isna(value):
        return ""
    value = re.sub(r"\s+", "", str(value))
    return re.sub(
        r"^(จังหวัด|อำเภอ|ตำบล|จ\.|อ\.|ต\.)",
        "", value
    )

records = []
for p in geo:
    for d in p.get("districts", []):
        for t in d.get("subdistricts", []):
            records.append({
                "province": p["name_th"],
                "district": d["name_th"],
                "subdistrict": t["name_th"],
                "tambon_code_6": str(t["code"]).zfill(6)
            })

ref = pd.DataFrame(records)

hrdi = pd.read_csv(
    REPORTS / "hrdi_geo_matching.csv",
    dtype=str,
    encoding="utf-8-sig"
)

unmatched = hrdi[
    hrdi["tambon_code_6"].isna()
].copy()

results = []

for _, row in unmatched.iterrows():
    province = clean_name(row["province"])
    district = clean_name(row["district"])
    subdistrict = clean_name(row["subdistrict"])

    same_province = ref[
        ref["province"].map(clean_name) == province
    ].copy()

    district_options = same_province[
        "district"
    ].drop_duplicates().tolist()

    district_matches = get_close_matches(
        district,
        [clean_name(x) for x in district_options],
        n=5,
        cutoff=0.4
    )

    for _, candidate in same_province.iterrows():
        cand_district = clean_name(candidate["district"])
        cand_tambon = clean_name(candidate["subdistrict"])

        district_similar = (
            cand_district == district
            or cand_district in district_matches
            or district in cand_district
        )

        tambon_similar = (
            cand_tambon == subdistrict
            or subdistrict in cand_tambon
            or cand_tambon in subdistrict
        )

        if district_similar and tambon_similar:
            results.append({
                "station": row["STA_TH"],
                "hrdi_province": row["province"],
                "hrdi_district": row["district"],
                "hrdi_subdistrict": row["subdistrict"],
                "geo_district": candidate["district"],
                "geo_subdistrict": candidate["subdistrict"],
                "candidate_code": candidate["tambon_code_6"],
                "review_status": "NEEDS_MANUAL_REVIEW"
            })

result = pd.DataFrame(results)

output = REPORTS / "unmatched_area_candidates.csv"
result.to_csv(
    output,
    index=False,
    encoding="utf-8-sig"
)

print("===== UNMATCHED AREA REVIEW =====")
print("สถานีที่จับคู่ไม่ได้:", len(unmatched))
print("รายการที่อาจตรงกัน:", len(result))

if not result.empty:
    print(result.to_string(index=False))
else:
    print("ไม่พบชื่อใกล้เคียงตามเงื่อนไข")

print("\nบันทึกผล:", output)
