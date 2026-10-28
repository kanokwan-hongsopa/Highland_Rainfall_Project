"""
Script 50: Create Experimental Completed & Synthetic Datasets
Generates:
1. data/synthetic/geographic_linkage.csv
2. data/synthetic/hrdi_completed_experimental.csv
3. data/synthetic/hii_completed_experimental.csv
4. data/synthetic/rice_completed_experimental.csv
Strictly adheres to:
- No changes to raw data
- Clear data_status: observed, estimated, synthetic
- Full traceability: method, source_file, uncertainty
- Preserves observed data completely untouched
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"
PROCESSED = ROOT / "data" / "processed"
SYNTHETIC = ROOT / "data" / "synthetic"
REPORTS = ROOT / "reports"

SYNTHETIC.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducible stochastic simulations
np.random.seed(42)

print("=== STEP 1: GEOGRAPHIC LINKAGE TABLE ===")
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
print(f"Total GeoThai tambons in 9 provinces: {len(geo_df)}")

# Load HRDI stations
df_hrdi_raw = pd.read_csv(RAW / "HRDI_meteo.csv", dtype=str)
stations = df_hrdi_raw[[
    "CODE_REF", "STA_TH", "PROVINCE", "AMPHOE", "TAMBON", "LAT", "LONG"
]].drop_duplicates(subset=["CODE_REF"]).copy().sort_values("CODE_REF").reset_index(drop=True)

# Previous matching table
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

    # Check in old matching
    old_row = old_matching[old_matching["CODE_REF"] == c_ref]
    old_t_code = old_row["tambon_code_6"].values[0] if len(old_row) > 0 and pd.notna(old_row["tambon_code_6"].values[0]) else None

    # Handle known aliases
    if c_ref == "KLN":
        # Khlong Lan station in Kamphaeng Phet, subdistrict Pang Ma Kha
        t_code = "620411"
        tier = "matched_tambon_alias_verified"
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล ปางมะค่า (620411) ในอำเภอขาณุวรลักษบุรี (สะกดต่างจาก ขาณุวรลักษณบุรี)"
    elif c_ref == "NAN":
        # Nan station in Mueang Nan, subdistrict Pha Sing
        t_code = "550103"
        tier = "matched_tambon_alias_verified"
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล ผาสิงห์ (550103) ในอำเภอเมืองน่าน (HRDI บันทึกเพียง อำเภอเมือง)"
    elif c_ref == "RPF":
        # Royal Park Rajapruek in Mueang Chiang Mai, subdistrict Mae Hia
        t_code = "500109"
        tier = "matched_tambon_alias_verified"
        notes = "จับคู่ระดับตำบลสำเร็จจากชื่อตำบล แม่เหียะ (500109) ในอำเภอเมืองเชียงใหม่ (HRDI บันทึกเพียง อำเภอเมือง)"
    elif c_ref == "MSL":
        # Mae Salong (Mae Fa Luang, Chiang Rai) - split between 571502 and 571503
        t_code = None
        tier = "matched_amphoe_only_ambiguous_subdistrict"
        notes = "จับคู่ได้ระดับอำเภอแม่ฟ้าหลวง (5715) จังหวัดเชียงราย แต่ตำบลแม่สลองในฐานข้อมูล DOPA แบ่งเป็น แม่สลองใน (571502) และ แม่สลองนอก (571503) จึงไม่ผูกรหัสตำบลเพื่อป้องกันการระบุผิดพลาดโดยไม่มี GIS polygon"
    elif c_ref == "HHA":
        # Huai Ha (Pai, Mae Hong Son) - subdistrict listed as เมืองปาย
        t_code = None
        tier = "matched_amphoe_only_ambiguous_subdistrict"
        notes = "จับคู่ได้ระดับอำเภอปาย (5803) จังหวัดแม่ฮ่องสอน แต่ตำบลบันทึกเป็น เมืองปาย ซึ่งไม่มีในรหัสทางการ DOPA"
    elif c_ref in ["HNG", "OKI"]:
        # Sop Khong in Omkoi, Chiang Mai
        t_code = None
        tier = "matched_amphoe_only_ambiguous_subdistrict"
        notes = f"จับคู่ได้ระดับอำเภออมก๋อย (5018) จังหวัดเชียงใหม่ แต่ตำบลบันทึกเป็น สบโขง ซึ่งไม่มีในรหัสตำบลทางการของอำเภออมก๋อยในฐานข้อมูล DOPA"
    elif old_t_code:
        t_code = old_t_code
        tier = "matched_tambon_exact"
        notes = "จับคู่ระดับตำบลสมบูรณ์ ตรงทั้งชื่อจังหวัด อำเภอ และตำบลตามฐานข้อมูล DOPA GeoThai"
    else:
        t_code = None
        tier = "unmatched_area"
        notes = "ไม่สามารถจับคู่ระดับตำบลได้"

    # Fill geographic metadata from GeoThai if t_code exists
    if t_code:
        g_match = geo_df[geo_df["geo_tambon_code_6"] == t_code].iloc[0]
        p_code = g_match["geo_province_code"]
        p_name = g_match["geo_province_name"]
        a_code = g_match["geo_amphoe_code"]
        a_name = g_match["geo_amphoe_name"]
        t_name = g_match["geo_tambon_name"]
    else:
        # Fallback to province/amphoe matching from GeoThai
        p_matches = geo_df[geo_df["geo_province_name"] == p_raw]
        p_code = p_matches["geo_province_code"].iloc[0] if len(p_matches) > 0 else None
        p_name = p_raw
        a_matches = p_matches[p_matches["geo_amphoe_name"].str.contains(a_raw[:4], na=False)]
        a_code = a_matches["geo_amphoe_code"].iloc[0] if len(a_matches) > 0 else None
        a_name = a_raw
        t_name = t_raw

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
        "gis_spatial_polygon_verified": False,
        "linkage_notes": notes
    })

linkage_df = pd.DataFrame(linkage_rows)
linkage_path = SYNTHETIC / "geographic_linkage.csv"
linkage_df.to_csv(linkage_path, index=False, encoding="utf-8-sig")
print(f"Saved geographic linkage table: {linkage_path}")
print("Linkage tier breakdown:")
print(linkage_df["linkage_tier"].value_counts())

print("\n=== STEP 2: HII COMPLETED EXPERIMENTAL DATASET ===")
# HII is 100% complete for all 24 months across all 77 provinces!
df_hii_raw = pd.read_csv(RAW / "spatial-rain-hii.csv")
df_hii_raw.columns = df_hii_raw.columns.str.strip()

# Standardize column types
df_hii_raw["YEAR"] = pd.to_numeric(df_hii_raw["YEAR"], errors="coerce").astype(int)
df_hii_raw["MONTH"] = pd.to_numeric(df_hii_raw["MONTH"], errors="coerce").astype(int)
df_hii_raw["MinRain"] = pd.to_numeric(df_hii_raw["MinRain"], errors="coerce")
df_hii_raw["MaxRain"] = pd.to_numeric(df_hii_raw["MaxRain"], errors="coerce")
df_hii_raw["AvgRain"] = pd.to_numeric(df_hii_raw["AvgRain"], errors="coerce")

# Filter 2022-2023 for 9 provinces
hii_completed = df_hii_raw[
    (df_hii_raw["YEAR"].isin([2022, 2023])) &
    (df_hii_raw["PROV_T"].isin(linkage_df["geo_province_name"].unique()))
].copy().sort_values(["YEAR", "MONTH", "PROV_ID"]).reset_index(drop=True)

hii_completed = hii_completed.rename(columns={
    "YEAR": "year",
    "MONTH": "month",
    "PROV_ID": "province_id",
    "PROV_T": "province_name_th",
    "MinRain": "min_rain_mm",
    "MaxRain": "max_rain_mm",
    "AvgRain": "avg_rain_mm"
})

hii_completed["data_status"] = "observed"
hii_completed["method"] = "official_hii_satellite_gauge_spatial_interpolation"
hii_completed["source_file"] = "data/raw/spatial-rain-hii.csv"
hii_completed["uncertainty_std"] = 0.0

assert len(hii_completed) == 9 * 24  # Exactly 216 rows
assert not hii_completed.isna().any().any()

hii_path = SYNTHETIC / "hii_completed_experimental.csv"
hii_completed.to_csv(hii_path, index=False, encoding="utf-8-sig")
print(f"Saved HII completed experimental dataset ({len(hii_completed)} rows): {hii_path}")

print("\n=== STEP 3: HRDI COMPLETED EXPERIMENTAL DATASET ===")
# Load clean HRDI
hrdi_clean = pd.read_csv(PROCESSED / "hrdi_clean_2022_2023.csv")
hrdi_clean["year"] = pd.to_numeric(hrdi_clean["year"], errors="coerce").astype(int)
hrdi_clean["month"] = pd.to_numeric(hrdi_clean["month"], errors="coerce").astype(int)
for col in ["rainfall_mm", "TEMP", "TEMP_MIN", "TEMP_MAX", "HUMIDITY", "WIND_SPEED", "RAINDAY"]:
    hrdi_clean[col] = pd.to_numeric(hrdi_clean[col], errors="coerce")

# Build target grid: 50 stations x 24 months = 1,200 rows
target_grid = []
for _, st in linkage_df.iterrows():
    for y in [2022, 2023]:
        for m in range(1, 13):
            target_grid.append({
                "station_code": st["station_code"],
                "station_name_th": st["station_name_th"],
                "province": st["geo_province_name"],
                "amphoe": st["geo_amphoe_name"],
                "tambon": st["geo_tambon_name"],
                "tambon_code_6": st["geo_tambon_code_6"],
                "lat": st["station_lat"],
                "long": st["station_lon"],
                "year": y,
                "month": m
            })
grid_df = pd.DataFrame(target_grid)

# Merge grid with clean HRDI
hrdi_merged = grid_df.merge(
    hrdi_clean[[
        "CODE_REF", "year", "month", "rainfall_mm",
        "TEMP", "TEMP_MIN", "TEMP_MAX", "HUMIDITY", "WIND_SPEED", "RAINDAY"
    ]],
    left_on=["station_code", "year", "month"],
    right_on=["CODE_REF", "year", "month"],
    how="left"
).drop(columns=["CODE_REF"])

# Merge with HII monthly provincial rain for ratio calibration
hrdi_merged = hrdi_merged.merge(
    hii_completed[["year", "month", "province_name_th", "avg_rain_mm"]].rename(
        columns={"province_name_th": "province", "avg_rain_mm": "hii_prov_rain_mm"}
    ),
    on=["year", "month", "province"],
    how="left"
)

# Compute historical empirical ratio k_s = mean(station_rain) / mean(prov_hii_rain) for each station
station_ratios = hrdi_merged[hrdi_merged["rainfall_mm"].notna()].groupby("station_code").apply(
    lambda grp: grp["rainfall_mm"].sum() / np.maximum(grp["hii_prov_rain_mm"].sum(), 1.0)
).to_dict()

# Compute monthly climatology (mean, std) for temp, humidity, wind per station
clim_stats = hrdi_clean.groupby(["CODE_REF", "month"]).agg({
    "TEMP": ["mean", "std"],
    "TEMP_MIN": ["mean", "std"],
    "TEMP_MAX": ["mean", "std"],
    "HUMIDITY": ["mean", "std"],
    "WIND_SPEED": ["mean", "std"],
    "RAINDAY": ["mean", "std"]
})

completed_rows = []
for idx, row in hrdi_merged.iterrows():
    s_code = row["station_code"]
    yr = row["year"]
    mo = row["month"]
    rain = row["rainfall_mm"]
    temp = row["TEMP"]
    t_min = row["TEMP_MIN"]
    t_max = row["TEMP_MAX"]
    hum = row["HUMIDITY"]
    wind = row["WIND_SPEED"]
    rday = row["RAINDAY"]
    hii_rain = row["hii_prov_rain_mm"]

    # 1. Observed Data (genuine non-null reading)
    if pd.notna(rain):
        data_status = "observed"
        method = "direct_telemetry_observation"
        source = "data/raw/HRDI_meteo.csv"
        unc_low = rain
        unc_high = rain
        final_rain = rain
    else:
        # 2. Estimated vs Synthetic
        # Check if row has other climate telemetry (estimated) or is totally offline (synthetic)
        has_telemetry = pd.notna(temp) and pd.notna(hum)
        k_ratio = station_ratios.get(s_code, 1.0)
        # Bounded scaling
        k_ratio = np.clip(k_ratio, 0.4, 2.5)

        if has_telemetry:
            # Estimated: Missing rain, but telemetry active (e.g. Jan 2023 dry season)
            data_status = "estimated"
            method = "provincial_hii_ratio_interpolation"
            source = "data/raw/spatial-rain-hii.csv"
            # In dry season, HII rain is very small (0-10 mm)
            est_rain = round(float(hii_rain * k_ratio), 2)
            sigma = max(2.0, est_rain * 0.25)
            unc_low = max(0.0, round(est_rain - 1.96 * sigma, 2))
            unc_high = round(est_rain + 1.96 * sigma, 2)
            final_rain = est_rain
        else:
            # Synthetic: Station completely offline (e.g. Sep-Dec 2023)
            data_status = "synthetic"
            method = "spatial_hii_gamma_stochastic_scaling"
            source = "data/raw/spatial-rain-hii.csv + climatological_distribution"
            
            # Gamma stochastic perturbation with mean 1, CV = 0.18
            gamma_shape = 1.0 / (0.18 ** 2)
            gamma_scale = (0.18 ** 2)
            perturbation = np.random.gamma(gamma_shape, gamma_scale)
            syn_rain = round(float(hii_rain * k_ratio * perturbation), 2)
            sigma = max(5.0, syn_rain * 0.25)
            unc_low = max(0.0, round(syn_rain - 1.96 * sigma, 2))
            unc_high = round(syn_rain + 1.96 * sigma, 2)
            final_rain = syn_rain

    # Fill missing temperature, humidity, wind using climatological normal
    if pd.isna(temp):
        try:
            m_temp = clim_stats.loc[(s_code, mo), ("TEMP", "mean")]
            s_temp = clim_stats.loc[(s_code, mo), ("TEMP", "std")]
            s_temp = 1.0 if pd.isna(s_temp) or s_temp == 0 else s_temp
            temp = round(float(np.random.normal(m_temp, s_temp)), 2)
        except Exception:
            temp = 22.0
    if pd.isna(t_min):
        t_min = round(temp - np.random.uniform(2.5, 4.5), 2)
    if pd.isna(t_max):
        t_max = round(temp + np.random.uniform(2.5, 5.0), 2)
    if pd.isna(hum):
        try:
            m_hum = clim_stats.loc[(s_code, mo), ("HUMIDITY", "mean")]
            s_hum = clim_stats.loc[(s_code, mo), ("HUMIDITY", "std")]
            s_hum = 3.0 if pd.isna(s_hum) or s_hum == 0 else s_hum
            hum = round(float(np.clip(np.random.normal(m_hum, s_hum), 50.0, 95.0)), 2)
        except Exception:
            hum = 78.0
    if pd.isna(wind):
        try:
            m_wind = clim_stats.loc[(s_code, mo), ("WIND_SPEED", "mean")]
            wind = round(float(max(0.2, m_wind + np.random.normal(0, 0.3))), 2)
        except Exception:
            wind = 2.5
    if pd.isna(rday):
        if final_rain == 0:
            rday = 0
        else:
            rday = int(np.clip(round(final_rain / 12.0 + np.random.uniform(-1, 2)), 1, 30))

    completed_rows.append({
        "station_code": s_code,
        "station_name_th": row["station_name_th"],
        "province": row["province"],
        "amphoe": row["amphoe"],
        "tambon": row["tambon"],
        "tambon_code_6": row["tambon_code_6"],
        "lat": row["lat"],
        "long": row["long"],
        "year": yr,
        "month": mo,
        "rainfall_mm": final_rain,
        "temp_c": temp,
        "temp_min_c": t_min,
        "temp_max_c": t_max,
        "humidity_pct": hum,
        "wind_speed_ms": wind,
        "rainday_count": rday,
        "data_status": data_status,
        "imputation_method": method,
        "source_file": source,
        "uncertainty_range_lower": unc_low,
        "uncertainty_range_upper": unc_high
    })

hrdi_completed = pd.DataFrame(completed_rows)
assert len(hrdi_completed) == 1200
assert not hrdi_completed.duplicated(subset=["station_code", "year", "month"]).any()

hrdi_path = SYNTHETIC / "hrdi_completed_experimental.csv"
hrdi_completed.to_csv(hrdi_path, index=False, encoding="utf-8-sig")
print(f"Saved HRDI completed experimental dataset ({len(hrdi_completed)} rows): {hrdi_path}")
print("HRDI status breakdown:")
print(hrdi_completed["data_status"].value_counts())

print("\n=== STEP 4: RICE COMPLETED EXPERIMENTAL DATASET ===")
# Load normalized DOAE rice records
c22 = pd.read_csv(REPORTS / "crop_2022_normalized.csv", dtype=str)
c23 = pd.read_csv(REPORTS / "crop_2023_normalized.csv", dtype=str)

c22["prod_norm"] = c22["product_id"].astype(str).str.zfill(6)
c23["prod_norm"] = c23["product_id"].astype(str).str.zfill(6)

for c in ["area_plant", "area_harvest", "product_harvest"]:
    c22[c] = pd.to_numeric(c22[c], errors="coerce")
    c23[c] = pd.to_numeric(c23[c], errors="coerce")

# Filter wet season lowland rice (011000)
r22 = c22[(c22["code_valid"] == "True") & (c22["prod_norm"] == "011000")].copy()
r23 = c23[(c23["code_valid"] == "True") & (c23["prod_norm"] == "011000")].copy()

# Aggregate by tambon (2022 has multiple breed rows per tambon, 2023 has 1)
r22_agg = r22.groupby("tambon_code_6", as_index=False).agg({
    "area_plant": "sum",
    "area_harvest": "sum",
    "product_harvest": "sum"
})
r22_agg["year"] = 2022
r22_agg["yield_kg_per_rai"] = np.where(
    r22_agg["area_harvest"] > 0,
    r22_agg["product_harvest"] / r22_agg["area_harvest"],
    0.0
)
r22_agg["source_file"] = "data/raw/plant01_65.csv"

r23_agg = r23.groupby("tambon_code_6", as_index=False).agg({
    "area_plant": "sum",
    "area_harvest": "sum",
    "product_harvest": "sum"
})
r23_agg["year"] = 2023
r23_agg["yield_kg_per_rai"] = np.where(
    r23_agg["area_harvest"] > 0,
    r23_agg["product_harvest"] / r23_agg["area_harvest"],
    0.0
)
r23_agg["source_file"] = "data/raw/5.-01-2566.csv"

doae_observed = pd.concat([r22_agg, r23_agg], ignore_index=True)
doae_observed["data_status"] = "observed"
doae_observed["estimation_method"] = "official_doae_registration"
print(f"Total DOAE observed tambon-year records: {len(doae_observed)}")

# Build comprehensive rice grid for all 921 tambons x 2 years = 1,842 rows
rice_grid = []
for _, tb in geo_df.iterrows():
    for yr in [2022, 2023]:
        rice_grid.append({
            "year": yr,
            "geo_province_code": tb["geo_province_code"],
            "geo_province_name": tb["geo_province_name"],
            "geo_amphoe_code": tb["geo_amphoe_code"],
            "geo_amphoe_name": tb["geo_amphoe_name"],
            "tambon_code_6": tb["geo_tambon_code_6"],
            "tambon_name": tb["geo_tambon_name"]
        })
rice_grid_df = pd.DataFrame(rice_grid)

# Merge grid with DOAE observed
rice_merged = rice_grid_df.merge(
    doae_observed[[
        "tambon_code_6", "year", "area_plant", "area_harvest",
        "product_harvest", "yield_kg_per_rai", "data_status",
        "estimation_method", "source_file"
    ]],
    on=["tambon_code_6", "year"],
    how="left"
)

# Merge HRDI station presence flag
station_tambon_map = linkage_df[linkage_df["geo_tambon_code_6"].notna()].set_index("geo_tambon_code_6")["station_code"].to_dict()
rice_merged["matched_hrdi_station"] = rice_merged["tambon_code_6"].map(station_tambon_map)
rice_merged["has_hrdi_station"] = rice_merged["matched_hrdi_station"].notna()

# Compute empirical provincial yield distribution parameters (mean, std) for synthesis
prov_yield_stats = doae_observed[doae_observed["yield_kg_per_rai"] > 0].merge(
    geo_df[["geo_tambon_code_6", "geo_province_name"]],
    left_on="tambon_code_6", right_on="geo_tambon_code_6", how="left"
).groupby(["geo_province_name", "year"])["yield_kg_per_rai"].agg(["mean", "std", "median"]).to_dict("index")

rice_completed_rows = []
for _, row in rice_merged.iterrows():
    yr = row["year"]
    t_code = row["tambon_code_6"]
    p_name = row["geo_province_name"]
    st_code = row["matched_hrdi_station"]
    has_st = row["has_hrdi_station"]

    if pd.notna(row["area_plant"]):
        # Observed DOAE
        status = "observed"
        method = "official_doae_registration"
        source = row["source_file"]
        p_area = round(float(row["area_plant"]), 2)
        h_area = round(float(row["area_harvest"]), 2)
        prod = round(float(row["product_harvest"]), 2)
        yield_val = round(float(row["yield_kg_per_rai"]), 2)
        unc_low = yield_val
        unc_high = yield_val
    else:
        # Synthetic simulation for experimental/pipeline testing
        status = "synthetic"
        method = "provincial_empirical_parametric_sampling"
        source = "synthetic_monte_carlo_distribution (NOT_DOAE)"

        # Sample yield from provincial distribution
        stats = prov_yield_stats.get((p_name, yr), {"mean": 550.0, "std": 90.0})
        m_y = stats["mean"] if pd.notna(stats["mean"]) else 550.0
        s_y = stats["std"] if pd.notna(stats["std"]) and stats["std"] > 0 else 85.0
        # Draw from truncated normal between 250 and 1000 kg/rai
        raw_draw = np.random.normal(m_y, s_y)
        yield_val = round(float(np.clip(raw_draw, 250.0, 950.0)), 2)
        
        # Synthetic area
        p_area = round(float(np.random.uniform(300.0, 3500.0)), 2)
        h_area = round(float(p_area * np.random.uniform(0.92, 0.99)), 2)
        prod = round(float(h_area * yield_val), 2)
        unc_low = round(max(200.0, yield_val - 1.96 * s_y), 2)
        unc_high = round(min(1100.0, yield_val + 1.96 * s_y), 2)

    rice_completed_rows.append({
        "year": yr,
        "province_code": row["geo_province_code"],
        "province_name": p_name,
        "amphoe_code": row["geo_amphoe_code"],
        "amphoe_name": row["geo_amphoe_name"],
        "tambon_code_6": t_code,
        "tambon_name": row["tambon_name"],
        "has_hrdi_station": has_st,
        "matched_hrdi_station_code": st_code if pd.notna(st_code) else "NONE",
        "crop_type": "wet_season_lowland_rice_011000",
        "plant_area_rai": p_area,
        "harvest_area_rai": h_area,
        "production_kg": prod,
        "yield_kg_per_rai": yield_val,
        "data_status": status,
        "estimation_method": method,
        "source_file": source,
        "uncertainty_range_lower": unc_low,
        "uncertainty_range_upper": unc_high
    })

rice_completed = pd.DataFrame(rice_completed_rows)
assert len(rice_completed) == 921 * 2  # Exactly 1,842 rows
assert not rice_completed.duplicated(subset=["tambon_code_6", "year"]).any()

rice_path = SYNTHETIC / "rice_completed_experimental.csv"
rice_completed.to_csv(rice_path, index=False, encoding="utf-8-sig")
print(f"Saved Rice completed experimental dataset ({len(rice_completed)} rows): {rice_path}")
print("Rice status breakdown:")
print(rice_completed["data_status"].value_counts())

print("\n=== STEP 5: VERIFY INTEGRITY OF OBSERVED VALUES ===")
# Check that observed values in synthetic outputs exactly match original processed/raw values!
# 1. HII check
hii_orig_sub = df_hii_raw[
    (df_hii_raw["YEAR"].isin([2022, 2023])) &
    (df_hii_raw["PROV_T"].isin(linkage_df["geo_province_name"].unique()))
].set_index(["YEAR", "MONTH", "PROV_T"])["AvgRain"]
hii_comp_sub = hii_completed.set_index(["year", "month", "province_name_th"])["avg_rain_mm"]
assert np.allclose(hii_orig_sub.values, hii_comp_sub.values, equal_nan=True)
print("HII observed values integrity check: 100% MATCH.")

# 2. HRDI check
hrdi_clean_val = hrdi_clean[hrdi_clean["rainfall_mm"].notna()].set_index(["CODE_REF", "year", "month"])["rainfall_mm"]
hrdi_comp_val = hrdi_completed[hrdi_completed["data_status"] == "observed"].set_index(["station_code", "year", "month"])["rainfall_mm"]
# Check matching index
common_idx = hrdi_clean_val.index.intersection(hrdi_comp_val.index)
assert len(common_idx) == 976
assert np.allclose(hrdi_clean_val.loc[common_idx].values, hrdi_comp_val.loc[common_idx].values)
print("HRDI observed values integrity check: 100% MATCH (976 station-months).")

# 3. Rice check
doae_obs_val = doae_observed.set_index(["tambon_code_6", "year"])["yield_kg_per_rai"]
rice_comp_val = rice_completed[rice_completed["data_status"] == "observed"].set_index(["tambon_code_6", "year"])["yield_kg_per_rai"]
common_rice_idx = doae_obs_val.index.intersection(rice_comp_val.index)
assert len(common_rice_idx) == len(doae_obs_val)
assert np.allclose(doae_obs_val.loc[common_rice_idx].values, rice_comp_val.loc[common_rice_idx].values, atol=0.01)
print(f"Rice observed values integrity check: 100% MATCH ({len(doae_obs_val)} tambon-years).")

print("\n=== SCRIPT 50 FINISHED SUCCESSFULLY ===")
