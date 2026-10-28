"""
Script 54: Build Complete, Traceable, and Rigorous Data Ecosystem
Outputs:
1. data/analysis_ready/ (Pure observed data, no synthetic)
   - hrdi_station_monthly_observed.csv (976 rows)
   - hrdi_estimated_sensitivity.csv (7 rows)
   - hii_province_monthly_observed.csv (216 rows)
   - rice_tambon_annual_observed.csv (1695 rows)
   - geographic_linkage_verified.csv (50 stations, with pure python Ray-Casting Polygon verification)
   - rice_hrdi_tambon_panel_observed.csv (27 balanced tambons x 2 years = 54 rows)
   - rice_hrdi_tambon_panel_unbalanced.csv (33 tambons = 60 rows)
   - rice_hii_province_panel_observed.csv (9 provinces x 2 years = 18 rows)

2. data/experimental_complete/ (Full grid datasets for experimentation)
   - hrdi_experimental_complete.csv (1200 rows: 50 stations x 24 months)
   - hii_experimental_complete.csv (216 rows: 9 provinces x 24 months)
   - rice_experimental_complete.csv (1842 rows: 921 tambons x 2 years, non-cultivated tambons as not_registered)
   - rice_scenario_synthetic_simulation.csv (1842 rows: simulation scenario for pipeline testing)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"
PROCESSED = ROOT / "data" / "processed"
ANALYSIS_READY = ROOT / "data" / "analysis_ready"
EXPERIMENTAL = ROOT / "data" / "experimental_complete"
REPORTS = ROOT / "reports"

ANALYSIS_READY.mkdir(parents=True, exist_ok=True)
EXPERIMENTAL.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

print("=== 1. POINT-IN-POLYGON & GEOGRAPHIC LINKAGE ===")
def point_in_polygon(x, y, poly_coords):
    inside = False
    n = len(poly_coords)
    p1x, p1y = poly_coords[0]
    for i in range(1, n + 1):
        p2x, p2y = poly_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def point_in_multipolygon(x, y, multipoly):
    for poly in multipoly:
        if point_in_polygon(x, y, poly[0]):
            return True
    return False

with open(REF / "thailand_9provinces.geojson", "r", encoding="utf-8") as f:
    prov_geojson = json.load(f)

prov_geoms = {}
for feat in prov_geojson["features"]:
    p_code = feat["properties"]["pro_code"]
    geom = feat["geometry"]
    coords = geom["coordinates"]
    if geom["type"] == "Polygon":
        coords = [coords]
    prov_geoms[p_code] = coords

with open(REF / "geo.json", "r", encoding="utf-8-sig") as f:
    geo = json.load(f)

prov_9_codes = {"50", "55", "57", "58", "62", "63", "65", "67", "71"}
geo_records = []
for p in geo:
    p_code = str(p["code"]).zfill(2)
    if p_code in prov_9_codes:
        for d in p.get("districts", []):
            d_code = str(d["code"])
            for s in d.get("subdistricts", []):
                geo_records.append({
                    "geo_province_code": p_code,
                    "geo_province_name": p["name_th"],
                    "geo_amphoe_code": d_code,
                    "geo_amphoe_name": d["name_th"],
                    "geo_tambon_code_6": str(s["code"]).zfill(6),
                    "geo_tambon_name": s["name_th"]
                })
geo_df = pd.DataFrame(geo_records)

df_hrdi_raw = pd.read_csv(RAW / "HRDI_meteo.csv", dtype=str)
stations = df_hrdi_raw[[
    "CODE_REF", "STA_TH", "PROVINCE", "AMPHOE", "TAMBON", "LAT", "LONG"
]].drop_duplicates(subset=["CODE_REF"]).copy().sort_values("CODE_REF").reset_index(drop=True)

old_matching = pd.read_csv(REPORTS / "hrdi_crop_matching.csv", dtype=str)

linkage_rows = []
for _, st in stations.iterrows():
    c_ref = st["CODE_REF"]
    sta_th = st["STA_TH"]
    p_raw = str(st["PROVINCE"]).strip() if pd.notna(st["PROVINCE"]) else ""
    a_raw = str(st["AMPHOE"]).strip() if pd.notna(st["AMPHOE"]) else ""
    t_raw = str(st["TAMBON"]).strip() if pd.notna(st["TAMBON"]) else ""
    lat = float(st["LAT"]) if pd.notna(st["LAT"]) else np.nan
    lon = float(st["LONG"]) if pd.notna(st["LONG"]) else np.nan

    old_row = old_matching[old_matching["CODE_REF"] == c_ref]
    old_t_code = old_row["tambon_code_6"].values[0] if len(old_row) > 0 and pd.notna(old_row["tambon_code_6"].values[0]) else None

    if c_ref == "KLN":
        t_code = "620411"
        tier = "matched_tambon_alias_verified"
        eligible = True
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล ปางมะค่า (620411) ในอำเภอขาณุวรลักษบุรี (สะกดต่างจาก ขาณุวรลักษณบุรี)"
    elif c_ref == "NAN":
        t_code = "550103"
        tier = "matched_tambon_alias_verified"
        eligible = True
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล ผาสิงห์ (550103) ในอำเภอเมืองน่าน (HRDI บันทึกเพียง อำเภอเมือง)"
    elif c_ref == "RPF":
        t_code = "500109"
        tier = "matched_tambon_alias_verified"
        eligible = True
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล แม่เหียะ (500109) ในอำเภอเมืองเชียงใหม่ (HRDI บันทึกเพียง อำเภอเมือง)"
    elif c_ref == "MSL":
        t_code = None
        tier = "matched_amphoe_only"
        eligible = False
        notes = "จับคู่ได้ระดับอำเภอแม่ฟ้าหลวง (5715) จังหวัดเชียงราย แต่ตำบลแม่สลองแบ่งเป็น แม่สลองใน (571502) และ แม่สลองนอก (571503) จึงไม่นำมารวมในระดับตำบล"
    elif c_ref == "HHA":
        t_code = None
        tier = "matched_amphoe_only"
        eligible = False
        notes = "จับคู่ได้ระดับอำเภอปาย (5803) จังหวัดแม่ฮ่องสอน แต่ตำบลบันทึกเป็น เมืองปาย ซึ่งไม่มีในรหัสทางการ DOPA"
    elif c_ref in ["HNG", "OKI"]:
        t_code = None
        tier = "matched_amphoe_only"
        eligible = False
        notes = f"จับคู่ได้ระดับอำเภออมก๋อย (5018) จังหวัดเชียงใหม่ แต่ตำบลบันทึกเป็น สบโขง ซึ่งไม่มีในรหัสทางการของอำเภออมก๋อยใน DOPA GeoThai"
    elif old_t_code:
        t_code = old_t_code
        tier = "matched_tambon_exact"
        eligible = True
        notes = "จับคู่ระดับตำบลสมบูรณ์ ตรงทั้งชื่อจังหวัด อำเภอ และตำบลตามฐานข้อมูล DOPA GeoThai"
    else:
        t_code = None
        tier = "unmatched"
        eligible = False
        notes = "ไม่สามารถจับคู่ได้"

    if t_code:
        g_match = geo_df[geo_df["geo_tambon_code_6"] == t_code].iloc[0]
        p_code = g_match["geo_province_code"]
        p_name = g_match["geo_province_name"]
        a_code = g_match["geo_amphoe_code"]
        a_name = g_match["geo_amphoe_name"]
        t_name = g_match["geo_tambon_name"]
    else:
        p_matches = geo_df[geo_df["geo_province_name"] == p_raw]
        p_code = p_matches["geo_province_code"].iloc[0] if len(p_matches) > 0 else None
        p_name = p_raw
        a_matches = p_matches[p_matches["geo_amphoe_name"].str.contains(a_raw[:4], na=False)]
        a_code = a_matches["geo_amphoe_code"].iloc[0] if len(a_matches) > 0 else None
        a_name = a_raw
        t_name = t_raw

    # Verify point-in-polygon against declared province boundary
    in_prov = point_in_multipolygon(lon, lat, prov_geoms[p_code]) if p_code in prov_geoms else False

    linkage_rows.append({
        "station_code": c_ref,
        "station_name_th": sta_th,
        "hrdi_province_raw": p_raw,
        "hrdi_amphoe_raw": a_raw,
        "hrdi_tambon_raw": t_raw,
        "station_lat": lat,
        "station_lon": lon,
        "geo_province_code": p_code,
        "geo_province_name": p_name,
        "geo_amphoe_code": a_code,
        "geo_amphoe_name": a_name,
        "geo_tambon_code_6": t_code,
        "geo_tambon_name": t_name,
        "linkage_tier": tier,
        "eligible_for_tambon_panel": eligible,
        "gis_province_polygon_verified": in_prov,
        "gis_tambon_polygon_verified": False,
        "matching_type": "administrative_name_matching",
        "linkage_notes": notes
    })

linkage_df = pd.DataFrame(linkage_rows)
assert linkage_df["gis_province_polygon_verified"].all()
linkage_df.to_csv(ANALYSIS_READY / "geographic_linkage_verified.csv", index=False, encoding="utf-8-sig")
print("Saved geographic_linkage_verified.csv (50 stations, 100% inside province polygon).")

print("\n=== 2. HII PROVINCE MONTHLY OBSERVED ===")
df_hii_raw = pd.read_csv(RAW / "spatial-rain-hii.csv")
df_hii_raw.columns = df_hii_raw.columns.str.strip()

df_hii_raw["YEAR"] = pd.to_numeric(df_hii_raw["YEAR"], errors="coerce").astype(int)
df_hii_raw["MONTH"] = pd.to_numeric(df_hii_raw["MONTH"], errors="coerce").astype(int)
df_hii_raw["MinRain"] = pd.to_numeric(df_hii_raw["MinRain"], errors="coerce")
df_hii_raw["MaxRain"] = pd.to_numeric(df_hii_raw["MaxRain"], errors="coerce")
df_hii_raw["AvgRain"] = pd.to_numeric(df_hii_raw["AvgRain"], errors="coerce")

hii_obs = df_hii_raw[
    (df_hii_raw["YEAR"].isin([2022, 2023])) &
    (df_hii_raw["PROV_T"].isin(linkage_df["geo_province_name"].unique()))
].copy().sort_values(["YEAR", "MONTH", "PROV_ID"]).reset_index(drop=True)

hii_obs = hii_obs.rename(columns={
    "YEAR": "year",
    "MONTH": "month",
    "PROV_ID": "province_id",
    "PROV_T": "province_name_th",
    "MinRain": "min_rain_mm",
    "MaxRain": "max_rain_mm",
    "AvgRain": "avg_rain_mm"
})

hii_obs["data_status"] = "observed"
hii_obs["source_file"] = "data/raw/spatial-rain-hii.csv"
hii_obs["measurement_unit"] = "millimeter_monthly_provincial_area_weighted"

assert len(hii_obs) == 216
hii_obs.to_csv(ANALYSIS_READY / "hii_province_monthly_observed.csv", index=False, encoding="utf-8-sig")
hii_obs.to_csv(EXPERIMENTAL / "hii_experimental_complete.csv", index=False, encoding="utf-8-sig")
print("Saved HII datasets (216 rows, 100% observed).")

print("\n=== 3. HRDI OBSERVED & EXPERIMENTAL COMPLETE ===")
hrdi_clean = pd.read_csv(PROCESSED / "hrdi_clean_2022_2023.csv")
hrdi_clean["year"] = pd.to_numeric(hrdi_clean["year"], errors="coerce").astype(int)
hrdi_clean["month"] = pd.to_numeric(hrdi_clean["month"], errors="coerce").astype(int)
for col in ["rainfall_mm", "TEMP", "TEMP_MIN", "TEMP_MAX", "HUMIDITY", "WIND_SPEED", "RAINDAY"]:
    hrdi_clean[col] = pd.to_numeric(hrdi_clean[col], errors="coerce")

hrdi_obs_raw = hrdi_clean[hrdi_clean["rainfall_mm"].notna()].copy()
assert len(hrdi_obs_raw) == 976

hrdi_obs = hrdi_obs_raw.rename(columns={"CODE_REF": "station_code"}).merge(
    linkage_df[[
        "station_code", "geo_province_code", "geo_province_name",
        "geo_amphoe_code", "geo_amphoe_name", "geo_tambon_code_6", "geo_tambon_name",
        "eligible_for_tambon_panel"
    ]],
    on="station_code", how="left"
)

anomalous_zero_stations = {"FON", "PAO", "KST", "HKP", "NPAK"}
hrdi_obs["is_monsoon_zero_rain_anomalous"] = hrdi_obs["station_code"].isin(anomalous_zero_stations)

hrdi_obs_out = hrdi_obs.rename(columns={
    "STA_TH": "station_name_th",
    "geo_province_name": "province",
    "geo_amphoe_name": "amphoe",
    "geo_tambon_name": "tambon",
    "geo_tambon_code_6": "tambon_code_6",
    "LAT": "lat",
    "LONG": "long",
    "TEMP": "temp_c",
    "TEMP_MIN": "temp_min_c",
    "TEMP_MAX": "temp_max_c",
    "HUMIDITY": "humidity_pct",
    "WIND_SPEED": "wind_speed_ms",
    "RAINDAY": "rainday_count"
})[[
    "station_code", "station_name_th", "province", "amphoe", "tambon",
    "tambon_code_6", "lat", "long", "year", "month",
    "rainfall_mm", "temp_c", "temp_min_c", "temp_max_c",
    "humidity_pct", "wind_speed_ms", "rainday_count",
    "source_type", "is_monsoon_zero_rain_anomalous", "eligible_for_tambon_panel"
]].copy().sort_values(["station_code", "year", "month"]).reset_index(drop=True)

hrdi_obs_out["data_status"] = "observed"
hrdi_obs_out["source_file"] = "data/raw/HRDI_meteo.csv"

hrdi_obs_out.to_csv(ANALYSIS_READY / "hrdi_station_monthly_observed.csv", index=False, encoding="utf-8-sig")
print("Saved hrdi_station_monthly_observed.csv (976 rows).")

# Save estimated sensitivity (7 rows)
synth_hrdi = pd.read_csv(ROOT / "data" / "synthetic" / "hrdi_completed_experimental.csv")
hrdi_est = synth_hrdi[synth_hrdi["data_status"] == "estimated"].copy()
assert len(hrdi_est) == 7
hrdi_est.to_csv(ANALYSIS_READY / "hrdi_estimated_sensitivity.csv", index=False, encoding="utf-8-sig")
print("Saved hrdi_estimated_sensitivity.csv (7 rows).")

# Experimental complete HRDI (1200 rows)
synth_hrdi.to_csv(EXPERIMENTAL / "hrdi_experimental_complete.csv", index=False, encoding="utf-8-sig")
print("Saved hrdi_experimental_complete.csv (1200 rows).")

print("\n=== 4. DOAE RICE DATASETS ===")
c22 = pd.read_csv(REPORTS / "crop_2022_normalized.csv", dtype=str)
c23 = pd.read_csv(REPORTS / "crop_2023_normalized.csv", dtype=str)

c22["prod_norm"] = c22["product_id"].astype(str).str.zfill(6)
c23["prod_norm"] = c23["product_id"].astype(str).str.zfill(6)

for c in ["area_plant", "area_harvest", "product_harvest"]:
    c22[c] = pd.to_numeric(c22[c], errors="coerce")
    c23[c] = pd.to_numeric(c23[c], errors="coerce")

r22 = c22[(c22["code_valid"] == "True") & (c22["prod_norm"] == "011000")].copy()
r23 = c23[(c23["code_valid"] == "True") & (c23["prod_norm"] == "011000")].copy()

r22_agg = r22.groupby("tambon_code_6", as_index=False).agg({
    "area_plant": "sum", "area_harvest": "sum", "product_harvest": "sum"
})
r22_agg["year"] = 2022
r22_agg["source_file"] = "data/raw/plant01_65.csv"

r23_agg = r23.groupby("tambon_code_6", as_index=False).agg({
    "area_plant": "sum", "area_harvest": "sum", "product_harvest": "sum"
})
r23_agg["year"] = 2023
r23_agg["source_file"] = "data/raw/5.-01-2566.csv"

rice_obs = pd.concat([r22_agg, r23_agg], ignore_index=True)
assert len(rice_obs) == 1695

rice_obs = rice_obs.merge(geo_df, left_on="tambon_code_6", right_on="geo_tambon_code_6", how="left")
rice_obs["yield_kg_per_rai"] = np.where(
    rice_obs["area_harvest"] > 0,
    np.round(rice_obs["product_harvest"] / rice_obs["area_harvest"], 2),
    0.0
)
rice_obs["is_unharvested_crop_failure"] = (rice_obs["area_plant"] > 0) & (rice_obs["area_harvest"] == 0)

rice_obs_out = rice_obs.rename(columns={
    "geo_province_code": "province_code",
    "geo_province_name": "province_name",
    "geo_amphoe_code": "amphoe_code",
    "geo_amphoe_name": "amphoe_name",
    "geo_tambon_name": "tambon_name",
    "area_plant": "plant_area_rai",
    "area_harvest": "harvest_area_rai",
    "product_harvest": "production_kg"
})[[
    "year", "province_code", "province_name", "amphoe_code", "amphoe_name",
    "tambon_code_6", "tambon_name", "plant_area_rai", "harvest_area_rai",
    "production_kg", "yield_kg_per_rai", "is_unharvested_crop_failure",
    "source_file"
]].copy().sort_values(["province_code", "amphoe_code", "tambon_code_6", "year"]).reset_index(drop=True)

rice_obs_out["crop_type"] = "wet_season_lowland_rice_011000"
rice_obs_out["registration_status"] = "registered_observed"
rice_obs_out["data_status"] = "observed"

rice_obs_out.to_csv(ANALYSIS_READY / "rice_tambon_annual_observed.csv", index=False, encoding="utf-8-sig")
print("Saved rice_tambon_annual_observed.csv (1695 rows).")

# EXPERIMENTAL COMPLETE RICE (1842 rows)
# Build full grid: 921 tambons x 2 years
rice_grid = []
for _, tb in geo_df.iterrows():
    for yr in [2022, 2023]:
        rice_grid.append({
            "year": yr,
            "province_code": tb["geo_province_code"],
            "province_name": tb["geo_province_name"],
            "amphoe_code": tb["geo_amphoe_code"],
            "amphoe_name": tb["geo_amphoe_name"],
            "tambon_code_6": tb["geo_tambon_code_6"],
            "tambon_name": tb["geo_tambon_name"]
        })
rice_grid_df = pd.DataFrame(rice_grid)

rice_exp = rice_grid_df.merge(
    rice_obs_out[[
        "tambon_code_6", "year", "crop_type", "plant_area_rai",
        "harvest_area_rai", "production_kg", "yield_kg_per_rai",
        "is_unharvested_crop_failure", "registration_status", "data_status",
        "source_file"
    ]],
    on=["tambon_code_6", "year"],
    how="left"
)

# For unobserved/non-registered tambons: DO NOT fabricate positive rice farms!
# Represent truthfully as not_registered / no_cultivation
unobs_mask = rice_exp["data_status"].isna()
rice_exp.loc[unobs_mask, "crop_type"] = "wet_season_lowland_rice_011000"
rice_exp.loc[unobs_mask, "plant_area_rai"] = 0.0
rice_exp.loc[unobs_mask, "harvest_area_rai"] = 0.0
rice_exp.loc[unobs_mask, "production_kg"] = 0.0
rice_exp.loc[unobs_mask, "yield_kg_per_rai"] = np.nan
rice_exp.loc[unobs_mask, "is_unharvested_crop_failure"] = False
rice_exp.loc[unobs_mask, "registration_status"] = "not_registered"
rice_exp.loc[unobs_mask, "data_status"] = "not_registered"
rice_exp.loc[unobs_mask, "source_file"] = "official_administrative_grid_non_cultivated"

assert len(rice_exp) == 1842
rice_exp.to_csv(EXPERIMENTAL / "rice_experimental_complete.csv", index=False, encoding="utf-8-sig")
print("Saved rice_experimental_complete.csv (1842 rows: 1695 observed, 147 not_registered).")

# Save dedicated simulation scenario file for testing/ML
rice_scenario = rice_exp.copy()
prov_yield_stats = rice_obs_out[rice_obs_out["yield_kg_per_rai"] > 0].groupby(
    ["province_name", "year"]
)["yield_kg_per_rai"].agg(["mean", "std"]).to_dict("index")

synth_yields = []
for _, r in rice_scenario.iterrows():
    if r["data_status"] == "observed":
        synth_yields.append(r["yield_kg_per_rai"])
    else:
        p_name = r["province_name"]
        yr = r["year"]
        st = prov_yield_stats.get((p_name, yr), {"mean": 550.0, "std": 85.0})
        m = st["mean"] if pd.notna(st["mean"]) else 550.0
        s = st["std"] if pd.notna(st["std"]) and st["std"] > 0 else 85.0
        val = np.round(np.clip(np.random.normal(m, s), 250.0, 950.0), 2)
        synth_yields.append(val)
rice_scenario["scenario_simulation_yield_kg_per_rai"] = synth_yields
rice_scenario.to_csv(EXPERIMENTAL / "rice_scenario_synthetic_simulation.csv", index=False, encoding="utf-8-sig")
print("Saved rice_scenario_synthetic_simulation.csv (1842 rows).")

print("\n=== 5. BALANCED & UNBALANCED RESEARCH PANELS ===")
hrdi_valid = hrdi_obs_out[
    hrdi_obs_out["month"].isin([5, 6, 7, 8]) &
    (hrdi_obs_out["eligible_for_tambon_panel"] == True) &
    (hrdi_obs_out["is_monsoon_zero_rain_anomalous"] == False)
].copy()

m_count = hrdi_valid.groupby(["station_code", "year"])["month"].nunique().reset_index()
complete_st_yr = m_count[m_count["month"] == 4][["station_code", "year"]]
hrdi_valid_4m = hrdi_valid.merge(complete_st_yr, on=["station_code", "year"])

# Aggregate rain by tambon_code_6
tam_rain_st = hrdi_valid_4m.groupby(["year", "station_code", "tambon_code_6"], as_index=False)["rainfall_mm"].sum()
tam_rain = tam_rain_st.groupby(["year", "tambon_code_6"], as_index=False).agg(
    hrdi_may_aug_mean_rain_mm=("rainfall_mm", "mean"),
    station_count=("station_code", "nunique"),
    station_codes=("station_code", lambda s: ", ".join(sorted(set(s))))
)
tam_rain["hrdi_may_aug_mean_rain_mm"] = np.round(tam_rain["hrdi_may_aug_mean_rain_mm"], 2)

# Unbalanced Panel
unbalanced_panel = rice_obs_out[rice_obs_out["is_unharvested_crop_failure"] == False].merge(
    tam_rain, on=["year", "tambon_code_6"], how="inner"
).sort_values(["province_code", "tambon_code_6", "year"]).reset_index(drop=True)
unbalanced_panel.to_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_unbalanced.csv", index=False, encoding="utf-8-sig")
print(f"Saved rice_hrdi_tambon_panel_unbalanced.csv ({len(unbalanced_panel)} rows, {unbalanced_panel['tambon_code_6'].nunique()} unique tambons).")

# Balanced Panel
years_per_tb = unbalanced_panel.groupby("tambon_code_6")["year"].nunique()
balanced_tb = years_per_tb[years_per_tb == 2].index
balanced_panel = unbalanced_panel[unbalanced_panel["tambon_code_6"].isin(balanced_tb)].copy().sort_values(
    ["province_code", "tambon_code_6", "year"]
).reset_index(drop=True)
assert len(balanced_panel) == 54
balanced_panel.to_csv(ANALYSIS_READY / "rice_hrdi_tambon_panel_observed.csv", index=False, encoding="utf-8-sig")
print(f"Saved rice_hrdi_tambon_panel_observed.csv ({len(balanced_panel)} rows, 27 balanced tambons).")

# Provincial Panel
prov_rice = rice_obs_out.groupby(["year", "province_code", "province_name"], as_index=False).agg(
    total_plant_area_rai=("plant_area_rai", "sum"),
    total_harvest_area_rai=("harvest_area_rai", "sum"),
    total_production_kg=("production_kg", "sum"),
    tambon_count=("tambon_code_6", "nunique")
)
prov_rice["weighted_yield_kg_per_rai"] = np.round(
    prov_rice["total_production_kg"] / prov_rice["total_harvest_area_rai"], 2
)

hii_may_aug = hii_obs[hii_obs["month"].isin([5, 6, 7, 8])].groupby(
    ["year", "province_name_th"], as_index=False
)["avg_rain_mm"].sum().rename(columns={"avg_rain_mm": "hii_may_aug_rain_mm"})
hii_may_aug["hii_may_aug_rain_mm"] = np.round(hii_may_aug["hii_may_aug_rain_mm"], 2)

hii_annual = hii_obs.groupby(
    ["year", "province_name_th"], as_index=False
)["avg_rain_mm"].sum().rename(columns={"avg_rain_mm": "hii_annual_rain_mm"})
hii_annual["hii_annual_rain_mm"] = np.round(hii_annual["hii_annual_rain_mm"], 2)

hii_prov_summary = hii_may_aug.merge(hii_annual, on=["year", "province_name_th"])

prov_panel = prov_rice.merge(
    hii_prov_summary,
    left_on=["year", "province_name"],
    right_on=["year", "province_name_th"],
    how="inner"
).drop(columns=["province_name_th"])
assert len(prov_panel) == 18
prov_panel.to_csv(ANALYSIS_READY / "rice_hii_province_panel_observed.csv", index=False, encoding="utf-8-sig")
print(f"Saved rice_hii_province_panel_observed.csv ({len(prov_panel)} rows).")

print("\n=== DATA GENERATION COMPLETE ===")
