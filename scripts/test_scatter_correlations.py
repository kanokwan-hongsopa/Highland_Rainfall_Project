# -*- coding: utf-8 -*-
import json
import sys
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_data import get_halloween_payload

data = json.loads(get_halloween_payload())
provs = data["province_summaries"]

# Calculate Spearman rho in Python to cross-check
def spearman(x, y):
    n = len(x)
    if n < 3: return 0, 1.0
    def rank(arr):
        s = sorted(range(n), key=lambda i: arr[i])
        r = [0]*n
        i = 0
        while i < n:
            j = i
            while j < n-1 and arr[s[j+1]] == arr[s[j]]:
                j += 1
            avg = 1 + (i + j) / 2.0
            for k in range(i, j+1):
                r[s[k]] = avg
            i = j + 1
        return r
    rx = rank(x)
    ry = rank(y)
    mx = sum(rx)/n
    my = sum(ry)/n
    num = sum((rx[i]-mx)*(ry[i]-my) for i in range(n))
    den = math.sqrt(sum((rx[i]-mx)**2 for i in range(n)) * sum((ry[i]-my)**2 for i in range(n)))
    rho = num/den if den != 0 else 0
    df = n - 2
    if abs(rho) >= 1.0:
        p = 0.0
    else:
        t = rho * math.sqrt(df / (1 - rho**2))
        # approx p-value
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(t) / math.sqrt(2))))
    return rho, p

# 1. HII vs Rice Yield (18 points: 9 provs x 2 years)
x_hii = []
y_hii = []
pts_hii = []
for p, s in provs.items():
    if s["rice_yield_2022"]:
        x_hii.append(s["hii_rain_2022"])
        y_hii.append(s["rice_yield_2022"])
        pts_hii.append((p, 2022, s["hii_rain_2022"], s["rice_yield_2022"]))
    if s["rice_yield_2023"]:
        x_hii.append(s["hii_rain_2023"])
        y_hii.append(s["rice_yield_2023"])
        pts_hii.append((p, 2023, s["hii_rain_2023"], s["rice_yield_2023"]))

rho_hii, p_hii = spearman(x_hii, y_hii)
print(f"HII Rain vs Rice Yield (n={len(x_hii)}): rho={rho_hii:.4f}, p={p_hii:.4f}")

# 2. HRDI Exploratory vs Rice Yield (18 points)
x_exp = []
y_exp = []
for p, s in provs.items():
    if s["rain_exp_2022"] and s["rice_yield_2022"]:
        x_exp.append(s["rain_exp_2022"])
        y_exp.append(s["rice_yield_2022"])
    if s["rain_exp_2023"] and s["rice_yield_2023"]:
        x_exp.append(s["rain_exp_2023"])
        y_exp.append(s["rice_yield_2023"])

rho_exp, p_exp = spearman(x_exp, y_exp)
print(f"HRDI Exp Rain vs Rice Yield (n={len(x_exp)}): rho={rho_exp:.4f}, p={p_exp:.4f}")
