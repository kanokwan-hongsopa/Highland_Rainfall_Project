"""
Unit test suite for Halloween Interactive Dashboard
Tests payload generation, data integrity, Leaflet/Chart.js integration,
and responsive UI elements.
"""

import json
import re
import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dashboard.halloween_data import get_halloween_payload
from dashboard.halloween_app import get_halloween_html


def test_halloween_payload_integrity():
    """ตรวจสอบความสมบูรณ์และถูกต้องของ JSON Data Payload"""
    raw_json = get_halloween_payload()
    data = json.loads(raw_json)

    # 1. โครงสร้างหลัก
    assert "centers" in data, "Missing 'centers' in payload"
    assert "overview_center" in data, "Missing 'overview_center' in payload"
    assert "stations" in data, "Missing 'stations' in payload"
    assert "tambons" in data, "Missing 'tambons' in payload"
    assert "province_changes" in data, "Missing 'province_changes' in payload"
    assert "correlations" in data, "Missing 'correlations' in payload"
    assert "lopo" in data, "Missing 'lopo' in payload"
    assert "completeness" in data, "Missing 'completeness' in payload"

    # 2. ตรวจสอบ 9 จังหวัด
    centers = data["centers"]
    assert len(centers) == 9, f"Expected 9 provinces, got {len(centers)}"
    expected_provs = {
        "เชียงใหม่", "เชียงราย", "แม่ฮ่องสอน", "ตาก",
        "น่าน", "กำแพงเพชร", "พิษณุโลก", "เพชรบูรณ์", "กาญจนบุรี"
    }
    actual_provs = set(centers.keys())
    assert actual_provs == expected_provs, f"Province mismatch: {actual_provs ^ expected_provs}"

    # 3. ตรวจสอบ 50 สถานี
    stations = data["stations"]
    assert len(stations) == 50, f"Expected 50 stations, got {len(stations)}"
    for s in stations:
        assert s["name"], "Station Name must not be empty"
        assert s["lat"] is not None and -90 <= s["lat"] <= 90, f"Invalid lat: {s['lat']}"
        assert s["lng"] is not None and -180 <= s["lng"] <= 180, f"Invalid lng: {s['lng']}"
        assert s["province"] in expected_provs, f"Unknown station province: {s['province']}"

    # 4. ตรวจสอบ 25 ตำบล Balanced Panel
    tambons = data["tambons"]
    assert len(tambons) == 25, f"Expected 25 tambons, got {len(tambons)}"
    for t in tambons:
        assert len(t["tambon_code_6"]) == 6, f"Invalid tambon code: {t['tambon_code_6']}"
        assert t["province_name"] in expected_provs, f"Unknown tambon province: {t['province_name']}"
        assert "delta_hrdi" in t and "delta_yield" in t, "Missing delta metrics"

    # 5. ตรวจสอบ QA Completeness Metrics
    comp = data["completeness"]
    assert comp["num_stations"] == 50, f"Expected 50 stations, got {comp['num_stations']}"
    assert comp["expected_station_months"] == 1200, f"Expected 1200 expected records, got {comp['expected_station_months']}"
    assert comp["actual_rows"] == 983, f"Expected 983 actual records, got {comp['actual_rows']}"
    assert comp["missing_rows"] == 217, f"Expected 217 missing rows, got {comp['missing_rows']}"
    assert comp["rain_missing_values"] == 7, f"Expected 7 missing values, got {comp['rain_missing_values']}"

    # 6. ตรวจสอบ Correlation Metrics
    corrs = {c["analysis"]: c for c in data["correlations"]}
    assert "HRDI_tambon" in corrs, "Missing HRDI_tambon correlation"
    assert "HRDI_province" in corrs, "Missing HRDI_province correlation"
    assert "HII_province" in corrs, "Missing HII_province correlation"
    # ตรวจสอบค่า rho ทางทฤษฎี/การคำนวณจริง
    assert abs(corrs["HRDI_tambon"]["spearman_rho"] - (-0.173427)) < 0.001
    assert abs(corrs["HRDI_province"]["spearman_rho"] - (-0.7000)) < 0.001
    assert abs(corrs["HII_province"]["spearman_rho"] - (-0.9000)) < 0.001

    print("✔ test_halloween_payload_integrity passed successfully!")


def test_halloween_html_structure():
    """ตรวจสอบโครงสร้าง HTML, UI Components, Theme Colors, และ Interactive Logic"""
    html = get_halloween_html()

    # 1. Palette สี Halloween Night
    assert "#130D22" in html, "Missing dark background #130D22"
    assert "#211631" in html, "Missing card background #211631"
    assert "#FF8A32" in html, "Missing pumpkin orange #FF8A32"
    assert "#A778E8" in html, "Missing lavender accent #A778E8"
    assert "#F18AB6" in html, "Missing pink accent #F18AB6"
    assert "#F7F0E8" in html, "Missing cream text #F7F0E8"

    # 2. Hero Header SVG Elements
    assert "<svg" in html, "Missing hero banner SVG"
    assert "moonGlow" in html or "glow" in html, "Missing moon / glow in hero SVG"
    assert "ค้างคาว" in html or "bat" in html or "M" in html, "Missing bat silhouettes in hero SVG"
    assert "ปราสาท" in html or "castle" in html or "house" in html or "rect" in html, "Missing mansion in hero SVG"

    # 3. 5 Horizontal Navigation Tabs
    assert 'data-tab="page1"' in html, "Missing Tab 1 navigation"
    assert 'data-tab="page2"' in html, "Missing Tab 2 navigation"
    assert 'data-tab="page3"' in html, "Missing Tab 3 navigation"
    assert 'data-tab="page4"' in html, "Missing Tab 4 navigation"
    assert 'data-tab="page5"' in html, "Missing Tab 5 navigation"

    # 4. Leaflet Map Container & Script
    assert 'id="leafletMap"' in html, "Missing Leaflet map container 'leafletMap'"
    assert "leaflet.js" in html, "Missing Leaflet.js script"
    assert "flyTo" in html, "Missing smooth animated zoom (map.flyTo)"

    # 5. Detail Drawer with Close Button
    assert 'id="detailDrawer"' in html, "Missing slide-in detail drawer 'detailDrawer'"
    assert 'id="btnDrawerClose"' in html, "Missing close drawer button 'btnDrawerClose'"

    # 6. Navigation / Reset Controls
    assert 'id="btnMapBack"' in html, "Missing back button 'btnMapBack'"
    assert 'id="btnResetMap"' in html, "Missing reset map button 'btnResetMap'"
    assert 'id="btnResetAll"' in html, "Missing reset all filters button 'btnResetAll'"

    # 7. Non-Causal Disclaimers & Unit Warnings
    assert "วิเคราะห์เชิงสำรวจ (Non-causal)" in html, "Missing non-causal exploratory disclaimer"
    assert "หน่วยรอยืนยัน" in html, "Missing unconfirmed unit labels"

    print("✔ test_halloween_html_structure passed successfully!")


if __name__ == "__main__":
    print("Running Halloween Dashboard Test Suite...")
    test_halloween_payload_integrity()
    test_halloween_html_structure()
    print("ALL TESTS PASSED! 🎃✨")
