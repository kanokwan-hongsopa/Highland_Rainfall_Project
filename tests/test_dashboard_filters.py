# -*- coding: utf-8 -*-
"""
Filter combinations & edge-case stress test for Halloween Dashboard
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dashboard.halloween_data import get_halloween_payload
from dashboard.halloween_app import get_halloween_html

def test_all_province_filter_options():
    payload = json.loads(get_halloween_payload())
    html = get_halloween_html()
    
    # 9 provinces
    expected_provinces = [
        "เชียงใหม่", "เชียงราย", "น่าน", "ตาก", "กำแพงเพชร",
        "พิษณุโลก", "เพชรบูรณ์", "กาญจนบุรี", "แม่ฮ่องสอน"
    ]
    for p in expected_provinces:
        assert p in payload["centers"]
        assert p in payload["province_summaries"]
        assert f'value="{p}"' in html

def test_missing_data_tambons_in_payload():
    payload = json.loads(get_halloween_payload())
    tambons = payload["tambons"]
    
    # Check that missing data rows are present with proper badges
    missing_tambons = [t for t in tambons if t["coverage_badge"] == "missing"]
    assert len(missing_tambons) == 52, f"Expected 52 missing tambons, got {len(missing_tambons)}"
    for mt in missing_tambons:
        assert mt["yield_2022"] is None
        assert mt["yield_2023"] is None
        assert mt["coverage_status"] == "ไม่มีข้อมูลรายงาน"

    # Check observed both years
    obs_tambons = [t for t in tambons if t["coverage_badge"] == "observed_both"]
    assert len(obs_tambons) == 826, f"Expected 826 observed both years, got {len(obs_tambons)}"
    for ot in obs_tambons:
        assert ot["yield_2022"] is not None
        assert ot["yield_2023"] is not None

def test_station_data_completeness():
    payload = json.loads(get_halloween_payload())
    stations = payload["stations"]
    assert len(stations) == 50
    
    # Ensure every station has a status label
    for s in stations:
        assert "data_status_label" in s
        assert "ตรวจวัดจริง" in s["data_status_label"]
        assert len(s["monthly_obs_24"]) == 24
        assert len(s["monthly_demo_24"]) == 24
        assert len(s["monthly_status_24"]) == 24

def test_hii_province_24_months():
    payload = json.loads(get_halloween_payload())
    hii = payload["hii_prov_24"]
    assert len(hii) == 9
    for p, series in hii.items():
        assert len(series) == 24
        for val in series:
            assert isinstance(val, (int, float))

if __name__ == "__main__":
    test_all_province_filter_options()
    test_missing_data_tambons_in_payload()
    test_station_data_completeness()
    test_hii_province_24_months()
    print("[PASS] All filter and missing-data stress tests passed successfully!")
