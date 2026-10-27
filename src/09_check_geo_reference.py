
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "data" / "reference" / "geo.json"

print("===== CHECK GEO.JSON =====")
print("พบไฟล์:", FILE.exists())

if not FILE.exists():
    raise FileNotFoundError(FILE)

print("ขนาดไฟล์:", FILE.stat().st_size, "bytes")

with open(FILE, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

print("\n===== JSON STRUCTURE =====")
print("ชนิดข้อมูล:", type(data).__name__)

if isinstance(data, dict):
    print("คีย์ระดับบน:", list(data.keys())[:20])

    for key, value in list(data.items())[:2]:
        print(f"\nตัวอย่างคีย์: {key}")
        print(json.dumps(
            value, ensure_ascii=False, indent=2
        )[:1500])

elif isinstance(data, list):
    print("จำนวนรายการ:", len(data))
    print("\nตัวอย่างข้อมูล:")
    print(json.dumps(
        data[:2], ensure_ascii=False, indent=2
    )[:2000])
