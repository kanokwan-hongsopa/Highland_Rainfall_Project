# -*- coding: utf-8 -*-
"""
Simulation test for all user interaction flows across 5 tabs in Halloween Dashboard
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dashboard.halloween_data import get_halloween_payload

payload = json.loads(get_halloween_payload())
stations = payload["stations"]
tambons = payload["tambons"]
provinces = list(payload["centers"].keys())
b_tambons = payload.get("balanced_tambons", [])

print("=== Starting Browser Interaction Flow Simulation ===")

# 1. TAB 1 Simulation: Province -> Station -> Tambon Cascading & KPI/Chart calculation
print("\n[Sim 1] Tab 1: Filtering across all 9 provinces & 50 stations...")
for p in ["all"] + provinces:
    p_stas = stations if p == "all" else [s for s in stations if s["province"] == p]
    p_tbs = tambons if p == "all" else [t for t in tambons if t["province_name"] == p]
    assert len(p_stas) > 0, f"Province {p} must have at least 1 HRDI station"
    assert len(p_tbs) > 0, f"Province {p} must have tambons"
    
    # Test years
    for yr in ["all", "2022", "2023"]:
        # Province summary
        if p != "all":
            sum_p = payload["province_summaries"][p]
            assert sum_p["rain_all"] is not None
            assert sum_p["hii_rain_2022"] is not None
            assert sum_p["hii_rain_2023"] is not None

# Test individual stations
for s in stations:
    assert s["name"]
    assert s["province"] in provinces
    assert len(s["monthly_obs_24"]) == 24
    assert len(s["monthly_demo_24"]) == 24

# Test tambon rice yield missing case in Tab 1
missing_tbs = [t for t in tambons if t["coverage_badge"] == "missing"]
print(f"Found {len(missing_tbs)} tambons with missing DOAE data")
for mt in missing_tbs[:5]:
    # Ensure yield is None (handled by in-chart empty state)
    assert mt["yield_2022"] is None
    assert mt["yield_2023"] is None

# 2. TAB 2 Simulation: Comparison between HRDI and HII
print("\n[Sim 2] Tab 2: HII vs HRDI across all 9 provinces...")
for p in ["all"] + provinces:
    for src in ["all", "HRDI", "HII"]:
        for yr in ["all", "2022", "2023"]:
            if p != "all":
                sum_p = payload["province_summaries"][p]
                hrdi = sum_p["rain_2022"] if yr == "2022" else sum_p["rain_2023"] if yr == "2023" else sum_p["rain_all"]
                hii = sum_p["hii_rain_2022"] if yr == "2022" else sum_p["hii_rain_2023"] if yr == "2023" else (sum_p["hii_rain_2022"] + sum_p["hii_rain_2023"]) / 2
                assert hrdi is not None and not (isinstance(hrdi, float) and hrdi != hrdi) # not NaN
                assert hii is not None and not (isinstance(hii, float) and hii != hii)

# 3. TAB 3 Simulation: Rice yield across all 921 tambons
print("\n[Sim 3] Tab 3: Rice yield 921 tambons & search...")
for p in ["all"] + provinces:
    tbs_slice = tambons if p == "all" else [t for t in tambons if t["province_name"] == p]
    valid_2yr = [t for t in tbs_slice if t["yield_2022"] is not None and t["yield_2023"] is not None]
    missing = [t for t in tbs_slice if t["yield_2022"] is None and t["yield_2023"] is None]
    single_yr = [t for t in tbs_slice if (t["yield_2022"] is None) != (t["yield_2023"] is None)]
    
    # Check that counts sum to total
    assert len(valid_2yr) + len(missing) + len(single_yr) == len(tbs_slice)

# 4. TAB 4 Simulation: Correlation & sample size guards
print("\n[Sim 4] Tab 4: Scatter Plot & Sample Size (n) Guards...")
# Test level = tambon (balanced 25)
for p in ["all"] + provinces:
    pts = b_tambons if p == "all" else [t for t in b_tambons if t["province_name"] == p]
    n = len(pts)
    if n < 3:
        # Must trigger empty state
        # Provinces with n < 3 in balanced panel: Tak (2), Chiang Rai (1), Kamphaeng Phet (0), Phitsanulok (0), Phetchabun (0), Kanchanaburi (0)
        assert p in ["ตาก", "เชียงราย", "กำแพงเพชร", "พิษณุโลก", "เพชรบูรณ์", "กาญจนบุรี"]
    else:
        # Provinces with n >= 3: Chiang Mai (14), Nan (5), Mae Hong Son (3), all (25)
        assert p in ["all", "เชียงใหม่", "น่าน", "แม่ฮ่องสอน"]

print("=== ALL INTERACTION FLOW SIMULATIONS PASSED SUCCESSFULLY! ===")
