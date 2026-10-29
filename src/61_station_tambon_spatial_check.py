"""
ตรวจพิกัดสถานี HRDI กับขอบเขตตำบลจริง (Spatial Join) — ใช้พิกัดจากไฟล์ HRDI เท่านั้น ไม่สมมติพิกัด

ที่มาขอบเขต: OpenGISData-Thailand subdistricts.geojson (ไม่แก้ไฟล์ต้นฉบับ)
ใช้งาน: python src/61_station_tambon_spatial_check.py <path/to/subdistricts.geojson>
ผลลัพธ์:
  data/analysis_ready/station_tambon_spatial_check.csv  (ทุกสถานี + คู่สถานี–ตำบลใน Balanced Panel)
  data/reference/panel_tambons_simplified.geojson        (ขอบเขต 26 ตำบลใน panel สำหรับแผนที่ dashboard)
"""
from pathlib import Path
import csv
import importlib.util
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
LINK = ROOT / "data" / "analysis_ready" / "geographic_linkage_verified.csv"
PANEL = ROOT / "data" / "analysis_ready" / "rice_hrdi_tambon_panel_observed.csv"
OUT_CSV = ROOT / "data" / "analysis_ready" / "station_tambon_spatial_check.csv"
OUT_GEO = ROOT / "data" / "reference" / "panel_tambons_simplified.geojson"
EXCLUDED_TAMBONS = {"500109"}  # ตัดออกจาก panel (สถานี RPF ฝน 0 ทั้งฤดู) — ตรงกับ src/59

# ใช้ตัวย่อเส้นตัวเดียวกับ src/60
_spec = importlib.util.spec_from_file_location("simplify60", ROOT / "src" / "60_simplify_thailand_provinces.py")
_s60 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_s60)


def in_ring(x, y, ring):
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def in_multipolygon(x, y, mp):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in mp)


def dist_to_boundary_km(x, y, mp):
    """ระยะสั้นที่สุดจากจุดถึงเส้นขอบ (กม.) ด้วยการฉายแบบ equirectangular รอบจุด"""
    kx, ky = 111.32 * math.cos(math.radians(y)), 110.57
    best = float("inf")
    for p in mp:
        for ring in p:
            for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
                ax, ay, bx, by = (x1 - x) * kx, (y1 - y) * ky, (x2 - x) * kx, (y2 - y) * ky
                dx, dy = bx - ax, by - ay
                t = 0 if dx == dy == 0 else max(0, min(1, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
                best = min(best, math.hypot(ax + t * dx, ay + t * dy))
    return best


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def status_of(inside, edge_km):
    if inside:
        return "inside"
    return "near_edge" if edge_km <= 5 else "outside_far"


def main(sub_path):
    tam = {f["properties"]["tam_code"]: f for f in json.loads(Path(sub_path).read_text(encoding="utf-8"))["features"]}
    link = list(csv.DictReader(LINK.open(encoding="utf-8-sig")))
    stations = {r["station_code"].strip(): r for r in link}

    def containing_tambon(r):
        x, y = float(r["station_lon"]), float(r["station_lat"])
        prov = str(r["geo_province_code"]).split(".")[0]
        return next((c for c, f in tam.items() if f["properties"]["pro_code"] == prov
                     and in_multipolygon(x, y, f["geometry"]["coordinates"])), None)

    actual = {code: containing_tambon(r) for code, r in stations.items()}

    # คู่สถานี–ตำบลใน Balanced Panel
    pairs, seen = [], set()
    for r in csv.DictReader(PANEL.open(encoding="utf-8-sig")):
        t = r["tambon_code_6"]
        if t in EXCLUDED_TAMBONS or t in seen:
            continue
        seen.add(t)
        for c in (c.strip() for c in re.split(r"[,;]", r["station_codes"]) if c.strip()):
            pairs.append((t, c))
    assert len(seen) == 26, len(seen)

    rows = []
    for t, c in pairs:
        f, s = tam[t], stations[c]
        x, y = float(s["station_lon"]), float(s["station_lat"])
        inside = in_multipolygon(x, y, f["geometry"]["coordinates"])
        edge = 0.0 if inside else dist_to_boundary_km(x, y, f["geometry"]["coordinates"])
        act = actual[c]
        rows.append({
            "scope": "panel_pair",
            "tambon_code_6": t,
            "tambon_name": f["properties"]["tam_th"],
            "amphoe_name": f["properties"]["amp_th"],
            "province_name": f["properties"]["pro_th"],
            "station_code": c,
            "station_name": s["station_name_th"].replace("สถานีตรวจวัดสภาพอากาศ", "").strip(),
            "station_lat": y,
            "station_lon": x,
            "inside_matched_tambon": inside,
            "distance_to_boundary_km": round(edge, 2),
            "distance_to_tambon_centroid_km": round(haversine_km(y, x, f["properties"]["lat"], f["properties"]["lon"]), 1),
            "tambon_area_sqkm": round(f["properties"]["area_sqkm"], 1),
            "actual_tambon_code_6": act or "",
            "actual_tambon_name": tam[act]["properties"]["tam_th"] if act else "",
            "status": status_of(inside, edge),
        })
    for c, s in stations.items():
        exp = str(s["geo_tambon_code_6"]).split(".")[0]
        act = actual[c]
        rows.append({
            "scope": "all_stations",
            "tambon_code_6": exp if exp not in ("", "nan") else "",
            "tambon_name": s["geo_tambon_name"],
            "amphoe_name": s["geo_amphoe_name"],
            "province_name": s["geo_province_name"],
            "station_code": c,
            "station_name": s["station_name_th"].replace("สถานีตรวจวัดสภาพอากาศ", "").strip(),
            "station_lat": float(s["station_lat"]),
            "station_lon": float(s["station_lon"]),
            "inside_matched_tambon": act == exp,
            "distance_to_boundary_km": "",
            "distance_to_tambon_centroid_km": "",
            "tambon_area_sqkm": "",
            "actual_tambon_code_6": act or "",
            "actual_tambon_name": tam[act]["properties"]["tam_th"] if act else "",
            "status": "inside" if act == exp else ("no_recorded_tambon" if exp in ("", "nan") else "different_tambon"),
        })

    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    feats = []
    for t in sorted(seen):
        f = tam[t]
        polys = []
        for poly in f["geometry"]["coordinates"]:
            rings = [r for r in (_s60.simplify_ring(r) for r in poly) if r]
            if rings:
                polys.append(rings)
        p = f["properties"]
        feats.append({"type": "Feature",
                      "properties": {"tam_code": t, "tam_th": p["tam_th"], "amp_th": p["amp_th"], "pro_th": p["pro_th"]},
                      "geometry": {"type": "MultiPolygon", "coordinates": polys}})
    OUT_GEO.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False,
                                  separators=(",", ":")), encoding="utf-8")

    pr = [r for r in rows if r["scope"] == "panel_pair"]
    print(f"panel pairs={len(pr)} inside={sum(r['status'] == 'inside' for r in pr)} "
          f"near_edge(<=5km)={sum(r['status'] == 'near_edge' for r in pr)} outside_far={sum(r['status'] == 'outside_far' for r in pr)}")
    al = [r for r in rows if r["scope"] == "all_stations"]
    print(f"all stations={len(al)} inside recorded tambon={sum(r['status'] == 'inside' for r in al)}")
    print(f"-> {OUT_CSV}\n-> {OUT_GEO} ({OUT_GEO.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main(sys.argv[1])
