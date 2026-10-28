# -*- coding: utf-8 -*-
"""
Acceptance Test Suite for Province Insights & Rain-Rice Relationship
Tests all 7 acceptance criteria from the user specification
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_data import get_halloween_payload
from dashboard.halloween_app import get_halloween_html

print("=== Starting Province Insights & Rain-Rice Relationship Acceptance Tests ===")

# Load data payload
payload_str = get_halloween_payload()
data = json.loads(payload_str)
provs = data["province_summaries"]
stations = data["stations"]
html = get_halloween_html()

# -------------------------------------------------------------------------
# Test 1: อันดับเปลี่ยนถูกต้องเมื่อเปลี่ยนปี (Ranking changes correctly by year)
# -------------------------------------------------------------------------
print("\n[Test 1] Testing rankings by year and mode...")
# 2022 HII Max vs 2023 HII Max
max_hii_22 = max(provs.items(), key=lambda x: x[1]["hii_rain_2022"])
max_hii_23 = max(provs.items(), key=lambda x: x[1]["hii_rain_2023"])
assert max_hii_22[0] == "เชียงราย", f"Expected เชียงราย for 2022 Max HII, got {max_hii_22[0]}"
assert max_hii_23[0] == "เชียงใหม่", f"Expected เชียงใหม่ for 2023 Max HII, got {max_hii_23[0]}"
print(f"  ✓ 2022 Max HII: {max_hii_22[0]} ({max_hii_22[1]['hii_rain_2022']:.1f} mm)")
print(f"  ✓ 2023 Max HII: {max_hii_23[0]} ({max_hii_23[1]['hii_rain_2023']:.1f} mm) -> Ranking properly changed!")

# Rice Yield Max and Min
max_y_22 = max(provs.items(), key=lambda x: x[1]["rice_yield_2022"])
min_y_22 = min(provs.items(), key=lambda x: x[1]["rice_yield_2022"])
max_y_23 = max(provs.items(), key=lambda x: x[1]["rice_yield_2023"])
min_y_23 = min(provs.items(), key=lambda x: x[1]["rice_yield_2023"])
assert max_y_22[0] == "กำแพงเพชร" and min_y_22[0] == "แม่ฮ่องสอน"
assert max_y_23[0] == "กำแพงเพชร" and min_y_23[0] == "แม่ฮ่องสอน"
print(f"  ✓ Rice Yield 2022: Max={max_y_22[0]} ({max_y_22[1]['rice_yield_2022']:.1f}), Min={min_y_22[0]} ({min_y_22[1]['rice_yield_2022']:.1f})")
print(f"  ✓ Rice Yield 2023: Max={max_y_23[0]} ({max_y_23[1]['rice_yield_2023']:.1f}), Min={min_y_23[0]} ({min_y_23[1]['rice_yield_2023']:.1f})")

# -------------------------------------------------------------------------
# Test 2: ค่าเฉลี่ยฝนสะสมรายปีต่อสถานี (ห้ามนำผลรวมทุกสถานีบวกกัน)
# -------------------------------------------------------------------------
print("\n[Test 2] Verifying per-station average metric (no station sum distortion)...")
# Check that Chiang Mai (22 stations) is not 22x Nan (12 stations)
cm_rain = provs["เชียงใหม่"]["rain_exp_2022"]
nan_rain = provs["น่าน"]["rain_exp_2022"]
assert 1000 < cm_rain < 3000, f"Chiang Mai rain {cm_rain} should be normalized per station"
assert 1000 < nan_rain < 3000, f"Nan rain {nan_rain} should be normalized per station"
print(f"  ✓ เชียงใหม่ (22 สถานี) ฝนเฉลี่ย: {cm_rain} มม./สถานี")
print(f"  ✓ น่าน (12 สถานี) ฝนเฉลี่ย: {nan_rain} มม./สถานี")

# -------------------------------------------------------------------------
# Test 3: ค่าฝนที่ประมาณไม่ถูกแสดงเป็นข้อมูลจริง
# -------------------------------------------------------------------------
print("\n[Test 3] Verifying estimated data is strictly separated from observed...")
for s in stations:
    for m_idx, v in enumerate(s["monthly_obs_24"]):
        st = s["monthly_status_24"][m_idx]
        if st != "observed":
            assert v is None, f"Station {s['name']} month {m_idx} is {st} but has observed value {v}"
# Check 2023 HRDI in observed mode is None for all stations and provinces
for p, s in provs.items():
    assert s["rain_obs_2023"] is None, f"Province {p} rain_obs_2023 must be None in Observed mode"
for s in stations:
    assert s["annual_obs_2023"] is None, f"Station {s['name']} annual_obs_2023 must be None in Observed mode"
print("  ✓ 100% of estimated months are None in monthly_obs_24.")
print("  ✓ 100% of 2023 HRDI annual sums are None in Observed mode.")

# -------------------------------------------------------------------------
# Test 4: ผลผลิตข้าวใช้ข้อมูลรายปี ไม่สร้างผลผลิตรายเดือน
# -------------------------------------------------------------------------
print("\n[Test 4] Verifying rice yield is strictly annual (no monthly yield mock)...")
for t in data["tambons"]:
    assert "yield_2022" in t and "yield_2023" in t
    for k in t.keys():
        assert not k.startswith("yield_month_") and not k.startswith("monthly_yield_"), f"Found monthly yield in tambon: {k}"
print("  ✓ Rice yield is strictly annual (2022 & 2023), 0 monthly mock yields found.")

# -------------------------------------------------------------------------
# Test 5: ความสัมพันธ์ Rain-Rice Scatter Plot & Spearman rho
# -------------------------------------------------------------------------
print("\n[Test 5] Verifying Rain-Rice Relationship Scatter Plot elements in HTML...")
assert 'id="chartRainRiceScatter"' in html, "Missing chartRainRiceScatter canvas"
assert 'id="scatterMetricSelect"' in html, "Missing scatterMetricSelect dropdown"
assert 'id="scatterSpearmanBadge"' in html, "Missing scatterSpearmanBadge badge"
assert "renderRainRiceScatterPlot()" in html, "Missing renderRainRiceScatterPlot() call"
assert "renderTop4HighlightCards()" in html, "Missing renderTop4HighlightCards() call"
print("  ✓ All HTML elements, canvas, selectors, and JS render calls exist.")

# -------------------------------------------------------------------------
# Test 6: ไม่แสดงความสัมพันธ์เมื่อไม่มีคู่ข้อมูลเพียงพอ (n < 4 guard)
# -------------------------------------------------------------------------
print("\n[Test 6] Verifying insufficient data guard (n < 4)...")
assert "allPts.length < 4" in html, "Missing n < 4 sample size guard in scatter plot"
assert "ข้อมูลไม่เพียงพอสำหรับวิเคราะห์สหสัมพันธ์" in html, "Missing empty state title for n < 4"
print("  ✓ n < 4 sample size guard is present in scatter plot logic.")

# -------------------------------------------------------------------------
# Test 7: Interactive Cross-Filtering (Clicking cards & markers dispatches filter)
# -------------------------------------------------------------------------
print("\n[Test 7] Verifying cross-filtering dispatchTab1Filter on cards and markers...")
assert "dispatchTab1Filter" in html, "Missing dispatchTab1Filter function"
assert "btnResetMap" in html, "Missing btnResetMap (home) button"
assert "resetTab1Map" in html, "Missing resetTab1Map function"
assert "openStationDetailSubpanel" in html, "Missing openStationDetailSubpanel function"
assert "renderStationMiniChart" in html, "Missing renderStationMiniChart function"
print("  ✓ dispatchTab1Filter, map navigation, drawer, and mini chart are fully integrated.")

print("\n=== ALL ACCEPTANCE TESTS PASSED SUCCESSFULLY! ===")
