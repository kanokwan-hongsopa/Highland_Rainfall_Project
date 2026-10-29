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


def test_unit_status():
    u = payload["unit_verification"]
    assert u["HII"]["status"] == "confirmed"
    assert u["DOAE"]["status"] == "partial"
    assert u["HRDI"]["status"] == "unconfirmed"
    print("  ✓ unit status: HII confirmed, DOAE partial, HRDI unconfirmed")


if __name__ == "__main__":
    for fn in [test_observed_window_is_jan_aug_paired, test_hii_same_window, test_data_source_disclosed,
               test_spatial_check, test_relationship_compare_matches_recompute, test_unit_status]:
        fn()
    print("ALL ACADEMIC REVIEW TESTS PASSED")
