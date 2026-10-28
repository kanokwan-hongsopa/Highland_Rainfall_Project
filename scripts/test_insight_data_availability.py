# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_data import get_halloween_payload

data = json.loads(get_halloween_payload())

print("Checking REAL_DATA keys:")
print("  centers:", len(data["centers"]))
print("  province_summaries:", len(data["province_summaries"]))
print("  stations:", len(data["stations"]))
print("  tambons:", len(data["tambons"]))

# Check provincial rice yields
for p, s in data["province_summaries"].items():
    print(f"  {p}: y22={s.get('rice_yield_2022')}, y23={s.get('rice_yield_2023')}, hii22={s.get('hii_rain_2022')}, hii23={s.get('hii_rain_2023')}, obs22={s.get('rain_obs_2022')}, exp22={s.get('rain_exp_2022')}, exp23={s.get('rain_exp_2023')}")
