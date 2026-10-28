# -*- coding: utf-8 -*-
"""
Script to apply Exploratory & Observed Only Dual-Mode Upgrades to dashboard/halloween_app.py
"""

from pathlib import Path
import re

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------------
# 1. ADD CSS FOR HRDI DUAL-MODE SWITCHER (BEFORE </style>)
# -------------------------------------------------------------------------
mode_css = """
        /* HRDI MODE SWITCHER (OBSERVED ONLY VS EXPLORATORY 12M) */
        .hrdi-mode-bar-container {{
            background: linear-gradient(135deg, rgba(33, 22, 49, 0.95), rgba(20, 11, 36, 0.95));
            border: 1px solid rgba(167, 120, 232, 0.35);
            border-radius: 12px;
            padding: 0.9rem 1.25rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45);
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}

        .hrdi-mode-switch-wrapper {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .hrdi-mode-label-group {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .hrdi-mode-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .hrdi-mode-tag {{
            font-size: 0.75rem;
            color: var(--accent-lavender);
            font-weight: 500;
        }}

        .hrdi-mode-toggle-group {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}

        .mode-toggle-btn {{
            background: rgba(43, 28, 66, 0.7);
            border: 1px solid rgba(167, 120, 232, 0.25);
            border-radius: 8px;
            padding: 0.55rem 0.95rem;
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.65rem;
            transition: all 0.25s ease;
            text-align: left;
            font-family: var(--font-family);
        }}

        .mode-toggle-btn:hover {{
            background: rgba(58, 38, 88, 0.85);
            border-color: rgba(167, 120, 232, 0.5);
            color: #ffffff;
            transform: translateY(-1px);
        }}

        .mode-toggle-btn.active#btnModeObserved {{
            background: linear-gradient(135deg, rgba(167, 120, 232, 0.25), rgba(139, 92, 246, 0.15));
            border-color: #A778E8;
            color: #ffffff;
            box-shadow: 0 0 14px rgba(167, 120, 232, 0.35);
        }}

        .mode-toggle-btn.active#btnModeExploratory {{
            background: linear-gradient(135deg, rgba(255, 138, 50, 0.25), rgba(249, 115, 22, 0.15));
            border-color: #FF8A32;
            color: #ffffff;
            box-shadow: 0 0 14px rgba(255, 138, 50, 0.35);
        }}

        .mode-toggle-btn .mode-icon {{
            font-size: 1.3rem;
        }}

        .mode-btn-content {{
            display: flex;
            flex-direction: column;
            gap: 1px;
        }}

        .mode-name {{
            font-size: 0.82rem;
            font-weight: 600;
        }}

        .mode-hint {{
            font-size: 0.68rem;
            opacity: 0.8;
        }}

        .hrdi-mode-status-banner {{
            border-radius: 8px;
            padding: 0.6rem 0.95rem;
            font-size: 0.78rem;
            line-height: 1.45;
            display: flex;
            align-items: center;
            gap: 0.65rem;
            transition: all 0.25s ease;
        }}

        .hrdi-mode-status-banner.banner-observed {{
            background: rgba(167, 120, 232, 0.1);
            border-left: 4px solid #A778E8;
            color: #E2D9F3;
        }}

        .hrdi-mode-status-banner.banner-exploratory {{
            background: rgba(255, 138, 50, 0.12);
            border-left: 4px solid #FF8A32;
            color: #FFE8D6;
        }}

        .hrdi-mode-status-banner .banner-icon {{
            font-size: 1.1rem;
            flex-shrink: 0;
        }}
"""

if ".hrdi-mode-bar-container" not in content:
    target_css_end = "        .leaflet-prov-label {{\n            background: transparent !important;\n            border: none !important;\n            box-shadow: none !important;\n            color: #ffffff !important;\n            font-family: var(--font-family) !important;\n            font-weight: 600 !important;\n            font-size: 0.82rem !important;\n            text-shadow: 0 1px 4px #000, 0 0 8px #000, 0 0 12px #000;\n            pointer-events: none;\n        }}\n    </style>"
    replacement_css = "        .leaflet-prov-label {{\n            background: transparent !important;\n            border: none !important;\n            box-shadow: none !important;\n            color: #ffffff !important;\n            font-family: var(--font-family) !important;\n            font-weight: 600 !important;\n            font-size: 0.82rem !important;\n            text-shadow: 0 1px 4px #000, 0 0 8px #000, 0 0 12px #000;\n            pointer-events: none;\n        }}\n" + mode_css + "\n    </style>"
    if target_css_end in content:
        content = content.replace(target_css_end, replacement_css)
        print("[SUCCESS] Added Mode CSS")
    else:
        print("[WARNING] Could not match target_css_end")

# -------------------------------------------------------------------------
# 2. ADD MODE SWITCHER HTML (AFTER </nav>)
# -------------------------------------------------------------------------
mode_html = """        <!-- HRDI DUAL ANALYSIS MODE SWITCHER (STICKY / TOP BAR) -->
        <div class="hrdi-mode-bar-container" id="hrdiModeBar">
            <div class="hrdi-mode-switch-wrapper">
                <div class="hrdi-mode-label-group">
                    <span class="hrdi-mode-title">🔬 โหมดข้อมูลฝน HRDI</span>
                    <span class="hrdi-mode-tag" id="hrdiCurrentModeTag">โหมดปัจจุบัน: ตรวจวัดจริง (Observed Only)</span>
                </div>
                <div class="hrdi-mode-toggle-group">
                    <button type="button" id="btnModeObserved" class="mode-toggle-btn active" data-mode="observed">
                        <span class="mode-icon">🧪</span>
                        <div class="mode-btn-content">
                            <span class="mode-name">ตรวจวัดจริงเท่านั้น (Observed Only)</span>
                            <span class="mode-hint">แสดงเฉพาะเดือนที่วัดจริง • ไม่แสดงผลรวมสถานีที่ไม่ครบ 12 ด.</span>
                        </div>
                    </button>
                    <button type="button" id="btnModeExploratory" class="mode-toggle-btn" data-mode="exploratory">
                        <span class="mode-icon">🔮</span>
                        <div class="mode-btn-content">
                            <span class="mode-name">ทดลองวิเคราะห์ (Exploratory 12 ด.)</span>
                            <span class="mode-hint">เติมเต็ม 12 เดือนด้วยสถิติ • มีป้ายเตือนค่าประมาณการ</span>
                        </div>
                    </button>
                </div>
            </div>
            <div id="hrdiModeBanner" class="hrdi-mode-status-banner banner-observed">
                <span class="banner-icon" id="hrdiBannerIcon">🛡️</span>
                <span class="banner-text" id="hrdiModeBannerText"><strong>โหมดข้อมูลตรวจวัดจริง (Observed Only):</strong> แสดงเฉพาะข้อมูลจริงจากเซ็นเซอร์ HRDI รายเดือน (เดือนที่ไม่มีข้อมูลแสดงเป็นช่องว่าง ห้ามนำไปคิดเป็นศูนย์ และห้ามแสดงผลรวมทั้งปีสำหรับสถานีที่ข้อมูลไม่ครบ 12 เดือน)</span>
            </div>
        </div>
"""

nav_end_str = """        </nav>

        <!-- ====================================================================
             PAGE 1: OVERVIEW & STATION EXPLORER
             ==================================================================== -->"""

if "id=\"hrdiModeBar\"" not in content:
    if nav_end_str in content:
        content = content.replace(nav_end_str, "        </nav>\n\n" + mode_html + "\n        <!-- ====================================================================\n             PAGE 1: OVERVIEW & STATION EXPLORER\n             ==================================================================== -->")
        print("[SUCCESS] Added Mode Switcher HTML")
    else:
        print("[WARNING] Could not match nav_end_str")

# Add id="tab1_kpiRainSub" to the rain subtext
target_rain_sub = """                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiRain">1,842.6</div>
                        <span class="kpi-delta-pill kpi-delta-up" id="tab1_kpiRainBadge">▲ 8.3%</span>
                    </div>
                    <div class="kpi-subtext">ฝนสะสมเฉลี่ยบนพื้นที่สูง</div>"""

replacement_rain_sub = """                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiRain">1,842.6</div>
                        <span class="kpi-delta-pill kpi-delta-up" id="tab1_kpiRainBadge">✓ 12/12 ด.</span>
                    </div>
                    <div class="kpi-subtext" id="tab1_kpiRainSub">ข้อมูลตรวจวัดจริงครบ 12 เดือน</div>"""

if target_rain_sub in content:
    content = content.replace(target_rain_sub, replacement_rain_sub)
    print("[SUCCESS] Updated Tab 1 Rain KPI Subtext HTML")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] First pass HTML & CSS upgrade saved.")
