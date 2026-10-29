# -*- coding: utf-8 -*-
"""
ทดสอบกฎความถูกต้องทางวิชาการของ dashboard (รอบตรวจทาน 2026-10-29)
- เทียบฝนระหว่างปีเฉพาะ ม.ค.–ส.ค. ที่มีค่าต้นทางทั้งสองปี
- Spatial join สถานี–ตำบล
- HRDI vs HII บนตำบลชุดเดียวกัน (คำนวณซ้ำจากไฟล์ dashboard)
- สถานะหน่วยวัดจาก metadata
"""
from pathlib import Path
import json
import sys

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from dashboard.halloween_data import get_halloween_payload  # noqa: E402

DATA = BASE / "data"
payload = json.loads(get_halloween_payload())


def test_observed_window_is_jan_aug_paired():
    w = payload["obs_compare_window"]
    assert w["months"] == 8 and w["label"] == "ม.ค.–ส.ค."
    complete = [s for s in payload["stations"] if s["obs_compare_complete"]]
    assert w["stations"] == len(complete) == payload["overall_kpis"]["hrdi_obs_station_count"]
    po = payload["monthly_obs_paired_overall"]
    assert all(v is None for v in po["2022"][8:] + po["2023"][8:]), "ก.ย.–ธ.ค. ต้องไม่ถูกนำมาเทียบในโหมดข้อมูลต้นทาง"
    assert all(n > 0 for n in po["n"][:8]) and all(n == 0 for n in po["n"][8:])
    k = payload["overall_kpis"]
    assert abs(k["hrdi_obs_rain_2023"] - sum(s["annual_obs_2023"] for s in complete) / len(complete)) < 0.06
    print("  ✓ observed comparison = Jan–Aug on", len(complete), "complete stations")


def test_hii_same_window():
    for p, s in payload["province_summaries"].items():
        assert s["hii_ja_2022"] is not None and s["hii_ja_2023"] is not None, p
        assert s["hii_ja_2022"] <= s["hii_rain_2022"] + 0.1, p
    print("  ✓ HII Jan–Aug totals present for all 9 provinces")


def test_data_source_disclosed():
    k = payload["overall_kpis"]
    assert k["rows_total_2022_2023"] == 983
    assert k["rows_openweathermap"] == 883
    assert all(s["data_source_label"] for s in payload["stations"])
    print("  ✓ OpenWeatherMap share disclosed:", k["rows_openweathermap"], "/", k["rows_total_2022_2023"])


def test_spatial_check():
    sp = pd.read_csv(DATA / "analysis_ready" / "station_tambon_spatial_check.csv", encoding="utf-8-sig", dtype={"tambon_code_6": str})
    pairs = sp[sp["scope"] == "panel_pair"]
    assert len(pairs) == 29 and pairs["tambon_code_6"].nunique() == 26
    assert set(pairs["status"]) <= {"inside", "near_edge", "outside_far"}
    assert (pairs.loc[pairs["status"] == "inside", "distance_to_boundary_km"] == 0).all()
    assert (pairs.loc[pairs["status"] == "near_edge", "distance_to_boundary_km"].between(0, 5)).all()
    assert (pairs.loc[pairs["status"] == "outside_far", "distance_to_boundary_km"] > 5).all()
    counts = pairs["status"].value_counts().to_dict()
    assert counts == {"inside": 24, "near_edge": 2, "outside_far": 3}, counts
    assert len(sp[sp["scope"] == "all_stations"]) == 50
    print("  ✓ spatial check:", counts)


def test_relationship_compare_matches_recompute():
    comp = pd.read_csv(DATA / "dashboard" / "dashboard_relationship_compare.csv", encoding="utf-8-sig")
    rt = pd.read_csv(DATA / "dashboard" / "dashboard_rice_tambon.csv", encoding="utf-8-sig")
    w = rt.pivot(index="tambon_code_6", columns="year")
    ch = pd.DataFrame({
        "dy": w[("rice_yield_per_harvest_area", 2023)] - w[("rice_yield_per_harvest_area", 2022)],
        "dh": w[("hrdi_may_aug", 2023)] - w[("hrdi_may_aug", 2022)],
        "di": w[("hii_may_aug", 2023)] - w[("hii_may_aug", 2022)],
    })
    get = lambda sub, src: comp[(comp.subset == sub) & (comp.rain_source == src)].iloc[0]
    hr, hi = get("all_panel", "HRDI"), get("all_panel", "HII")
    assert hr.n_tambons == hi.n_tambons == 26
    assert abs(hr.spearman_rho - ch.dh.corr(ch.dy, method="spearman")) < 1e-9
    assert abs(hi.spearman_rho - ch.di.corr(ch.dy, method="spearman")) < 1e-9
    assert hi.distinct_rain_values == 6, "HII มี 1 ค่าต่อจังหวัด"
    for _, r in comp.iterrows():
        assert r.ci95_low <= r.spearman_rho <= r.ci95_high, r.to_dict()
    sens = get("exclude_station_far_from_tambon", "HRDI")
    assert sens.n_tambons == 23
    print(f"  ✓ HRDI ρ={hr.spearman_rho:+.3f} HII ρ={hi.spearman_rho:+.3f} (recomputed, same 26 tambons)")


def test_relationship_compare_12m_exploratory():
    comp = pd.read_csv(DATA / "dashboard" / "dashboard_relationship_compare.csv", encoding="utf-8-sig")
    r12 = pd.read_csv(DATA / "dashboard" / "dashboard_tambon_rain_12m.csv", encoding="utf-8-sig")
    rt = pd.read_csv(DATA / "dashboard" / "dashboard_rice_tambon.csv", encoding="utf-8-sig")
    w = rt.pivot(index="tambon_code_6", columns="year", values="rice_yield_per_harvest_area")
    df = r12.set_index("tambon_code_6").join((w[2023] - w[2022]).rename("dy"))
    main = comp[comp.rain_window == "May-Aug"]
    exp = comp[comp.rain_window == "Jan-Dec"]
    assert len(main) == len(exp) == 6
    assert not main.includes_estimates.astype(bool).any() and exp.includes_estimates.astype(bool).all()
    get = lambda src: exp[(exp.subset == "all_panel") & (exp.rain_source == src)].iloc[0]
    assert abs(get("HRDI").spearman_rho - df.delta_hrdi_12m.corr(df.dy, method="spearman")) < 1e-9
    assert abs(get("HII").spearman_rho - df.delta_hii_12m.corr(df.dy, method="spearman")) < 1e-9
    assert 0 < get("HRDI").hrdi_estimated_share < 0.5
    assert {t["tambon_code_6"] for t in payload["balanced_tambons"] if t["delta_hrdi_12m"] is not None} == set(r12.tambon_code_6.astype(str))
    print(f"  ✓ 12-month (exploratory) HRDI ρ={get('HRDI').spearman_rho:+.3f} HII ρ={get('HII').spearman_rho:+.3f}")


def test_rice_yield_qa_flags_and_sensitivity():
    fl = pd.read_csv(DATA / "analysis_ready" / "rice_yield_qa_flags.csv", encoding="utf-8-sig")
    assert fl["qa_flag"].value_counts().to_dict() == {"no_harvest_area": 27, "low_lt50": 14, "high_gt1200": 5}
    z = fl[fl.qa_flag == "no_harvest_area"]
    assert (z.harvest_area_rai == 0).all() and (z.production_kg == 0).all()
    assert z.evidence.str.contains("product_avg ว่าง").all(), "ต้องมีหลักฐานจากต้นทางว่า product_avg ว่าง"
    sens = pd.read_csv(DATA / "dashboard" / "dashboard_rice_sensitivity.csv", encoding="utf-8-sig").set_index("scenario")
    assert sens.loc["S0", "rows_excluded"] == 0 and sens.loc["S1", "rows_excluded"] == 27 and sens.loc["S2", "rows_excluded"] == 46
    # ค่าถ่วงน้ำหนักพื้นที่เก็บเกี่ยวไม่ถูกกระทบจากแถวที่พื้นที่เก็บเกี่ยว = 0
    assert abs(sens.loc["S0", "weighted_2022"] - sens.loc["S1", "weighted_2022"]) < 1e-6
    # ชุด 26 ตำบลของผลหลักไม่มีค่าที่ถูกตั้งข้อสงสัย
    rt = pd.read_csv(DATA / "dashboard" / "dashboard_rice_tambon.csv", encoding="utf-8-sig")
    assert rt.rice_yield_per_harvest_area.between(50, 1200).all()
    tb = {(t["tambon_code_6"]) for t in payload["tambons"] if t["qa_flag_2022"] or t["qa_flag_2023"]}
    assert len(tb) == fl.tambon_code_6.nunique()
    print("  ✓ rice QA: 27 no-harvest-area, 14 low, 5 high; panel 26 unaffected")


def test_rain_station_qa():
    q = payload["rain_station_qa"]
    assert [f["name"] for f in q["flagged"]] == ["สถานีตรวจวัดสภาพอากาศอุทยานหลวงราชพฤกษ์"]
    assert q["before"]["stations"] == 34 and q["after"]["stations"] == 33
    k = payload["overall_kpis"]
    assert k["hrdi_obs_station_count"] == 33 and abs(k["hrdi_obs_rain_2022"] - q["after"]["rain_2022"]) < 0.06
    assert payload["panel_rain_source"]["by_source"].get("HRDI", 0) < 0.05 * payload["panel_rain_source"]["rows"]
    print("  ✓ rain QA: RPF excluded, 34 -> 33 stations;", q["before"]["rain_2022"], "->", q["after"]["rain_2022"])


def test_cluster_ci_present():
    comp = pd.read_csv(DATA / "dashboard" / "dashboard_relationship_compare.csv", encoding="utf-8-sig")
    assert comp[["ci95_cluster_low", "ci95_cluster_high"]].notna().all().all()
    assert (comp.ci95_cluster_low < comp.ci95_cluster_high).all()
    assert (comp.tambons_sharing_station_set == 0).all()
    print("  ✓ cluster (province) bootstrap CI present for all rows")


def test_unit_status():
    u = payload["unit_verification"]
    assert u["HII"]["status"] == "confirmed"
    assert u["DOAE"]["status"] == "partial"
    assert u["HRDI"]["status"] == "partial" and "openweathermap.org" in u["HRDI"]["evidence"]
    print("  ✓ unit status: HII confirmed, DOAE partial, HRDI partial (OpenWeatherMap docs)")


if __name__ == "__main__":
    for fn in [test_observed_window_is_jan_aug_paired, test_hii_same_window, test_data_source_disclosed,
               test_spatial_check, test_relationship_compare_matches_recompute, test_relationship_compare_12m_exploratory, test_rice_yield_qa_flags_and_sensitivity, test_rain_station_qa,
               test_cluster_ci_present, test_unit_status]:
        fn()
    print("ALL ACADEMIC REVIEW TESTS PASSED")
