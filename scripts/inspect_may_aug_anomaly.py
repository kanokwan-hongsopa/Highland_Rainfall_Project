# -*- coding: utf-8 -*-
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
exp_df = pd.read_csv(BASE_DIR / "data" / "analysis_ready" / "HRDI_2022_2023_12months_EXPLORATORY.csv")
hii_df = pd.read_csv(BASE_DIR / "data" / "completeness" / "hii_all_9_provinces_24_months.csv")
rice_df = pd.read_csv(BASE_DIR / "data" / "completeness" / "rice_all_921_tambons_2022_2023.csv")

# May-Aug (months 5, 6, 7, 8)
print("=== MAY-AUG RAINFALL AND RICE YIELD CHANGES (2022 -> 2023) ===")
provs = exp_df["PROVINCE"].unique()
for p in provs:
    # HII May-Aug
    h_p = hii_df[hii_df["province_name_th"] == p]
    h_22 = h_p[(h_p["year"] == 2022) & (h_p["month"].isin([5, 6, 7, 8]))]["avg_rain_mm"].sum()
    h_23 = h_p[(h_p["year"] == 2023) & (h_p["month"].isin([5, 6, 7, 8]))]["avg_rain_mm"].sum()
    h_diff = h_23 - h_22

    # HRDI May-Aug observed
    e_p = exp_df[exp_df["PROVINCE"] == p]
    # mean station rain May-Aug
    sta_22 = []
    sta_23 = []
    for s_code, s_grp in e_p.groupby("CODE_REF"):
        r22 = s_grp[(s_grp["YEAR"] == 2022) & (s_grp["MONTH_NUM"].isin([5, 6, 7, 8]))]["RAINFALL"].sum()
        r23 = s_grp[(s_grp["YEAR"] == 2023) & (s_grp["MONTH_NUM"].isin([5, 6, 7, 8]))]["RAINFALL"].sum()
        if pd.notna(r22): sta_22.append(r22)
        if pd.notna(r23): sta_23.append(r23)
    hrdi_22 = sum(sta_22)/len(sta_22) if sta_22 else None
    hrdi_23 = sum(sta_23)/len(sta_23) if sta_23 else None
    hrdi_diff = (hrdi_23 - hrdi_22) if hrdi_22 and hrdi_23 else None

    # Rice yield mean
    r_p = rice_df[rice_df["province_name"] == p]
    y22 = r_p[r_p["year"] == 2022]["yield_kg_per_rai"].mean()
    y23 = r_p[r_p["year"] == 2023]["yield_kg_per_rai"].mean()
    y_diff = (y23 - y22) if pd.notna(y22) and pd.notna(y23) else None

    print(f"{p}:")
    print(f"  HII May-Aug: 22={h_22:.1f}, 23={h_23:.1f} (diff={h_diff:+.1f} mm)")
    v22 = f"{hrdi_22:.1f}" if hrdi_22 else "None"
    v23 = f"{hrdi_23:.1f}" if hrdi_23 else "None"
    vd = f"{hrdi_diff:+.1f}" if hrdi_diff else "None"
    print(f"  HRDI May-Aug: 22={v22}, 23={v23} (diff={vd} mm)")
    print(f"  Rice Yield: 22={y22:.1f}, 23={y23:.1f} (diff={y_diff:+.1f} kg/rai)")
    print(f"  HII Rain Up & Yield Down? {h_diff > 0 and y_diff is not None and y_diff < 0}")
    print(f"  HRDI Rain Up & Yield Down? {hrdi_diff is not None and hrdi_diff > 0 and y_diff is not None and y_diff < 0}")
