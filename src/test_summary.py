import pandas as pd
import json
from pathlib import Path
from dashboard.data_loader import load_climate_data, PROVINCE_NAMES

c = load_climate_data()
h50 = pd.read_csv('data/completeness/hrdi_all_50_stations_24_months_DEMO.csv')
hii = pd.read_csv('data/completeness/hii_all_9_provinces_24_months.csv')
r921 = pd.read_csv('data/completeness/rice_all_921_tambons_2022_2023.csv')

p_centers = {
    'เชียงใหม่': {'lat': 18.7904, 'lng': 98.9847, 'zoom': 8.5, 'code': '50'},
    'เชียงราย': {'lat': 19.9072, 'lng': 99.8325, 'zoom': 8.5, 'code': '57'},
    'น่าน': {'lat': 18.7756, 'lng': 100.7730, 'zoom': 8.5, 'code': '55'},
    'ตาก': {'lat': 16.8840, 'lng': 99.1258, 'zoom': 8.0, 'code': '63'},
    'กำแพงเพชร': {'lat': 16.4828, 'lng': 99.5227, 'zoom': 8.5, 'code': '62'},
    'พิษณุโลก': {'lat': 16.8211, 'lng': 100.2659, 'zoom': 8.5, 'code': '65'},
    'เพชรบูรณ์': {'lat': 16.4190, 'lng': 101.1567, 'zoom': 8.5, 'code': '67'},
    'กาญจนบุรี': {'lat': 14.3000, 'lng': 99.1000, 'zoom': 8.0, 'code': '71'},
    'แม่ฮ่องสอน': {'lat': 19.3021, 'lng': 97.9654, 'zoom': 8.5, 'code': '58'},
}

sta_meta = c.groupby('STA_TH')[['province_clean', 'LAT', 'LONG', 'AMPHOE', 'TAMBON', 'CODE_REF', 'CODE_STA', 'source_type', 'TEMP', 'HUMIDITY', 'WIND_SPEED']].first().to_dict(orient='index')

prov_summaries = {}
for prov_name in p_centers:
    c_p = c[c['province_clean'] == prov_name]
    h_p = h50[h50['PROVINCE'] == prov_name]
    hii_p = hii[hii['province_name_th'] == prov_name]
    r_p = r921[r921['province_name'] == prov_name]
    
    stas_in_p = sorted(h_p['STA_TH'].unique().tolist())
    sta_cnt = len(stas_in_p)
    
    hii_22 = float(hii_p[hii_p['year'] == 2022]['avg_rain_mm'].sum()) if len(hii_p) > 0 else 0.0
    hii_23 = float(hii_p[hii_p['year'] == 2023]['avg_rain_mm'].sum()) if len(hii_p) > 0 else 0.0
    hii_chg = hii_23 - hii_22
    
    h22_demo = float(h_p[h_p['YEAR'] == 2022]['rainfall_for_demo_mm'].mean() * 12) if len(h_p) > 0 else 0.0
    h23_demo = float(h_p[h_p['YEAR'] == 2023]['rainfall_for_demo_mm'].mean() * 12) if len(h_p) > 0 else 0.0
    
    r22_mean = r_p[r_p['year'] == 2022]['yield_kg_per_rai'].mean()
    r23_mean = r_p[r_p['year'] == 2023]['yield_kg_per_rai'].mean()
    
    temp_avg = float(c_p['TEMP'].mean()) if len(c_p) > 0 and c_p['TEMP'].notna().sum() > 0 else 0.0
    hum_avg = float(c_p['HUMIDITY'].mean()) if len(c_p) > 0 and c_p['HUMIDITY'].notna().sum() > 0 else 0.0
    wind_avg = float(c_p['WIND_SPEED'].mean()) if len(c_p) > 0 and c_p['WIND_SPEED'].notna().sum() > 0 else 0.0
    
    prov_summaries[prov_name] = {
        'name': prov_name,
        'station_count': sta_cnt,
        'stations': stas_in_p,
        'rain_all': round((h22_demo + h23_demo) / 2, 1),
        'rain_2022': round(h22_demo, 1),
        'rain_2023': round(h23_demo, 1),
        'hii_rain_2022': round(hii_22, 1),
        'hii_rain_2023': round(hii_23, 1),
        'hii_change': round(hii_chg, 1),
        'rice_yield_2022': round(float(r22_mean), 1) if pd.notna(r22_mean) else None,
        'rice_yield_2023': round(float(r23_mean), 1) if pd.notna(r23_mean) else None,
        'temp': round(temp_avg, 1),
        'humidity': round(hum_avg, 1),
        'wind': round(wind_avg, 2),
        'tambon_count': int(r_p['tambon_code_6'].nunique())
    }

print('All 9 province summaries generated cleanly!')
for p, s in prov_summaries.items():
    print(f"{p}: stas={s['station_count']}, tambons={s['tambon_count']}, hii22={s['hii_rain_2022']}, rice22={s['rice_yield_2022']}")
