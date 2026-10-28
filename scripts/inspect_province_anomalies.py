# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_data import get_halloween_payload

data = json.loads(get_halloween_payload())
provs = data["province_summaries"]

print("--- PROVINCIAL COMPARISON (2022 vs 2023) ---")
for p, s in provs.items():
    hii_diff = s["hii_rain_2023"] - s["hii_rain_2022"]
    exp_diff = (s["rain_exp_2023"] - s["rain_exp_2022"]) if s["rain_exp_2023"] and s["rain_exp_2022"] else None
    y22 = s["rice_yield_2022"]
    y23 = s["rice_yield_2023"]
    y_diff = (y23 - y22) if y23 and y22 else None
    
    anomaly_hii = (hii_diff > 0 and y_diff is not None and y_diff < 0)
    anomaly_exp = (exp_diff is not None and exp_diff > 0 and y_diff is not None and y_diff < 0)
    
    print(f"{p}:")
    print(f"  HII: 2022={s['hii_rain_2022']}, 2023={s['hii_rain_2023']} (diff={hii_diff:+.1f} mm)")
    print(f"  HRDI Exp: 2022={s['rain_exp_2022']}, 2023={s['rain_exp_2023']} (diff={exp_diff if exp_diff is not None else 0:+.1f} mm)")
    print(f"  Rice Yield: 2022={y22}, 2023={y23} (diff={y_diff if y_diff is not None else 0:+.1f} kg/rai)")
    print(f"  -> Anomaly (HII Rain Up & Yield Down): {anomaly_hii}")
    print(f"  -> Anomaly (HRDI Exp Rain Up & Yield Down): {anomaly_exp}")
