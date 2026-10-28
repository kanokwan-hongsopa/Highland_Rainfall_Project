# -*- coding: utf-8 -*-
"""
Export dashboard เป็นเว็บ static สำหรับ GitHub Pages (ไม่ต้องรัน Streamlit)
ผลลัพธ์: docs/index.html (ฝังข้อมูล JSON ไว้ในไฟล์) + docs/.nojekyll

รันใหม่ทุกครั้งที่ข้อมูลหรือหน้าตา dashboard เปลี่ยน:
    .venv\\Scripts\\python.exe scripts/export_github_pages.py
"""
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dashboard.halloween_app import get_halloween_html

out_dir = BASE_DIR / "docs"
out_dir.mkdir(exist_ok=True)
html_content = get_halloween_html()
(out_dir / "index.html").write_text(html_content, encoding="utf-8")
(out_dir / ".nojekyll").write_text("", encoding="utf-8")

print(f"Exported GitHub Pages site to {out_dir / 'index.html'} ({len(html_content):,} bytes)")
