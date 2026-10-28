# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_data import get_halloween_payload

data = json.loads(get_halloween_payload())
provs = data["province_summaries"]

print("--- 2022 HRDI Observed per-station rain ranking ---")
r_obs_22 = [(p, s["rain_obs_2022"], s["station_count"]) for p, s in provs.items() if s["rain_obs_2022"] is not None]
r_obs_22.sort(key=lambda x: x[1], reverse=True)
for rank, (p, r, cnt) in enumerate(r_obs_22, 1):
    print(f"  #{rank}: {p} - {r:.1f} mm/station ({cnt} stations)")

print("\n--- 2022 HII Provincial rain ranking ---")
h_22 = [(p, s["hii_rain_2022"]) for p, s in provs.items()]
h_22.sort(key=lambda x: x[1], reverse=True)
for rank, (p, r) in enumerate(h_22, 1):
    print(f"  #{rank}: {p} - {r:.1f} mm")

print("\n--- 2022 Rice Yield ranking ---")
y_22 = [(p, s["rice_yield_2022"], s["tambon_count"]) for p, s in provs.items() if s["rice_yield_2022"] is not None]
y_22.sort(key=lambda x: x[1], reverse=True)
for rank, (p, y, cnt) in enumerate(y_22, 1):
    print(f"  #{rank}: {p} - {y:.1f} kg/rai ({cnt} tambons)")

print("\n--- 2023 Exploratory HRDI ranking ---")
r_exp_23 = [(p, s["rain_exp_2023"], s["station_count"]) for p, s in provs.items() if s["rain_exp_2023"] is not None]
r_exp_23.sort(key=lambda x: x[1], reverse=True)
for rank, (p, r, cnt) in enumerate(r_exp_23, 1):
    print(f"  #{rank}: {p} - {r:.1f} mm/station ({cnt} stations)")

print("\n--- 2023 Rice Yield ranking ---")
y_23 = [(p, s["rice_yield_2023"], s["tambon_count"]) for p, s in provs.items() if s["rice_yield_2023"] is not None]
y_23.sort(key=lambda x: x[1], reverse=True)
for rank, (p, y, cnt) in enumerate(y_23, 1):
    print(f"  #{rank}: {p} - {y:.1f} kg/rai ({cnt} tambons)")
