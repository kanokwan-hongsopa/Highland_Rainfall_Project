# -*- coding: utf-8 -*-
"""
Dual Mode Verification Script:
Verify Observed Only Mode vs Exploratory Mode in dashboard data & logic
"""

import json
from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from dashboard.halloween_data import get_halloween_payload

data = json.loads(get_halloween_payload())

print("=== Starting Dual-Mode Verification Test ===")

stations = data["stations"]
provs = data["province_summaries"]

# 1. Verify 50 stations count
assert len(stations) == 50, f"Expected 50 stations, got {len(stations)}"

# 2. Rule 7 & Incomplete stations check in Observed Mode
incomplete_22_codes = ["NAN", "NPAK", "RPF", "MJR"]
for s in stations:
    code = s["code_ref"]
    # 2022 check
    if code in incomplete_22_codes:
        assert s["annual_obs_2022"] is None, f"Station {code} has incomplete 2022 but annual_obs_2022 is not None: {s['annual_obs_2022']}"
        print(f"[PASS] Incomplete station {code} in 2022 has annual_obs_2022 = None (observed {s['observed_count_2022']}/12 m)")
    else:
        assert s["annual_obs_2022"] is not None, f"Station {code} is complete in 2022 but annual_obs_2022 is None"

    # 2023 check (Rule 7: 0 stations have 12 months observed in 2023, so all must be None!)
    assert s["annual_obs_2023"] is None, f"Station {code} has annual_obs_2023 = {s['annual_obs_2023']} (should be None in Observed mode!)"

print("[PASS] All 50 stations have annual_obs_2023 = None in Observed Mode (Strict Rule 7 Enforced).")

# 3. Exploratory Mode check
for s in stations:
    code = s["code_ref"]
    assert s["annual_exp_2022"] is not None and s["annual_exp_2022"] > 0, f"Station {code} missing annual_exp_2022"
    assert s["annual_exp_2023"] is not None and s["annual_exp_2023"] > 0, f"Station {code} missing annual_exp_2023"
    assert s["annual_exp_all"] is not None and s["annual_exp_all"] > 0, f"Station {code} missing annual_exp_all"
    assert len(s["monthly_exp_2022"]) == 12, f"Station {code} monthly_exp_2022 len != 12"
    assert len(s["monthly_exp_2023"]) == 12, f"Station {code} monthly_exp_2023 len != 12"

print("[PASS] All 50 stations have complete 12-month exploratory series for 2022 & 2023.")

# 4. Province Summaries check
for p_name, p_sum in provs.items():
    # Observed: 8 provinces have complete stations in 2022; พิษณุโลก has only NPAK (7 months) so it is correctly None!
    if p_name == "พิษณุโลก":
        assert p_sum["rain_obs_2022"] is None, "พิษณุโลก should have rain_obs_2022 = None because its station NPAK has only 7 months in 2022!"
        print("[PASS] พิษณุโลก correctly has rain_obs_2022 = None in Observed Mode (NPAK incomplete in 2022).")
    else:
        assert p_sum["rain_obs_2022"] is not None, f"Province {p_name} missing rain_obs_2022"

    assert p_sum["rain_obs_2023"] is None, f"Province {p_name} rain_obs_2023 should be None"
    # Exploratory
    assert p_sum["rain_exp_2022"] is not None and p_sum["rain_exp_2022"] > 0, f"Province {p_name} missing rain_exp_2022"
    assert p_sum["rain_exp_2023"] is not None and p_sum["rain_exp_2023"] > 0, f"Province {p_name} missing rain_exp_2023"
    assert p_sum["rain_exp_all"] is not None and p_sum["rain_exp_all"] > 0, f"Province {p_name} missing rain_exp_all"

print("[PASS] All 9 provinces have correct Observed & Exploratory metrics.")

# 5. Check no missing months replaced by zero in monthly_obs_24
for s in stations:
    for m_idx, v in enumerate(s["monthly_obs_24"]):
        status = s["monthly_status_24"][m_idx]
        if status != "observed":
            assert v is None, f"Station {s['name']} month {m_idx} status is {status} but value is {v} (not None!)"

print("[PASS] Missing/estimated months are strictly None (never zero) in monthly_obs_24.")

print("\n=== ALL DUAL-MODE VERIFICATION TESTS PASSED SUCCESSFULLY! ===")
