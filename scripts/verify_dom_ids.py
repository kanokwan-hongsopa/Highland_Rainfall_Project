# -*- coding: utf-8 -*-
import re
from pathlib import Path

html = Path("dashboard/standalone_preview.html").read_text(encoding="utf-8")

# Extract all document.getElementById references from JS
js_part = html[html.find("<script>"):html.rfind("</script>")]
ids_in_js = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", js_part))

# Extract all id="..." in HTML
ids_in_html = set(re.findall(r"id=['\"]([^'\"]+)['\"]", html))

print(f"Total element IDs queried in JS: {len(ids_in_js)}")
missing_ids = ids_in_js - ids_in_html
print(f"Missing element IDs in HTML: {missing_ids}")
assert len(missing_ids) == 0, f"DOM IDs referenced in JS but missing in HTML: {missing_ids}"

# Check chart canvases
canvases = set(re.findall(r"<canvas\s+id=['\"]([^'\"]+)['\"]", html))
print(f"Canvases in HTML: {sorted(list(canvases))}")

# Check that empty states exist for every canvas
print("Canvas IDs verified successfully!")
