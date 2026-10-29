"""
สร้างข้อมูล Dashboard จาก Balanced Panel 26 ตำบล (Baseline 27 ตัดตำบลแม่เหียะ 500109 / สถานี RPF
ที่ฝนเป็น 0 ตลอดฤดูฝน) — ช่วงฝนหลัก พ.ค.–ส.ค. และเก็บ ก.พ.–ก.ค. ไว้เป็น sensitivity

ข้อมูลจริงเท่านั้น:
- ข้าว: data/analysis_ready/rice_hrdi_tambon_panel_observed.csv (DOAE 2565/2566)
- ฝน HRDI: data/analysis_ready/hrdi_station_monthly_observed.csv (ค่าตรวจวัดจริง ไม่มีค่าประมาณ)
- ฝน HII: data/completeness/hii_all_9_provinces_24_months.csv

ผลลัพธ์: data/dashboard/dashboard_{rice_tambon,province_changes,correlations}.csv
        reports/rice_rain_leave_one_province_out.csv, reports/experiment_window_comparison.csv
"""
from pathlib import Path
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DASHBOARD = DATA / "dashboard"
REPORTS = ROOT / "reports"

EXCLUDED_TAMBONS = {500109: "แม่เหียะ (สถานี RPF ฝน 0 มม. ตลอดฤดูฝน)"}
WINDOWS = {"may_aug": [5, 6, 7, 8], "feb_jul": [2, 3, 4, 5, 6, 7]}

# 1. Rice panel (26 tambons)
rice = pd.read_csv(DATA / "analysis_ready" / "rice_hrdi_tambon_panel_observed.csv", encoding="utf-8-sig")
rice = rice[~rice["tambon_code_6"].isin(EXCLUDED_TAMBONS)].copy()
assert rice["tambon_code_6"].nunique() == 26 and (rice.groupby("tambon_code_6").size() == 2).all()

links = (
    rice[["tambon_code_6", "station_codes"]].drop_duplicates()
    .assign(station_code=lambda d: d["station_codes"].astype(str).map(lambda s: [c.strip() for c in re.split(r"[,;]", s) if c.strip()]))
    .explode("station_code")[["tambon_code_6", "station_code"]]
)

# 2. HRDI window totals: เฉลี่ยข้ามสถานีรายเดือน แล้วรวมตามช่วงเดือน (ต้องครบทุกเดือน)
hrdi = pd.read_csv(DATA / "analysis_ready" / "hrdi_station_monthly_observed.csv", encoding="utf-8-sig")
hrdi = hrdi.merge(links, on="station_code", how="inner", suffixes=("_station", ""))
assert set(links["station_code"]) <= set(hrdi["station_code"]), "missing station data"

tambon_rain = []
for name, months in WINDOWS.items():
    sub = hrdi[hrdi["month"].isin(months)]
    monthly = sub.groupby(["tambon_code_6", "year", "month"], as_index=False).agg(
        rain=("rainfall_mm", "mean"), station_count=("station_code", "nunique"))
    total = monthly.groupby(["tambon_code_6", "year"], as_index=False).agg(
        **{f"hrdi_{name}": ("rain", "sum"), f"months_{name}": ("month", "nunique"), "station_count": ("station_count", "max")})
    assert (total[f"months_{name}"] == len(months)).all(), f"incomplete HRDI months for {name}"
    tambon_rain.append(total.drop(columns=f"months_{name}").set_index(["tambon_code_6", "year"]))
hrdi_tot = tambon_rain[0].join(tambon_rain[1].drop(columns="station_count")).reset_index()

# 3. HII province window totals
hii = pd.read_csv(DATA / "completeness" / "hii_all_9_provinces_24_months.csv", encoding="utf-8-sig")
hii_tot = None
for name, months in WINDOWS.items():
    t = (hii[hii["month"].isin(months)].groupby(["province_id", "year"], as_index=False)
         .agg(**{f"hii_{name}": ("avg_rain_mm", "sum"), "n": ("month", "nunique")}))
    assert (t["n"] == len(months)).all()
    t = t.drop(columns="n")
    hii_tot = t if hii_tot is None else hii_tot.merge(t, on=["province_id", "year"])

# 4. dashboard_rice_tambon.csv (คอลัมน์เดิมของ dashboard)
panel = (
    rice[["year", "tambon_code_6", "province_code", "yield_kg_per_rai"]]
    .rename(columns={"province_code": "province_id", "yield_kg_per_rai": "rice_yield_per_harvest_area"})
    .merge(hrdi_tot, on=["tambon_code_6", "year"], how="left")
    .merge(hii_tot, on=["province_id", "year"], how="left")
)
panel = panel[["year", "tambon_code_6", "rice_yield_per_harvest_area", "province_id", "hrdi_may_aug",
               "station_count", "hii_may_aug", "hrdi_feb_jul", "hii_feb_jul"]].sort_values(["year", "tambon_code_6"])
assert panel.notna().all().all()

# ตรวจว่าวิธีคำนวณตรงกับไฟล์ 25 ตำบลเดิม (ยกเว้นตำบลที่เพิ่มใหม่)
old = pd.read_csv(DASHBOARD / "dashboard_rice_tambon.csv", encoding="utf-8-sig")
chk = old.merge(panel, on=["year", "tambon_code_6"], suffixes=("_old", ""))
if len(chk) == len(old):
    for c in ["rice_yield_per_harvest_area", "hrdi_may_aug", "hii_may_aug", "hrdi_feb_jul", "hii_feb_jul"]:
        assert (chk[c] - chk[f"{c}_old"]).abs().max() < 0.05, f"method mismatch on {c}"
panel.to_csv(DASHBOARD / "dashboard_rice_tambon.csv", index=False, encoding="utf-8-sig")

# 5. Within-tambon changes & province aggregation
wide = panel.pivot(index=["tambon_code_6", "province_id"], columns="year")
changes = pd.DataFrame(index=wide.index)
for col, out in [("rice_yield_per_harvest_area", "yield"), ("hrdi_may_aug", "hrdi"), ("hii_may_aug", "hii"),
                 ("hrdi_feb_jul", "hrdi_feb_jul"), ("hii_feb_jul", "hii_feb_jul")]:
    changes[f"{out}_change"] = wide[(col, 2023)] - wide[(col, 2022)]
changes = changes.reset_index()

prov = changes.groupby("province_id", as_index=False).agg(
    tambons=("yield_change", "size"),
    mean_yield_change=("yield_change", "mean"),
    mean_hrdi_change=("hrdi_change", "mean"),
    hii_change=("hii_change", "first"),
    mean_hrdi_feb_jul_change=("hrdi_feb_jul_change", "mean"),
    hii_feb_jul_change=("hii_feb_jul_change", "first"),
)
prov.to_csv(DASHBOARD / "dashboard_province_changes.csv", index=False, encoding="utf-8-sig")


def rho(df, x, y):
    return float(df[[x, y]].corr(method="spearman").iloc[0, 1])


def bootstrap_ci(df, x, y, reps=5000, seed=42):
    """95% percentile bootstrap CI ของ Spearman rho (สุ่มตำบลซ้ำแบบใส่คืน)"""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(reps):
        s = df.iloc[rng.integers(0, len(df), len(df))]
        if s[x].nunique() > 1 and s[y].nunique() > 1:
            vals.append(rho(s, x, y))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def corr_rows(window, hrdi_col, hii_col, prov_hrdi_col, prov_hii_col):
    lo, hi = bootstrap_ci(changes, hrdi_col, "yield_change")
    base = {"analysis_type": "exploratory", "causal_interpretation_allowed": False, "rain_window": window,
            "crop_season_verified": False, "source_units_verified": False}
    return [
        {"analysis": "HRDI_tambon", "n": len(changes), "spearman_rho": rho(changes, hrdi_col, "yield_change"),
         "ci95_low": lo, "ci95_high": hi, **base},
        {"analysis": "HRDI_province", "n": len(prov), "spearman_rho": rho(prov, prov_hrdi_col, "mean_yield_change"),
         "ci95_low": None, "ci95_high": None, **base},
        {"analysis": "HII_province", "n": len(prov), "spearman_rho": rho(prov, prov_hii_col, "mean_yield_change"),
         "ci95_low": None, "ci95_high": None, **base},
    ]


corr = pd.DataFrame(corr_rows("May-Aug", "hrdi_change", "hii_change", "mean_hrdi_change", "hii_change"))
corr.to_csv(DASHBOARD / "dashboard_correlations.csv", index=False, encoding="utf-8-sig")
corr_fj = pd.DataFrame(corr_rows("Feb-Jul", "hrdi_feb_jul_change", "hii_feb_jul_change",
                                 "mean_hrdi_feb_jul_change", "hii_feb_jul_change"))

# 6. LOPO (ช่วงหลัก พ.ค.–ส.ค.) + ช่วง ก.พ.–ก.ค. สำหรับตารางเปรียบเทียบ
def lopo(hrdi_col, prov_hrdi_col, prov_hii_col):
    rows = []
    for p in sorted(changes["province_id"].unique()):
        st, sp = changes[changes["province_id"] != p], prov[prov["province_id"] != p]
        rows.append({"scenario": f"exclude_province_{p}", "tambons": len(st), "provinces": len(sp),
                     "hrdi_tambon_rho": rho(st, hrdi_col, "yield_change"),
                     "hrdi_province_rho": rho(sp, prov_hrdi_col, "mean_yield_change"),
                     "hii_province_rho": rho(sp, prov_hii_col, "mean_yield_change"),
                     "excluded_province": p})
    return pd.DataFrame(rows)


lopo_ma = lopo("hrdi_change", "mean_hrdi_change", "hii_change")
lopo_fj = lopo("hrdi_feb_jul_change", "mean_hrdi_feb_jul_change", "hii_feb_jul_change")
lopo_ma.to_csv(REPORTS / "rice_rain_leave_one_province_out.csv", index=False, encoding="utf-8-sig")

# 7. Window comparison table (ช่วงหลัก พ.ค.–ส.ค. vs ก.พ.–ก.ค.)
def direction(s):
    return f"Decrease: {(s < 0).sum()} / Increase: {(s > 0).sum()}"


def rng(df, c):
    return f"{df[c].min():.4f} to {df[c].max():.4f}"


n_t, n_p, n_s = len(changes), len(prov), links["station_code"].nunique()
yc = changes["yield_change"]
window = pd.DataFrame([
    ["Sample Size (Tambons)", n_t, n_t, f"Same {n_t} tambons (Balanced Panel 26, excl. RPF zero-rain)"],
    ["Sample Size (Provinces)", n_p, n_p, f"Same {n_p} provinces"],
    ["HRDI Stations", n_s, n_s, f"Same {n_s} stations"],
    *[[f"{a.replace('_', ' ')} Spearman rho", round(fj, 4), round(ma, 4), f"{ma - fj:+.4f}"]
      for a, fj, ma in zip(["HRDI_Tambon", "HRDI_Province", "HII_Province"], corr_fj["spearman_rho"], corr["spearman_rho"])],
    ["HRDI Tambon rho 95% bootstrap CI", f"{corr_fj.ci95_low[0]:.2f} to {corr_fj.ci95_high[0]:.2f}",
     f"{corr.ci95_low[0]:.2f} to {corr.ci95_high[0]:.2f}", "CI crosses 0 = no reliable relationship"],
    ["HRDI Rain Direction (Decrease / Increase)", direction(changes["hrdi_feb_jul_change"]), direction(changes["hrdi_change"]), ""],
    ["HII Rain Direction (Decrease / Increase)", direction(changes["hii_feb_jul_change"]), direction(changes["hii_change"]), ""],
    ["Rice Yield Direction (Dec / Inc / Same)", *[f"Dec: {(yc < 0).sum()} / Inc: {(yc > 0).sum()} / Same: {(yc == 0).sum()}"] * 2, "Identical (same yield data)"],
    ["LOPO HRDI Tambon rho range", rng(lopo_fj, "hrdi_tambon_rho"), rng(lopo_ma, "hrdi_tambon_rho"), "Sensitivity range"],
    ["LOPO HRDI Province rho range", rng(lopo_fj, "hrdi_province_rho"), rng(lopo_ma, "hrdi_province_rho"), "Sensitivity range"],
    ["LOPO HII Province rho range", rng(lopo_fj, "hii_province_rho"), rng(lopo_ma, "hii_province_rho"), "Sensitivity range"],
], columns=["Metric", "Baseline (Feb-Jul)", "Experiment (May-Aug)", "Difference / Note"])
window.to_csv(REPORTS / "experiment_window_comparison.csv", index=False, encoding="utf-8-sig")

# 8. HRDI vs HII บนตำบลชุดเดียวกัน (Δ พ.ค.–ส.ค.) + CI ของผลต่าง + ทดสอบความไวตามผลตรวจพิกัด (src/61)
def paired_bootstrap(df, reps=5000, seed=42):
    rng = np.random.default_rng(seed)
    hr, hi = [], []
    for _ in range(reps):
        s = df.iloc[rng.integers(0, len(df), len(df))]
        if s["hrdi_change"].nunique() > 1 and s["hii_change"].nunique() > 1 and s["yield_change"].nunique() > 1:
            hr.append(rho(s, "hrdi_change", "yield_change"))
            hi.append(rho(s, "hii_change", "yield_change"))
    hr, hi = np.array(hr), np.array(hi)
    pct = lambda a: (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)))
    return pct(hr), pct(hi), pct(hr - hi)


spatial_path = DATA / "analysis_ready" / "station_tambon_spatial_check.csv"
far_tambons = set()
if spatial_path.exists():
    sp = pd.read_csv(spatial_path, encoding="utf-8-sig", dtype={"tambon_code_6": str})
    sp = sp[sp["scope"] == "panel_pair"]
    # ตัดตำบลที่ไม่มีสถานีใดอยู่ภายในหรือห่างขอบไม่เกิน 5 กม.
    ok = sp[sp["status"].isin(["inside", "near_edge"])]["tambon_code_6"].unique()
    far_tambons = set(sp["tambon_code_6"]) - set(ok)

compare_rows = []
for label, df in [("all_panel", changes),
                  ("exclude_station_far_from_tambon", changes[~changes["tambon_code_6"].astype(str).isin(far_tambons)])]:
    (hr_lo, hr_hi), (hi_lo, hi_hi), (d_lo, d_hi) = paired_bootstrap(df)
    base = {"subset": label, "n_tambons": len(df), "n_provinces": df["province_id"].nunique(),
            "rain_window": "May-Aug", "measure": "change_2023_minus_2022", "excluded_tambons": ";".join(sorted(far_tambons)) if label != "all_panel" else ""}
    compare_rows += [
        {**base, "rain_source": "HRDI", "spearman_rho": rho(df, "hrdi_change", "yield_change"), "ci95_low": hr_lo, "ci95_high": hr_hi,
         "distinct_rain_values": df["hrdi_change"].nunique()},
        {**base, "rain_source": "HII", "spearman_rho": rho(df, "hii_change", "yield_change"), "ci95_low": hi_lo, "ci95_high": hi_hi,
         "distinct_rain_values": df["hii_change"].nunique()},
        {**base, "rain_source": "HRDI_minus_HII", "spearman_rho": rho(df, "hrdi_change", "yield_change") - rho(df, "hii_change", "yield_change"),
         "ci95_low": d_lo, "ci95_high": d_hi, "distinct_rain_values": None},
    ]
compare = pd.DataFrame(compare_rows)
compare.to_csv(DASHBOARD / "dashboard_relationship_compare.csv", index=False, encoding="utf-8-sig")

print(f"Panel: {n_t} tambons, {n_p} provinces, {n_s} stations")
print(compare[["subset", "rain_source", "n_tambons", "spearman_rho", "ci95_low", "ci95_high", "distinct_rain_values"]].round(3).to_string(index=False))
print(corr[["analysis", "n", "spearman_rho", "ci95_low", "ci95_high"]].round(3).to_string(index=False))
print(prov.round(1).to_string(index=False))
print(window.to_string(index=False))
