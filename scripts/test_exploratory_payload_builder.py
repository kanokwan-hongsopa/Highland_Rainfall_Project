# -*- coding: utf-8 -*-
"""
Prototype & Test Payload Generator incorporating HRDI_2022_2023_12months_EXPLORATORY.csv
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
EXP_PATH = BASE_DIR / "data" / "analysis_ready" / "HRDI_2022_2023_12months_EXPLORATORY.csv"
HII_PATH = BASE_DIR / "data" / "completeness" / "hii_all_9_provinces_24_months.csv"
RICE_PATH = BASE_DIR / "data" / "completeness" / "rice_all_921_tambons_2022_2023.csv"
GEOJSON_FILE = BASE_DIR / "data" / "reference" / "thailand_9provinces.geojson"

df_exp = pd.read_csv(EXP_PATH)
df_hii = pd.read_csv(HII_PATH)
df_rice = pd.read_csv(RICE_PATH)

print(f"Loaded: exp={len(df_exp)}, hii={len(df_hii)}, rice={len(df_rice)}")

# 1. Build stations list
stations_dict = {}
for code, group in df_exp.groupby("CODE_REF"):
    g_sorted = group.sort_values(["YEAR", "MONTH_NUM"])
    first = g_sorted.iloc[0]
    
    m_obs_24 = []
    m_exp_24 = []
    m_status_24 = []
    
    for _, r in g_sorted.iterrows():
        c_status = r["completion_status"]
        rf_raw = r["RAINFALL"]
        rf_exp = r["rainfall_completed_exploratory_mm"]
        
        m_status_24.append(c_status)
        if c_status == "observed" and pd.notna(rf_raw):
            m_obs_24.append(round(float(rf_raw), 1))
        else:
            m_obs_24.append(None)
        m_exp_24.append(round(float(rf_exp), 1) if pd.notna(rf_exp) else None)
        
    obs_cnt_22 = sum(1 for x in m_obs_24[:12] if x is not None)
    obs_cnt_23 = sum(1 for x in m_obs_24[12:24] if x is not None)
    obs_cnt_tot = obs_cnt_22 + obs_cnt_23
    est_cnt_tot = sum(1 for s in m_status_24 if s == "estimated")
    exp_cnt_tot = sum(1 for s in m_status_24 if s == "estimated_exploratory")
    
    # Rule 7: ห้ามแสดงผลรวมทั้งปีของสถานีที่ไม่ครบ 12 เดือนในโหมด Observed!
    annual_obs_22 = round(sum(m_obs_24[:12]), 1) if obs_cnt_22 == 12 else None
    annual_obs_23 = round(sum(m_obs_24[12:24]), 1) if obs_cnt_23 == 12 else None
    
    annual_exp_22 = round(sum(m_exp_24[:12]), 1)
    annual_exp_23 = round(sum(m_exp_24[12:24]), 1)
    annual_exp_all = round((annual_exp_22 + annual_exp_23) / 2, 1)
    
    status_label = f"ตรวจวัดจริง {obs_cnt_tot}/24 ด."
    if est_cnt_tot > 0:
        status_label += f" (DEMO {est_cnt_tot} ด.)"
    if exp_cnt_tot > 0:
        status_label += f" (Exploratory {exp_cnt_tot} ด.)"
        
    stations_dict[code] = {
        "name": str(first["STA_TH"]),
        "code_ref": str(code),
        "province": str(first["PROVINCE"]),
        "amphoe": str(first["AMPHOE"]),
        "tambon": str(first["TAMBON"]),
        "observed_count_2022": obs_cnt_22,
        "observed_count_2023": obs_cnt_23,
        "observed_count_total": obs_cnt_tot,
        "estimated_count_total": est_cnt_tot,
        "exploratory_count_total": exp_cnt_tot,
        "data_status_label": status_label,
        "annual_obs_2022": annual_obs_22,
        "annual_obs_2023": annual_obs_23,
        "annual_exp_2022": annual_exp_22,
        "annual_exp_2023": annual_exp_23,
        "annual_exp_all": annual_exp_all,
        "monthly_obs_2022": m_obs_24[:12],
        "monthly_obs_2023": m_obs_24[12:24],
        "monthly_exp_2022": m_exp_24[:12],
        "monthly_exp_2023": m_exp_24[12:24],
        "monthly_obs_24": m_obs_24,
        "monthly_exp_24": m_exp_24,
        "monthly_status_24": m_status_24,
    }

print(f"Generated {len(stations_dict)} stations metadata.")

# 2. Build province summaries
prov_summaries = {}
for p in df_exp["PROVINCE"].unique():
    p_df = df_exp[df_exp["PROVINCE"] == p]
    p_stas = [s for s in stations_dict.values() if s["province"] == p]
    sta_names = [s["name"] for s in p_stas]
    
    # 2022
    comp_22 = [s for s in p_stas if s["annual_obs_2022"] is not None]
    prov_obs_22 = round(sum(s["annual_obs_22"] for s in comp_22) / len(comp_22), 1) if len(comp_22) == len(p_stas) else (round(sum(s["annual_obs_22"] for s in comp_22) / len(comp_22), 1) if len(comp_22) > 0 else None)
    # 2023
    comp_23 = [s for s in p_stas if s["annual_obs_2023"] is not None]
    prov_obs_23 = None # 0 stations complete in 2023
    
    # Exploratory sums
    prov_exp_22 = round(sum(s["annual_exp_2022"] for s in p_stas) / len(p_stas), 1)
    prov_exp_23 = round(sum(s["annual_exp_2023"] for s in p_stas) / len(p_stas), 1)
    prov_exp_all = round((prov_exp_22 + prov_exp_23) / 2, 1)
    
    # Monthly averages across stations in province
    monthly_obs_22 = []
    monthly_obs_23 = []
    monthly_exp_22 = []
    monthly_exp_23 = []
    
    for m in range(12):
        obs_vals_22 = [s["monthly_obs_2022"][m] for s in p_stas if s["monthly_obs_2022"][m] is not None]
        obs_vals_23 = [s["monthly_obs_2023"][m] for s in p_stas if s["monthly_obs_2023"][m] is not None]
        exp_vals_22 = [s["monthly_exp_2022"][m] for s in p_stas if s["monthly_exp_2022"][m] is not None]
        exp_vals_23 = [s["monthly_exp_2023"][m] for s in p_stas if s["monthly_exp_2023"][m] is not None]
        
        monthly_obs_22.append(round(sum(obs_vals_22) / len(obs_vals_22), 1) if obs_vals_22 else None)
        monthly_obs_23.append(round(sum(obs_vals_23) / len(obs_vals_23), 1) if obs_vals_23 else None)
        monthly_exp_22.append(round(sum(exp_vals_22) / len(exp_vals_22), 1) if exp_vals_22 else None)
        monthly_exp_23.append(round(sum(exp_vals_23) / len(exp_vals_23), 1) if exp_vals_23 else None)
        
    prov_summaries[p] = {
        "name": p,
        "station_count": len(p_stas),
        "stations": sta_names,
        "rain_obs_2022": prov_obs_22,
        "rain_obs_2023": prov_obs_23,
        "rain_exp_2022": prov_exp_22,
        "rain_exp_2023": prov_exp_23,
        "rain_exp_all": prov_exp_all,
        "monthly_obs_2022": monthly_obs_22,
        "monthly_obs_2023": monthly_obs_23,
        "monthly_exp_2022": monthly_exp_22,
        "monthly_exp_2023": monthly_exp_23,
    }

print(f"Generated {len(prov_summaries)} province summaries.")
for p, s in prov_summaries.items():
    print(f"  {p}: stas={s['station_count']}, obs22={s['rain_obs_2022']}, obs23={s['rain_obs_2023']}, exp22={s['rain_exp_2022']}, exp23={s['rain_exp_2023']}")

print("\n[SUCCESS] Test payload builder completed!")
