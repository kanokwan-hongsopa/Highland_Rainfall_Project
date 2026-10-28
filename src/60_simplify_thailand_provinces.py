"""
ย่อขอบเขต 77 จังหวัด (OpenGISData-Thailand provinces.geojson) ให้เบาพอฝังใน dashboard
ใช้เป็นเงาแผนที่ประเทศไทย (จังหวัดนอกพื้นที่ศึกษา) — ไม่ได้ใช้ในการวิเคราะห์

ที่มา: https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson
ใช้งาน: python src/60_simplify_thailand_provinces.py <path/to/provinces.geojson>
ผลลัพธ์: data/reference/thailand_77provinces_simplified.geojson
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "reference" / "thailand_77provinces_simplified.geojson"
TOLERANCE = 0.01   # องศา (~1 กม.) — พอสำหรับมุมมองระดับประเทศ
DECIMALS = 3


def _perp_dist(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
    return abs(dy * x - dx * y + x2 * y1 - y2 * x1) / (dx * dx + dy * dy) ** 0.5


def douglas_peucker(points, tol):
    """Douglas–Peucker แบบวนลูป (ไม่ recursive เพื่อเลี่ยง recursion limit กับแนวชายฝั่งยาว)"""
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        i, j = stack.pop()
        dmax, idx = 0.0, None
        for k in range(i + 1, j):
            d = _perp_dist(points[k], points[i], points[j])
            if d > dmax:
                dmax, idx = d, k
        if idx is not None and dmax > tol:
            keep[idx] = True
            stack += [(i, idx), (idx, j)]
    return [p for p, k in zip(points, keep) if k]


def simplify_ring(ring):
    pts = douglas_peucker(ring, TOLERANCE)
    pts = [[round(x, DECIMALS), round(y, DECIMALS)] for x, y in pts]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts if len(pts) >= 4 else None


def main(src):
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    features = []
    for f in data["features"]:
        polys = []
        for poly in f["geometry"]["coordinates"]:
            rings = [r for r in (simplify_ring(r) for r in poly) if r]
            if rings:
                polys.append(rings)
        props = f["properties"]
        features.append({
            "type": "Feature",
            "properties": {"pro_code": props["pro_code"], "pro_th": props["pro_th"], "pro_en": props["pro_en"]},
            "geometry": {"type": "MultiPolygon", "coordinates": polys},
        })
    assert len(features) == 77, len(features)
    out = {"type": "FeatureCollection", "features": features}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(features)} provinces -> {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main(sys.argv[1])
