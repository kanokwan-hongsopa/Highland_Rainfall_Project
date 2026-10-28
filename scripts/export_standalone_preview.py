# -*- coding: utf-8 -*-
from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_app import get_halloween_html

html_content = get_halloween_html()
out_path = BASE_DIR / "dashboard" / "standalone_preview.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Exported standalone preview to {out_path} ({len(html_content):,} bytes)")
