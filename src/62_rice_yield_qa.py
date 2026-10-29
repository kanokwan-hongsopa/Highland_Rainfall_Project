"""
ตรวจคุณภาพผลผลิตข้าวนาปี DOAE รายตำบล (921 ตำบล) ก่อนนำไปสรุป — ไม่แก้ไฟล์ต้นฉบับ

กฎ (เป็นกฎตรวจจับ ไม่ใช่การยืนยันว่าผิด):
- no_harvest_area : พื้นที่เก็บเกี่ยว = 0 จึงได้ผลผลิตต่อไร่ = 0 จากการหาร 0/0 ในขั้นประมวลผล
                    หลักฐานจากต้นทาง: product_avg ของแถวข้าวนาปีว่างทุกแถว (DOAE ไม่ได้ให้ค่าผลผลิตต่อไร่)
- low_lt50        : ผลผลิตต่อไร่ > 0 แต่ < 50 กก./ไร่
- high_gt1200     : ผลผลิตต่อไร่ > 1,200 กก./ไร่

เกณฑ์ทดสอบความไว:
- S0 ตามไฟล์ที่ประมวลผล (รวมค่า 0)
- S1 (หลัก) ไม่นับแถว no_harvest_area เพราะต้นทางไม่มีค่าผลผลิตต่อไร่ ค่าที่ต้องตรวจสอบยังนับรวม
- S2 ไม่นับแถวที่ถูกตั้งข้อสงสัยทั้งหมด

ผลลัพธ์:
- data/analysis_ready/rice_yield_qa_flags.csv
- data/dashboard/dashboard_rice_sensitivity.csv
- data/dashboard/dashboard_rice_province_sensitivity.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
LOW, HIGH = 50, 1200
RICE_WET = {"011000", "11000"}  # รหัสสินค้าข้าวนาปีใน DOAE

r = pd.read_csv(DATA / "completeness" / "rice_all_921_tambons_2022_2023.csv", encoding="utf-8-sig")
r = r[r["yield_kg_per_rai"].notna()].copy()

# หลักฐานจากไฟล์ต้นทาง (อ่านอย่างเดียว)
a = pd.read_csv(DATA / "raw" / "plant01_65.csv", dtype=str)
b = pd.read_csv(DATA / "raw" / "5.-01-2566.csv", dtype=str)
a["tambon_code_6"] = a.code_province_id.str.zfill(2) + a.code_amphur_id.str.zfill(2) + a.code_tambon_id.str.zfill(2)
b["tambon_code_6"] = b.code_tambon_id.str.zfill(6)
raw = pd.concat([a.assign(year=2022), b.assign(year=2023)], ignore_index=True)
raw = raw[raw["product_id"].isin(RICE_WET)].copy()
for c in ["area_plant", "area_harvest", "product_harvest", "product_avg"]:
    raw[c] = pd.to_numeric(raw[c], errors="coerce")
raw["tambon_code_6"] = raw["tambon_code_6"].astype(int)
ev = raw.groupby(["tambon_code_6", "year"]).agg(
    source_rows=("product_id", "size"),
    source_months=("db_month", lambda s: ",".join(sorted(set(s), key=int))),
    source_area_harvest=("area_harvest", "sum"),
    source_product_harvest=("product_harvest", "sum"),
    source_product_avg_blank=("product_avg", lambda s: int(s.isna().sum())),
    source_product_avg_min=("product_avg", "min"),
    source_product_avg_max=("product_avg", "max"),
).reset_index()
r = r.merge(ev, on=["tambon_code_6", "year"], how="left")


def flag(row):
    y = row["yield_kg_per_rai"]
    if row["harvest_area_rai"] == 0 or (y == 0 and row["production_kg"] == 0):
        return "no_harvest_area"
    if 0 < y < LOW:
        return "low_lt50"
    if y > HIGH:
        return "high_gt1200"
    return ""


r["qa_flag"] = r.apply(flag, axis=1)
recalc = np.where(r["harvest_area_rai"] > 0, r["production_kg"] / r["harvest_area_rai"].where(r["harvest_area_rai"] > 0), 0.0)
r["recalc_matches"] = np.isclose(recalc, r["yield_kg_per_rai"], atol=0.01)


def evidence(row):
    f = row["qa_flag"]
    if f == "no_harvest_area":
        return (f"ต้นทาง {int(row['source_rows'])} แถว (เดือน {row['source_months']}) พื้นที่เก็บเกี่ยว = {row['source_area_harvest']:.0f} ไร่ "
                f"ผลผลิต = {row['source_product_harvest']:.0f} กก. และ product_avg ว่าง {int(row['source_product_avg_blank'])}/{int(row['source_rows'])} แถว")
    if f in ("low_lt50", "high_gt1200"):
        return (f"ผลผลิต {row['production_kg']:,.0f} กก. ÷ พื้นที่เก็บเกี่ยว {row['harvest_area_rai']:,.0f} ไร่ = {row['yield_kg_per_rai']:.2f} "
                f"(คำนวณซ้ำ{'ตรง' if row['recalc_matches'] else 'ไม่ตรง'}) • product_avg ต้นทาง {row['source_product_avg_min']:.2f}–{row['source_product_avg_max']:.2f}")
    return ""


TREAT = {
    "no_harvest_area": "ไม่มีค่าผลผลิตต่อไร่ในต้นทาง — ไม่นับในผลหลัก (S1) แต่นับใน S0",
    "low_lt50": "ต้องตรวจสอบกับ DOAE — นับในผลหลัก ไม่นับใน S2",
    "high_gt1200": "ต้องตรวจสอบกับ DOAE — นับในผลหลัก ไม่นับใน S2",
}
r["evidence"] = r.apply(evidence, axis=1)
r["treatment"] = r["qa_flag"].map(TREAT).fillna("")
flags = r[r["qa_flag"] != ""][["tambon_code_6", "tambon_name", "amphoe_name", "province_name", "year", "plant_area_rai", "harvest_area_rai",
                               "production_kg", "yield_kg_per_rai", "qa_flag", "evidence", "treatment"]].sort_values(["qa_flag", "province_name", "tambon_code_6", "year"])
flags.to_csv(DATA / "analysis_ready" / "rice_yield_qa_flags.csv", index=False, encoding="utf-8-sig")

SCEN = {"S0": set(), "S1": {"no_harvest_area"}, "S2": {"no_harvest_area", "low_lt50", "high_gt1200"}}
LABEL = {"S0": "ตามไฟล์ประมวลผล (รวมค่า 0)", "S1": "หลัก: ไม่นับแถวที่ไม่มีพื้นที่เก็บเกี่ยว", "S2": "ไม่นับค่าที่ต้องตรวจสอบทั้งหมด"}


def summarize(df):
    out = {}
    for y in (2022, 2023):
        d = df[df["year"] == y]
        out[f"n_{y}"] = len(d)
        out[f"mean_{y}"] = d["yield_kg_per_rai"].mean()
        out[f"weighted_{y}"] = d["production_kg"].sum() / d["harvest_area_rai"].sum() if d["harvest_area_rai"].sum() > 0 else np.nan
    w = df.pivot(index="tambon_code_6", columns="year", values="yield_kg_per_rai").dropna()
    dlt = w[2023] - w[2022]
    pa = df[df["tambon_code_6"].isin(w.index)]
    p22, p23 = pa[pa.year == 2022], pa[pa.year == 2023]
    out.update(n_paired=len(w), mean_delta=dlt.mean(), median_delta=dlt.median(), n_increase=int((dlt > 0).sum()),
               n_decrease=int((dlt < 0).sum()), n_same=int((dlt == 0).sum()),
               weighted_paired_2022=p22["production_kg"].sum() / p22["harvest_area_rai"].sum(),
               weighted_paired_2023=p23["production_kg"].sum() / p23["harvest_area_rai"].sum())
    out["weighted_paired_delta"] = out["weighted_paired_2023"] - out["weighted_paired_2022"]
    return out


rows, prow = [], []
for s, drop in SCEN.items():
    df = r[~r["qa_flag"].isin(drop)]
    rows.append({"scenario": s, "label": LABEL[s], "rows_excluded": int(r["qa_flag"].isin(drop).sum()), **summarize(df)})
    for p, g in df.groupby("province_name"):
        prow.append({"scenario": s, "province_name": p, **summarize(g)})
sens = pd.DataFrame(rows)
prov = pd.DataFrame(prow)
sens.round(3).to_csv(DATA / "dashboard" / "dashboard_rice_sensitivity.csv", index=False, encoding="utf-8-sig")
prov.round(3).to_csv(DATA / "dashboard" / "dashboard_rice_province_sensitivity.csv", index=False, encoding="utf-8-sig")

print("flags:", flags["qa_flag"].value_counts().to_dict(), "| by year:", flags.groupby(["qa_flag", "year"]).size().to_dict())
print("recalc mismatches among reported rows:", int((~r["recalc_matches"]).sum()))
print(sens[["scenario", "rows_excluded", "n_2022", "n_2023", "mean_2022", "mean_2023", "weighted_2022", "weighted_2023", "n_paired",
            "mean_delta", "median_delta", "weighted_paired_delta", "n_increase", "n_decrease", "n_same"]].round(1).to_string(index=False))
piv = prov.pivot(index="province_name", columns="scenario", values="weighted_paired_delta").round(1)
piv["n_paired_S1"] = prov[prov.scenario == "S1"].set_index("province_name")["n_paired"]
print(piv.sort_values("S1", ascending=False).to_string())
