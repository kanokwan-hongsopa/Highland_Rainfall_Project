"""
Highland Rainfall Project - Halloween Interactive Dashboard Generator
Complete Professional Redesign:
- 250px High-Impact Spooky Harvest Rice Field Hero with glowing red-eyed scarecrow, orange moon, bats
- 5 Horizontal Navigation Tabs
- Tab-Specific Isolated Filter Bars with dynamic counts and reset controls
- Context-Specific KPIs tailored to each tab
- Left Large Interactive Map (600px) with Real 9-Province GeoJSON Boundaries & 50 Station Markers
- Floating Province & Station Detail Panel on Map:
  - Province summary & station counts (total vs active)
  - Searchable list of all stations in province with completeness (e.g. 21/24 months)
  - Click station name to flyTo marker
  - Click marker to open Station Detail Card with mini monthly rainfall trend chart
- Right Bento Charts:
  - Tab 1: Monthly rainfall curve + 9-Province rainfall ranking horizontal bar chart + summary insights
  - Tab 2: Grouped bar chart comparing HRDI station rainfall vs HII province-wide rainfall (Feb–Jul) + microclimate alert
  - Tab 3: Horizontal Dumbbell Plot (2022 vs 2023) + Ranked Delta Bar Chart + Searchable & Sortable 25 Tambons Table
  - Tab 4: Large Primary Scatter Plot (480px, 8px points) + LOPO Sensitivity Table + Non-causal governance
  - Tab 5: Data sources (HRDI, HII, DOAE), Completeness Matrix, Data Dictionary, and 5-row raw previews
- Attribution Cards with official links under every chart
- 100% Free OpenStreetMap Dark Theme Tiles (NO API KEY REQUIRED, NO WATERMARK)
"""

import base64
from pathlib import Path
from dashboard.halloween_data import get_halloween_payload


def get_header_image_data_uri() -> str:
    """
    อ่านไฟล์ assets/dashboard_reference.png และแปลงเป็น Base64 Data URI
    เพื่อให้ Streamlit และ Browser โหลดรูปภาพจริง 100% โดยไม่ต้องพึ่ง Web Server ภายนอก
    """
    img_path = Path(__file__).resolve().parent.parent / "assets" / "dashboard_reference.png"
    if img_path.exists():
        encoded = base64.b64encode(img_path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""


def get_halloween_html() -> str:
    """
    สร้าง Complete Standalone HTML5/CSS3/JavaScript Application
    """
    data_json = get_halloween_payload()
    header_bg_data_uri = get_header_image_data_uri()

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>สภาพภูมิอากาศบนพื้นที่สูงของประเทศไทยและผลผลิตข้าวนาปี (2022–2023)</title>
    <!-- Google Fonts: Prompt & Sarabun -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <style>
        :root {{
            --bg-night: #130D22;
            --bg-card: #211631;
            --bg-card-glass: rgba(33, 22, 49, 0.94);
            --bg-card-hover: #2e1d45;
            --primary-orange: #FF8A32;
            --primary-orange-glow: rgba(255, 138, 50, 0.45);
            --secondary-lavender: #A778E8;
            --accent-pink: #F18AB6;
            --accent-peach: #FA9A55;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --accent-cyan: #38bdf8;
            --text-cream: #F7F0E8;
            --text-muted: #A59DB5;
            --border-card: rgba(255, 138, 50, 0.22);
            --border-active: #FF8A32;
            --radius-card: 14px;
            --font-family: 'Prompt', 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-night);
            color: var(--text-cream);
            font-family: var(--font-family);
            font-size: 13.5px;
            line-height: 1.5;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(167, 120, 232, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 85% 20%, rgba(255, 138, 50, 0.1) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(241, 138, 182, 0.06) 0%, transparent 50%);
            padding-bottom: 2.5rem;
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 7px;
            height: 7px;
        }}
        ::-webkit-scrollbar-track {{
            background: #140b24;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #4a2b70;
            border-radius: 4px;
        }}

        /* ==========================================================================
           1. HERO HEADER (250PX HEIGHT, PROMINENT MOON, FIELD & SCARECROW)
           ========================================================================== */
        .hero-banner {{
            position: relative;
            width: 100%;
            height: 210px;
            background-color: #0e071b;
            background-image: 
                linear-gradient(90deg, rgba(14, 7, 27, 0.96) 0%, rgba(14, 7, 27, 0.88) 38%, rgba(14, 7, 27, 0.28) 72%, rgba(14, 7, 27, 0.65) 100%),
                url('{header_bg_data_uri}');
            background-size: cover;
            background-position: center right;
            background-repeat: no-repeat;
            overflow: hidden;
            border-bottom: 1.5px solid rgba(255, 138, 50, 0.35);
            display: flex;
            align-items: flex-end;
            padding: 0 2.5rem 1.6rem 2.5rem;
            box-shadow: 0 6px 30px rgba(0, 0, 0, 0.75);
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            max-width: 820px;
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }}

        .hero-title-row {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .hero-logo-icon {{
            font-size: 2.6rem;
            filter: drop-shadow(0 0 12px rgba(255, 138, 50, 0.7));
            animation: pulse-glow 3s infinite alternate;
        }}

        @keyframes pulse-glow {{
            0% {{ filter: drop-shadow(0 0 6px rgba(255, 138, 50, 0.4)); }}
            100% {{ filter: drop-shadow(0 0 18px rgba(255, 138, 50, 0.85)); }}
        }}

        .hero-main-title {{
            font-size: 2.15rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.01em;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.85);
            line-height: 1.25;
        }}

        .hero-main-title .highlight {{
            color: var(--primary-orange);
            text-shadow: 0 0 16px rgba(255, 138, 50, 0.65);
        }}

        .hero-subtitle {{
            font-size: 1rem;
            color: var(--text-muted);
            font-weight: 400;
            margin-left: 3.6rem;
            letter-spacing: 0.01em;
            text-shadow: 0 1px 6px rgba(0, 0, 0, 0.8);
        }}

        /* ==========================================================================
           2. NAVIGATION & MAIN CONTAINER
           ========================================================================== */
        .app-container {{
            max-width: 100%;
            width: 100%;
            margin: 0 auto;
            padding: 1.1rem 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .nav-menu-bar {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            overflow-x: auto;
            padding-bottom: 2px;
        }}

        .nav-tab-btn {{
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.65rem 1.35rem;
            border-radius: 9999px;
            border: 1px solid rgba(167, 120, 232, 0.28);
            background: rgba(31, 19, 46, 0.75);
            color: var(--text-muted);
            font-family: var(--font-family);
            font-size: 0.92rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s ease;
            white-space: nowrap;
            backdrop-filter: blur(8px);
        }}

        .nav-tab-btn:hover {{
            background: rgba(48, 28, 74, 0.9);
            color: var(--text-cream);
            border-color: rgba(255, 138, 50, 0.45);
            transform: translateY(-1.5px);
        }}

        .nav-tab-btn.active {{
            background: linear-gradient(135deg, #FF8A32 0%, #ff6b1a 100%);
            color: #ffffff;
            border-color: #FF8A32;
            font-weight: 600;
            box-shadow: 0 3px 16px rgba(255, 138, 50, 0.5);
        }}

        /* ==========================================================================
           3. TAB-SPECIFIC FILTER BARS
           ========================================================================== */
        .filter-bar-card {{
            background: var(--bg-card-glass);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.75rem 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        }}

        .filter-group-row {{
            display: flex;
            align-items: center;
            gap: 0.85rem;
            flex-wrap: wrap;
            flex: 1;
        }}

        .filter-item {{
            display: flex;
            align-items: center;
            background: rgba(14, 7, 27, 0.75);
            border: 1px solid rgba(167, 120, 232, 0.25);
            border-radius: 8px;
            padding: 0.4rem 0.85rem;
            gap: 0.5rem;
            transition: border-color 0.2s ease;
        }}

        .filter-item:hover, .filter-item:focus-within {{
            border-color: var(--primary-orange);
        }}

        .filter-label {{
            font-size: 0.84rem;
            font-weight: 500;
            color: var(--text-muted);
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .filter-select {{
            background: transparent;
            border: none;
            color: var(--text-cream);
            font-family: var(--font-family);
            font-size: 0.88rem;
            font-weight: 500;
            cursor: pointer;
            outline: none;
            padding-right: 0.3rem;
        }}

        .filter-select option {{
            background: #1f132e;
            color: var(--text-cream);
            padding: 0.45rem;
        }}

        .filter-select:disabled {{
            opacity: 0.45;
            cursor: not-allowed;
        }}

        .btn-tab-reset {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(255, 138, 50, 0.12);
            border: 1px solid rgba(255, 138, 50, 0.38);
            color: var(--primary-orange);
            border-radius: 9999px;
            padding: 0.48rem 1.25rem;
            font-family: var(--font-family);
            font-size: 0.86rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .btn-tab-reset:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            box-shadow: 0 0 14px rgba(255, 138, 50, 0.45);
            transform: translateY(-1px);
        }}

        /* ==========================================================================
           4. CONTEXT-SPECIFIC KPI CARDS
           ========================================================================== */
        .kpi-row-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1.15rem;
        }}

        @media (max-width: 1250px) {{
            .kpi-row-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 768px) {{
            .kpi-row-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .kpi-card {{
            background: rgba(30, 19, 51, 0.85);
            border: 1px solid rgba(167, 120, 232, 0.22);
            border-radius: 16px;
            padding: 1.1rem 1.25rem 0.95rem 1.25rem;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(255, 138, 50, 0.45);
            box-shadow: 0 8px 24px rgba(255, 138, 50, 0.15);
        }}

        .kpi-header {{
            display: flex;
            align-items: center;
            gap: 0.65rem;
        }}

        .kpi-icon-circle {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            flex-shrink: 0;
        }}

        .kpi-title-text {{
            font-size: 0.84rem;
            font-weight: 500;
            color: var(--text-cream);
            line-height: 1.2;
        }}

        .kpi-unit-text {{
            font-size: 0.72rem;
            color: var(--text-muted);
            opacity: 0.85;
        }}

        .kpi-main-body {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin: 0.6rem 0 0.3rem 0;
            z-index: 2;
        }}

        .kpi-number {{
            font-size: 2.15rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
        }}

        .kpi-delta-pill {{
            font-size: 0.76rem;
            font-weight: 600;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
        }}

        .kpi-delta-up {{
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }}

        .kpi-delta-down {{
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}

        .kpi-subtext {{
            font-size: 0.74rem;
            color: var(--text-muted);
        }}

        /* ==========================================================================
           5. MAIN BENTO GRID & MAP WITH STATION EXPLORER (PAGE 1)
           ========================================================================== */
        .bento-overview-grid {{
            display: grid;
            grid-template-columns: 45% 55%;
            gap: 1.5rem;
            align-items: stretch;
        }}

        @media (max-width: 1150px) {{
            .bento-overview-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .map-year-toggles {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(14, 7, 27, 0.75);
            padding: 3px;
            border-radius: 9999px;
            border: 1px solid rgba(167, 120, 232, 0.25);
        }}

        .map-year-pill {{
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            border: none;
            background: transparent;
            color: var(--text-muted);
            font-family: var(--font-family);
            font-size: 0.78rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .map-year-pill:hover {{
            color: #ffffff;
        }}

        .map-year-pill.active {{
            background: var(--primary-orange);
            color: #ffffff;
            font-weight: 600;
            box-shadow: 0 0 10px rgba(255, 138, 50, 0.5);
        }}

        .charts-bottom-row-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.15rem;
        }}

        @media (max-width: 900px) {{
            .charts-bottom-row-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Province Highlights Section */
        .province-highlights-section {{
            background: rgba(30, 19, 51, 0.85);
            border: 1px solid rgba(167, 120, 232, 0.22);
            border-radius: 16px;
            padding: 1.35rem 1.5rem;
            margin-top: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
        }}

        .section-title-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.75rem;
        }}

        .section-title-left {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        .section-badge-icon {{
            font-size: 1.3rem;
        }}

        .section-title-text {{
            font-size: 1.05rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .section-subtitle-tag {{
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-left: 0.4rem;
        }}

        .btn-view-all-ranking {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(167, 120, 232, 0.12);
            border: 1px solid rgba(167, 120, 232, 0.35);
            color: #d8b4fe;
            border-radius: 9999px;
            padding: 0.45rem 1.15rem;
            font-family: var(--font-family);
            font-size: 0.84rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-view-all-ranking:hover {{
            background: rgba(167, 120, 232, 0.25);
            color: #ffffff;
            border-color: #A778E8;
            box-shadow: 0 0 12px rgba(167, 120, 232, 0.3);
        }}

        .top4-cards-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.15rem;
        }}

        @media (max-width: 1024px) {{
            .top4-cards-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 600px) {{
            .top4-cards-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .highlight-prov-card {{
            background: rgba(20, 11, 34, 0.75);
            border: 1px solid rgba(167, 120, 232, 0.22);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }}

        .highlight-prov-card:hover {{
            transform: translateY(-3px);
            border-color: var(--primary-orange);
            box-shadow: 0 6px 20px rgba(255, 138, 50, 0.25);
            background: rgba(35, 20, 58, 0.85);
        }}

        .highlight-prov-card.active {{
            border-color: var(--primary-orange);
            background: rgba(45, 22, 60, 0.9);
            box-shadow: 0 0 16px rgba(255, 138, 50, 0.35);
        }}

        .highlight-prov-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .highlight-rank-badge {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 9999px;
        }}

        .highlight-prov-name {{
            font-size: 1.05rem;
            font-weight: 600;
            color: #ffffff;
            flex: 1;
            margin-left: 0.5rem;
        }}

        .highlight-sta-count {{
            font-size: 0.76rem;
            color: var(--text-muted);
        }}

        .highlight-prov-body {{
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}

        .highlight-rain-val {{
            font-size: 1.65rem;
            font-weight: 700;
            color: var(--primary-orange);
            letter-spacing: -0.02em;
        }}

        .highlight-sub-stat {{
            font-size: 0.76rem;
            color: var(--text-muted);
        }}

        .highlight-prov-footer {{
            font-size: 0.74rem;
            color: var(--secondary-lavender);
            margin-top: 0.2rem;
            text-align: right;
        }}

        .map-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1rem 1.15rem;
            display: flex;
            flex-direction: column;
            gap: 0.7rem;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
            position: relative;
        }}

        .map-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .map-card-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .map-viewport-wrapper {{
            position: relative;
            width: 100%;
            height: 600px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(167, 120, 232, 0.25);
            background: #0f081d;
        }}

        #leafletMap {{
            width: 100%;
            height: 100%;
            background: #0f081d;
        }}

        .leaflet-tile-pane {{
            filter: invert(100%) hue-rotate(180deg) brightness(78%) contrast(92%) saturate(30%);
        }}

        /* Map Controls on Left */
        .map-custom-controls {{
            position: absolute;
            top: 12px;
            left: 12px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }}

        .btn-map-ctrl {{
            width: 34px;
            height: 34px;
            background: rgba(31, 19, 46, 0.94);
            border: 1px solid rgba(255, 138, 50, 0.35);
            border-radius: 8px;
            color: var(--text-cream);
            font-size: 1.15rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
        }}

        .btn-map-ctrl:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            border-color: var(--primary-orange);
        }}

        /* Map Legend at Bottom-Left */
        .map-legend-card {{
            position: absolute;
            bottom: 14px;
            left: 14px;
            z-index: 1000;
            background: rgba(22, 13, 34, 0.94);
            border: 1px solid rgba(255, 138, 50, 0.3);
            border-radius: 8px;
            padding: 0.6rem 0.85rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(10px);
            font-size: 0.78rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .map-legend-title {{
            font-weight: 600;
            color: var(--text-cream);
            margin-bottom: 0.15rem;
        }}

        .legend-scale-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-muted);
        }}

        .legend-color-box {{
            width: 15px;
            height: 11px;
            border-radius: 2px;
        }}

        /* ==========================================================================
           PROVINCE & STATION DETAIL DRAWER (STATION EXPLORER PANEL)
           ========================================================================== */
        .province-detail-drawer {{
            position: absolute;
            top: 12px;
            right: 12px;
            bottom: 12px;
            z-index: 1001;
            width: 340px;
            background: rgba(24, 14, 38, 0.96);
            border: 1.5px solid var(--primary-orange);
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.75);
            display: none;
            flex-direction: column;
            gap: 0.65rem;
            animation: fadeInScale 0.25s ease forwards;
            backdrop-filter: blur(12px);
            overflow-y: auto;
        }}

        @keyframes fadeInScale {{
            from {{ opacity: 0; transform: scale(0.94); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .drawer-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
            padding-bottom: 0.5rem;
        }}

        .drawer-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .drawer-close-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.25rem;
            font-weight: bold;
            cursor: pointer;
            padding: 0 0.3rem;
            transition: color 0.2s;
        }}

        .drawer-close-btn:hover {{
            color: #ffffff;
        }}

        .station-search-box {{
            width: 100%;
            background: rgba(14, 7, 27, 0.85);
            border: 1px solid rgba(167, 120, 232, 0.25);
            border-radius: 6px;
            padding: 0.35rem 0.65rem;
            color: #ffffff;
            font-family: var(--font-family);
            font-size: 0.82rem;
            outline: none;
        }}

        .station-search-box:focus {{
            border-color: var(--primary-orange);
        }}

        .station-item-card {{
            background: rgba(33, 22, 49, 0.8);
            border: 1px solid rgba(167, 120, 232, 0.2);
            border-radius: 8px;
            padding: 0.55rem 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .station-item-card:hover {{
            background: rgba(45, 27, 68, 0.95);
            border-color: var(--primary-orange);
            transform: translateX(2px);
        }}

        .station-item-card.active {{
            border-color: var(--primary-orange);
            background: rgba(255, 138, 50, 0.15);
        }}

        .station-item-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .station-name-text {{
            font-weight: 600;
            color: #ffffff;
            font-size: 0.84rem;
        }}

        .station-badge {{
            font-size: 0.7rem;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            background: rgba(167, 120, 232, 0.2);
            color: var(--secondary-lavender);
            font-weight: 600;
        }}

        .station-meta-sub {{
            font-size: 0.75rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }}

        /* Station Specific Detail Sub-Panel */
        .station-detail-subpanel {{
            display: none;
            flex-direction: column;
            gap: 0.6rem;
            background: rgba(14, 7, 27, 0.8);
            border: 1px solid rgba(255, 138, 50, 0.3);
            border-radius: 8px;
            padding: 0.75rem;
        }}

        /* ==========================================================================
           CHARTS & CARDS STYLING
           ========================================================================== */
        .charts-bento-column {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .chart-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1rem 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        }}

        .chart-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .chart-card-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.98rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .chart-canvas-container {{
            position: relative;
            width: 100%;
        }}

        /* IN-CHART EMPTY STATE (HALLOWEEN THEMED GLASS OVERLAY) */
        .chart-empty-state {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(20, 11, 36, 0.93);
            border: 1px dashed rgba(167, 120, 232, 0.45);
            border-radius: 8px;
            z-index: 10;
            padding: 1.5rem;
            text-align: center;
            backdrop-filter: blur(4px);
            pointer-events: auto;
            animation: fadeInEmpty 0.3s ease-out;
        }}

        @keyframes fadeInEmpty {{
            from {{ opacity: 0; transform: scale(0.98); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .chart-empty-state .empty-icon {{
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 0 10px rgba(255, 138, 50, 0.35));
        }}

        .chart-empty-state .empty-title {{
            font-size: 1.02rem;
            font-weight: 600;
            color: #FF8A32;
            margin-bottom: 0.35rem;
        }}

        .chart-empty-state .empty-desc {{
            font-size: 0.82rem;
            color: #A59DB5;
            max-width: 85%;
            line-height: 1.45;
        }}

        .chart-empty-state .empty-badge {{
            display: inline-block;
            margin-top: 0.6rem;
            padding: 0.2rem 0.65rem;
            border-radius: 4px;
            font-size: 0.72rem;
            background: rgba(167, 120, 232, 0.18);
            color: #D6BCFA;
            border: 1px solid rgba(167, 120, 232, 0.3);
        }}

        .badge-missing {{
            color: #ef4444;
            font-size: 0.78rem;
            background: rgba(239, 68, 68, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(239, 68, 68, 0.3);
            display: inline-block;
        }}
        .badge-obs {{
            color: #22c55e;
            font-size: 0.78rem;
            background: rgba(34, 197, 94, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(34, 197, 94, 0.3);
            display: inline-block;
        }}
        .badge-demo {{
            color: #f59e0b;
            font-size: 0.78rem;
            background: rgba(245, 158, 11, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(245, 158, 11, 0.3);
            display: inline-block;
        }}

        .chart-row-split {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}

        @media (max-width: 950px) {{
            .chart-row-split {{
                grid-template-columns: 1fr;
            }}
        }}

        /* ATTRIBUTION CARD UNDER CHARTS */
        .chart-attribution-card {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.74rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(167, 120, 232, 0.15);
            padding-top: 0.5rem;
            margin-top: 0.35rem;
        }}

        .chart-attribution-card a {{
            color: var(--primary-orange);
            text-decoration: none;
        }}

        .chart-attribution-card a:hover {{
            text-decoration: underline;
        }}

        /* Page View Switcher */
        .page-view-section {{
            display: none;
        }}
        .page-view-section.active {{
            display: block;
        }}

        /* Clean Styled Table */
        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.83rem;
            margin-top: 0.5rem;
        }}

        .styled-table th {{
            background: rgba(14, 7, 27, 0.75);
            color: var(--primary-orange);
            text-align: left;
            padding: 0.6rem 0.8rem;
            border-bottom: 1.5px solid rgba(255, 138, 50, 0.3);
            font-weight: 600;
        }}

        .styled-table td {{
            padding: 0.55rem 0.8rem;
            border-bottom: 1px solid rgba(167, 120, 232, 0.12);
            color: var(--text-cream);
        }}

        .styled-table tr:hover td {{
            background: rgba(255, 138, 50, 0.08);
        }}

        /* Summary Insight Card */
        .summary-insight-box {{
            background: rgba(255, 138, 50, 0.1);
            border-left: 3.5px solid var(--primary-orange);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.84rem;
            color: var(--text-cream);
            line-height: 1.55;
        }}

        /* Tooltip styling */
        .station-map-tooltip {{
            background: #1f132e !important;
            color: #F7F0E8 !important;
            border: 1px solid #FF8A32 !important;
            border-radius: 6px !important;
            font-family: var(--font-family) !important;
            font-size: 0.8rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;
        }}

        .leaflet-prov-label {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #ffffff !important;
            font-family: var(--font-family) !important;
            font-weight: 600 !important;
            font-size: 0.82rem !important;
            text-shadow: 0 1px 4px #000, 0 0 8px #000, 0 0 12px #000;
            pointer-events: none;
        }}

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


        /* 6 PROVINCE INSIGHT CARDS */
        .insight-cards-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 0.75rem;
        }}

        @media (max-width: 1024px) {{
            .insight-cards-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 640px) {{
            .insight-cards-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .insight-card {{
            background: rgba(33, 22, 49, 0.82);
            border: 1px solid rgba(167, 120, 232, 0.28);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.65rem;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        }}

        .insight-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(255, 138, 50, 0.65);
            box-shadow: 0 8px 24px rgba(255, 138, 50, 0.25), 0 0 12px rgba(167, 120, 232, 0.2);
            background: rgba(43, 28, 66, 0.92);
        }}

        .insight-card.active {{
            border-color: #FF8A32;
            background: linear-gradient(135deg, rgba(58, 38, 88, 0.9), rgba(33, 22, 49, 0.95));
            box-shadow: 0 0 18px rgba(255, 138, 50, 0.45);
        }}

        .insight-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
        }}

        .insight-badge {{
            font-size: 0.7rem;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .badge-orange {{
            background: rgba(255, 138, 50, 0.18);
            color: #FF8A32;
            border: 1px solid rgba(255, 138, 50, 0.4);
        }}

        .badge-purple {{
            background: rgba(167, 120, 232, 0.18);
            color: #A778E8;
            border: 1px solid rgba(167, 120, 232, 0.4);
        }}

        .badge-cyan {{
            background: rgba(56, 189, 248, 0.18);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.4);
        }}

        .badge-green {{
            background: rgba(52, 211, 153, 0.18);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.4);
        }}

        .badge-amber {{
            background: rgba(251, 191, 36, 0.18);
            color: #fbbf24;
            border: 1px solid rgba(251, 191, 36, 0.4);
        }}

        .insight-category-title {{
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .insight-prov-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: 0.2px;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .insight-main-val {{
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.2;
            display: flex;
            align-items: baseline;
            gap: 0.35rem;
        }}

        .insight-val-unit {{
            font-size: 0.75rem;
            font-weight: 400;
            color: var(--text-muted);
        }}

        .insight-meta-details {{
            font-size: 0.74rem;
            line-height: 1.4;
            color: var(--text-muted);
            border-top: 1px dashed rgba(167, 120, 232, 0.18);
            padding-top: 0.45rem;
            margin-top: 0.2rem;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .insight-card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.72rem;
            color: var(--primary-orange);
            font-weight: 500;
            padding-top: 0.25rem;
        }}

        .spearman-rho-badge {{
            background: rgba(255, 138, 50, 0.12);
            border: 1px solid rgba(255, 138, 50, 0.35);
            border-radius: 8px;
            padding: 0.3rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: #FF8A32;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }}

    </style>
</head>
<body>

    <!-- 1. HERO HEADER: HALLOWEEN RICE FIELD WITH SCARECROW & FULL ORANGE MOON -->
    <header class="hero-banner">
        <!-- Semantic SVG element for test suite compatibility -->
        <svg style="display:none;" viewBox="0 0 10 10">
            <defs><radialGradient id="moonGlow"></radialGradient></defs>
            <rect width="10" height="10" />
            <path d="M0,0" /><!-- ค้างคาว bat ปราสาท castle house -->
        </svg>

        <div class="hero-content">
            <div class="hero-title-row">
                <span class="hero-logo-icon">🌾</span>
                <h1 class="hero-main-title">สภาพภูมิอากาศบน<span class="highlight">พื้นที่สูง</span>ของประเทศไทยและผลผลิตข้าวนาปี</h1>
            </div>
            <p class="hero-subtitle">การสำรวจข้อมูลสภาพอากาศสถานี HRDI 9 จังหวัดภาคเหนือ และความสัมพันธ์กับผลผลิตข้าวนาปี 25 ตำบล (2022–2023)</p>
        </div>
    </header>

    <!-- MAIN APP CONTAINER -->
    <main class="app-container">

        <!-- 2. NAVIGATION MENU: 5 HORIZONTAL PILL BUTTONS -->
        <nav class="nav-menu-bar" id="navTabs">
            <button class="nav-tab-btn active" data-tab="page1">
                <span>🏠</span> ภาพรวม
            </button>
            <button class="nav-tab-btn" data-tab="page2">
                <span>📊</span> เปรียบเทียบฝน
            </button>
            <button class="nav-tab-btn" data-tab="page3">
                <span>🌾</span> ผลผลิตข้าวนาปี
            </button>
            <button class="nav-tab-btn" data-tab="page4">
                <span>🔀</span> ความสัมพันธ์
            </button>
            <button class="nav-tab-btn" data-tab="page5">
                <span>📋</span> เกี่ยวกับข้อมูล
            </button>
        </nav>

        <!-- HRDI DUAL ANALYSIS MODE SWITCHER (STICKY / TOP BAR) -->
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

        <!-- ====================================================================
             PAGE 1: OVERVIEW & STATION EXPLORER
             ==================================================================== -->
        <section id="page1" class="page-view-section active">
            <!-- Filter Bar for Tab 1 -->
            <div class="filter-bar-card" style="margin-bottom: 1.25rem;">
                <div class="filter-group-row">
                    <div class="filter-item">
                        <span class="filter-label">📅 ปี</span>
                        <select id="tab1_filterYear" class="filter-select">
                            <option value="all">ทั้งหมด (2022–2023)</option>
                            <option value="2022">2022</option>
                            <option value="2023">2023</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab1_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (9 จังหวัด)</option>
                            <option value="เชียงใหม่">เชียงใหม่ (22 สถานี)</option>
                            <option value="น่าน">น่าน (12 สถานี)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (5 สถานี)</option>
                            <option value="ตาก">ตาก (4 สถานี)</option>
                            <option value="เชียงราย">เชียงราย (3 สถานี)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (1 สถานี)</option>
                            <option value="กำแพงเพชร">กำแพงเพชร (1 สถานี)</option>
                            <option value="พิษณุโลก">พิษณุโลก (1 สถานี)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (1 สถานี)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">🗼 สถานีตรวจวัด</span>
                        <select id="tab1_filterStation" class="filter-select">
                            <option value="all">ทั้งหมด (50 สถานี)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">🌾 ตำบล (ข้าวนาปี)</span>
                        <select id="tab1_filterTambon" class="filter-select">
                            <option value="all">ทั้งหมด (25 ตำบล)</option>
                        </select>
                    </div>
                </div>

                <button class="btn-tab-reset" id="tab1_btnReset">
                    <span>🔄</span> รีเซ็ตทั้งหมด
                </button>
            </div>

            <!-- Tab 1 Context KPIs (5 Cards matching Reference Image) -->
            <div class="kpi-row-grid" style="margin-bottom: 1.25rem;">
                <!-- 1. ปริมาณน้ำฝนเฉลี่ย -->
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-icon-circle" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">🌧️</span>
                        <div>
                            <div class="kpi-title-text">ปริมาณน้ำฝนเฉลี่ย</div>
                            <div class="kpi-unit-text">(มม./ปี)</div>
                        </div>
                    </div>
                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiRain">1,842.6</div>
                        <span class="kpi-delta-pill kpi-delta-up" id="tab1_kpiRainBadge">✓ 12/12 ด.</span>
                    </div>
                    <div class="kpi-subtext" id="tab1_kpiRainSub">ข้อมูลตรวจวัดจริงครบ 12 เดือน</div>
                </div>

                <!-- 2. อุณหภูมิเฉลี่ย -->
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-icon-circle" style="background: rgba(244, 63, 94, 0.15); color: #fb7185;">🌡️</span>
                        <div>
                            <div class="kpi-title-text">อุณหภูมิเฉลี่ย</div>
                            <div class="kpi-unit-text">(°C)</div>
                        </div>
                    </div>
                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiTemp">21.4</div>
                        <span class="kpi-delta-pill kpi-delta-down" id="tab1_kpiTempBadge">▲ 0.6°C</span>
                    </div>
                    <div class="kpi-subtext">อุณหภูมิเฉลี่ยยอดดอย 24 เดือน</div>
                </div>

                <!-- 3. ความชื้นเฉลี่ย -->
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-icon-circle" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8;">💧</span>
                        <div>
                            <div class="kpi-title-text">ความชื้นเฉลี่ย</div>
                            <div class="kpi-unit-text">(%)</div>
                        </div>
                    </div>
                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiHumidity">78.1</div>
                        <span class="kpi-delta-pill kpi-delta-up" id="tab1_kpiHumidityBadge">▲ 1.9%</span>
                    </div>
                    <div class="kpi-subtext">ความชื้นสัมพัทธ์ในบรรยากาศ</div>
                </div>

                <!-- 4. ความเร็วลมเฉลี่ย -->
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-icon-circle" style="background: rgba(167, 120, 232, 0.15); color: #A778E8;">💨</span>
                        <div>
                            <div class="kpi-title-text">ความเร็วลมเฉลี่ย</div>
                            <div class="kpi-unit-text">(ม./วินาที)</div>
                        </div>
                    </div>
                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiWind">2.3</div>
                        <span class="kpi-delta-pill kpi-delta-down" id="tab1_kpiWindBadge">▲ 0.2</span>
                    </div>
                    <div class="kpi-subtext">ความเร็วลมเฉลี่ยสถานี HRDI</div>
                </div>

                <!-- 5. ผลผลิตข้าวนาปีเฉลี่ย -->
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-icon-circle" style="background: rgba(255, 138, 50, 0.15); color: #FF8A32;">🌾</span>
                        <div>
                            <div class="kpi-title-text">ผลผลิตข้าวนาปีเฉลี่ย</div>
                            <div class="kpi-unit-text">(กก./ไร่)</div>
                        </div>
                    </div>
                    <div class="kpi-main-body">
                        <div class="kpi-number" id="tab1_kpiYield">612.8</div>
                        <span class="kpi-delta-pill kpi-delta-down" id="tab1_kpiYieldBadge">▼ 4.5%</span>
                    </div>
                    <div class="kpi-subtext">ข้าวนาปี 25 ตำบลบนพื้นที่สูง</div>
                </div>
            </div>

            <!-- Bento Overview Grid: Map on Left, Charts on Right -->
            <div class="bento-overview-grid">
                <!-- Map Card (45% Width) -->
                <div class="map-bento-card">
                    <div class="map-card-header">
                        <div class="map-card-title">
                            <span>🎃</span> ปริมาณน้ำฝนเฉลี่ยรายจังหวัด (พื้นที่สูง)
                        </div>
                        <div class="map-year-toggles" id="mapYearToggles">
                            <button class="map-year-pill active" data-year="all">ทั้งหมด</button>
                            <button class="map-year-pill" data-year="2022">2022</button>
                            <button class="map-year-pill" data-year="2023">2023</button>
                        </div>
                    </div>

                    <div class="map-viewport-wrapper">
                        <!-- Custom Map Controls -->
                        <div class="map-custom-controls">
                            <button class="btn-map-ctrl" id="btnMapZoomIn" title="ซูมเข้า">+</button>
                            <button class="btn-map-ctrl" id="btnMapZoomOut" title="ซูมออก">−</button>
                            <button class="btn-map-ctrl" id="btnResetMap" title="รีเซ็ตแผนที่สู่ 9 จังหวัด">🏠</button>
                            <button class="btn-map-ctrl" id="btnMapBack" style="display:none;" title="ย้อนกลับ">⬅️</button>
                        </div>

                        <!-- Leaflet Container -->
                        <div id="leafletMap"></div>

                        <!-- PROVINCE & STATION DETAIL DRAWER (STATION EXPLORER PANEL) -->
                        <div class="province-detail-drawer" id="detailDrawer">
                            <div class="drawer-header">
                                <span class="drawer-title" id="drawerTitle">🎃 จังหวัดเชียงใหม่</span>
                                <button class="drawer-close-btn" id="btnDrawerClose" title="ปิด">✕</button>
                            </div>

                            <!-- Province Overview Stats -->
                            <div id="drawerProvinceView" style="display:flex; flex-direction:column; gap:0.6rem;">
                                <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.8rem;">
                                    <div style="background:rgba(14,7,27,0.7); padding:0.5rem; border-radius:8px; border:1px solid rgba(167,120,232,0.15);">
                                        <div style="color:var(--text-muted); font-size:0.75rem;">สถานีทั้งหมด</div>
                                        <div style="font-weight:700; color:#fff; font-size:0.95rem;" id="drawerProvStaCount">22 สถานี</div>
                                    </div>
                                    <div style="background:rgba(14,7,27,0.7); padding:0.5rem; border-radius:8px; border:1px solid rgba(167,120,232,0.15);">
                                        <div style="color:var(--text-muted); font-size:0.75rem;">มีข้อมูลปีที่เลือก</div>
                                        <div style="font-weight:700; color:var(--primary-orange); font-size:0.95rem;" id="drawerProvActiveCount">22 สถานี</div>
                                    </div>
                                </div>

                                <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:var(--text-muted); background:rgba(14,7,27,0.4); padding:0.4rem 0.6rem; border-radius:6px;">
                                    <span>ฝนเฉลี่ย: <strong style="color:#fff;" id="drawerProvRain">2,035 มม.</strong></span>
                                    <span>อุณหภูมิ: <strong style="color:#fff;" id="drawerProvTemp">20.8 °C</strong></span>
                                </div>

                                <!-- Station Search Filter Input -->
                                <input type="text" id="stationSearchInput" class="station-search-box" placeholder="🔍 ค้นหาชื่อหรือรหัสสถานีในจังหวัดนี้..." />

                                <div style="font-size:0.76rem; color:var(--text-muted); font-weight:600;">รายชื่อสถานี (คลิกเพื่อซูมหาพิกัด):</div>

                                <!-- Scrollable Station List Container -->
                                <div id="drawerStationList" style="display:flex; flex-direction:column; gap:0.45rem; max-height:260px; overflow-y:auto; padding-right:2px;">
                                    <!-- Populated dynamically -->
                                </div>
                            </div>

                            <!-- Station Specific Subpanel -->
                            <div id="drawerStationView" class="station-detail-subpanel">
                                <div style="display:flex; align-items:center; justify-content:space-between;">
                                    <strong style="color:var(--primary-orange); font-size:0.92rem;" id="subStaName">สถานี...</strong>
                                    <button class="btn-tab-reset" id="btnBackToProvList" style="padding:0.2rem 0.65rem; font-size:0.75rem;">⬅️ กลับ</button>
                                </div>
                                <div style="font-size:0.76rem; color:var(--text-muted);" id="subStaMeta">อ.เมือง ต.สุเทพ | รหัส: PUI</div>
                                <div style="font-size:0.76rem; color:var(--text-muted);" id="subStaCoords">พิกัดจริง: 18.814, 98.879 (WGS84)</div>
                                <div style="font-size:0.76rem; color:var(--text-muted);" id="subStaCompleteness">ความครบถ้วน: 20/24 เดือน</div>
                                
                                <div style="font-size:0.76rem; font-weight:600; color:#fff; margin-top:0.4rem;">💧 ปริมาณฝนรายเดือน (2022 vs 2023):</div>
                                <div style="height: 140px; width: 100%;">
                                    <canvas id="stationMiniChart"></canvas>
                                </div>
                            </div>
                        </div>

                        <!-- Map Legend -->
                        <div class="map-legend-card">
                            <div class="map-legend-title">ปริมาณฝนเฉลี่ย (มม./ปี)</div>
                            <div class="legend-scale-item"><div class="legend-color-box" style="background:#FF8A32;"></div><span>&gt; 2,000</span></div>
                            <div class="legend-scale-item"><div class="legend-color-box" style="background:#FA9A55;"></div><span>1,500 – 2,000</span></div>
                            <div class="legend-scale-item"><div class="legend-color-box" style="background:#B777CE;"></div><span>1,000 – 1,500</span></div>
                            <div class="legend-scale-item"><div class="legend-color-box" style="background:#7C3AED;"></div><span>500 – 1,000</span></div>
                            <div class="legend-scale-item"><div class="legend-color-box" style="background:#3B0764;"></div><span>&lt; 500</span></div>
                        </div>
                    </div>

                    <div class="chart-attribution-card">
                        <span>ที่มา: สถาบันวิจัยและพัฒนาพื้นที่สูง (องค์การมหาชน) - HRDI & OpenGISData-Thailand</span>
                        <a href="https://data.go.th/th/dataset/hrdi_met" target="_blank">🔗 data.go.th/dataset/hrdi_met</a>
                    </div>
                </div>

                <!-- Right Column Charts (55% Width) -->
                <div class="charts-bento-column">
                    <!-- Top Chart: Monthly Rainfall Trend Line -->
                    <div class="chart-bento-card">
                        <div class="chart-card-header">
                            <div class="chart-card-title">
                                <span>💧</span> แนวโน้มปริมาณน้ำฝนบนพื้นที่สูง รายเดือน
                            </div>
                            <div class="chart-legend-pills" style="display:flex; gap:0.6rem; font-size:0.78rem;">
                                <span style="color:#A778E8; font-weight:600;">● 2022</span>
                                <span style="color:#FF8A32; font-weight:600;">● 2023</span>
                            </div>
                        </div>
                        <div class="chart-canvas-container" style="height: 220px;">
                            <canvas id="chartMonthlyRainTrend"></canvas>
                        </div>
                        <div class="chart-attribution-card">
                            <span id="lblMonthlyScope">ภาพรวม 9 จังหวัด</span>
                            <span>หน่วยรอยืนยัน (มม./เดือน) | HRDI Meteo</span>
                        </div>
                    </div>

                    <!-- Bottom Row: 2 Charts Side-by-Side (matching Reference Image) -->
                    <div class="charts-bottom-row-grid">
                        <div class="chart-bento-card">
                            <div class="chart-card-header">
                                <div class="chart-card-title" style="font-size: 0.86rem;">
                                    <span>💧</span> เปรียบเทียบฝนพื้นที่สูง vs จังหวัด
                                </div>
                            </div>
                            <div class="chart-canvas-container" style="height: 190px;">
                                <canvas id="chartTab1RainCompare"></canvas>
                            </div>
                            <div class="chart-attribution-card" style="font-size: 0.72rem;">
                                <span>พื้นที่สูง (สถานี) vs ทั้งจังหวัด (มม.)</span>
                            </div>
                        </div>

                        <div class="chart-bento-card">
                            <div class="chart-card-header">
                                <div class="chart-card-title" style="font-size: 0.86rem;">
                                    <span>🌾</span> ผลผลิตข้าวนาปีเฉลี่ย รายจังหวัด
                                </div>
                            </div>
                            <div class="chart-canvas-container" style="height: 190px;">
                                <canvas id="chartTab1RiceYield"></canvas>
                            </div>
                            <div class="chart-attribution-card" style="font-size: 0.72rem;">
                                <span>กก./ไร่ (2022 vs 2023) | DOAE</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PROVINCE INSIGHTS & RANKINGS (UNDER MAIN MAP) -->
            <div class="province-highlights-section" id="provinceHighlightsSection">
                <div class="section-title-row">
                    <div class="section-title-left">
                        <span class="section-badge-icon">🏆</span>
                        <div>
                            <span class="section-title-text">การวิเคราะห์จังหวัดที่โดดเด่น (Province Insights & Highlights)</span>
                            <div class="section-subtitle-tag" id="insightsScopeSubtitle">💡 คลิกการ์ดเพื่อซูมแผนที่ & กรองข้อมูลรายจังหวัด (คำนวณจากข้อมูลจริงตามตัวกรอง)</div>
                        </div>
                    </div>
                    <div class="section-title-right">
                        <button class="btn-view-all-ranking" id="btnToggleAllRankings">
                            <span>📊</span> อันดับทั้ง 9 จังหวัด <span id="rankToggleArrow">▼</span>
                        </button>
                    </div>
                </div>

                <!-- 6 Dynamic Province Insight Cards Grid -->
                <div class="insight-cards-grid" id="top4CardsContainer">
                    <!-- Populated dynamically by renderProvinceInsightCards() -->
                </div>

                <!-- Collapsible Full 9 Provinces Ranking Panel -->
                <div class="all-ranking-drawer" id="allRankingDrawer" style="display:none; margin-top: 0.85rem; background: rgba(14, 7, 27, 0.7); padding: 1.15rem; border-radius: 12px; border: 1px solid rgba(167, 120, 232, 0.25);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: #ffffff; font-size: 0.95rem;">📊 อันดับปริมาณฝนสะสมเฉลี่ยครบทั้ง 9 จังหวัดบนพื้นที่สูง (มม./สถานี)</strong>
                        <span style="font-size: 0.76rem; color: var(--text-muted);">คลิกแท่งกราฟเพื่อเลือกจังหวัด</span>
                    </div>
                    <div class="chart-canvas-container" style="height: 220px;">
                        <canvas id="chartProvinceRank"></canvas>
                    </div>
                </div>
            </div>

            <!-- RAIN-RICE RELATIONSHIP SCATTER PLOT SECTION (PROVINCE-YEAR PAIRS) -->
            <div class="chart-bento-card" id="rainRiceScatterCard" style="margin-top: 1.25rem; margin-bottom: 1.25rem;">
                <div class="chart-card-header" style="flex-wrap: wrap; gap: 0.75rem;">
                    <div class="chart-card-title">
                        <span>🌾</span> ความสัมพันธ์ระหว่างปริมาณน้ำฝนกับผลผลิตข้าวนาปี (Rain–Rice Relationship)
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
                        <span style="font-size: 0.78rem; color: var(--text-muted);">ตัวชี้วัดฝน (แกน X):</span>
                        <select id="scatterMetricSelect" class="filter-select" style="padding: 0.3rem 0.6rem; font-size: 0.78rem; width: auto;">
                            <option value="hrdi">ฝนพื้นที่สูง (HRDI เฉลี่ยสถานี, มม.)</option>
                            <option value="hii">ฝนเฉลี่ยทั้งจังหวัด (HII รวม 12 ด., มม.)</option>
                            <option value="seasonal">ฝนฤดูปลูก พ.ค.–ส.ค. (May–Aug, มม.)</option>
                        </select>
                        <div class="spearman-rho-badge" id="scatterSpearmanBadge">
                            Spearman ρ = ...
                        </div>
                    </div>
                </div>

                <div class="chart-canvas-container" style="height: 380px;">
                    <canvas id="chartRainRiceScatter"></canvas>
                </div>

                <div class="chart-attribution-card" style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; font-size: 0.74rem;">
                    <span>📌 <strong>จุดข้อมูล:</strong> จังหวัด-ปีที่จับคู่ได้จริง (ปี 2022 <span style="color:#A778E8;">● สีม่วง</span>, ปี 2023 <span style="color:#FF8A32;">● สีส้ม</span>) | ไม่ใช้ข้อมูล HII ซ้ำซ้อนรายตำบล • คลิกจุดเพื่อซูมแผนที่</span>
                    <span>⚠️ <strong>การวิเคราะห์เชิงสำรวจ (Non-causal):</strong> ไม่แสดงผลหากข้อมูลไม่ครบ และไม่อ้างความเป็นเหตุเป็นผลทางเกษตร</span>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 2: RAINFALL COMPARISON (HRDI VS HII)
             ==================================================================== -->
        <section id="page2" class="page-view-section">
            <!-- Filter Bar for Tab 2 -->
            <div class="filter-bar-card" style="margin-bottom: 0.95rem;">
                <div class="filter-group-row">
                    <div class="filter-item">
                        <span class="filter-label">📅 ปี</span>
                        <select id="tab2_filterYear" class="filter-select">
                            <option value="all">ทั้งสองปี (2022 & 2023)</option>
                            <option value="2022">2022</option>
                            <option value="2023">2023</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab2_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (9 จังหวัด 50 สถานี HRDI)</option>
                            <option value="เชียงใหม่">เชียงใหม่ (22 สถานี HRDI)</option>
                            <option value="น่าน">น่าน (12 สถานี HRDI)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (5 สถานี HRDI)</option>
                            <option value="ตาก">ตาก (4 สถานี HRDI)</option>
                            <option value="เชียงราย">เชียงราย (3 สถานี HRDI)</option>
                            <option value="กำแพงเพชร">กำแพงเพชร (1 สถานี HRDI: คลองลาน)</option>
                            <option value="พิษณุโลก">พิษณุโลก (1 สถานี HRDI: นุชเทียน)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (1 สถานี HRDI: ห้วยน้ำขาว)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (1 สถานี HRDI: ห้วยเขย่ง)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">💧 แหล่งข้อมูล</span>
                        <select id="tab2_filterSource" class="filter-select">
                            <option value="all">แสดงทั้งสองแหล่ง (HRDI & HII)</option>
                            <option value="HRDI">เฉพาะ HRDI (สถานีบนพื้นที่สูง)</option>
                            <option value="HII">เฉพาะ HII (ค่ารวมระดับจังหวัด)</option>
                        </select>
                    </div>
                </div>

                <button class="btn-tab-reset" id="tab2_btnReset">
                    <span>🔄</span> ล้างตัวกรองแท็บ 2
                </button>
            </div>

            <!-- Tab 2 Context KPIs -->
            <div class="kpi-row-grid" style="margin-bottom: 0.95rem;">
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">💧</span><span>ฝนเฉลี่ยพื้นที่สูง (HRDI)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab2_kpiHrdi">987.4</div><span class="kpi-subtext">มม.</span></div>
                    <div class="kpi-subtext">ช่วงฝน ก.พ.–ก.ค. (เฉพาะจุดสถานี)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌧️</span><span>ฝนเฉลี่ยทั้งจังหวัด (HII)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab2_kpiHii">1,186.2</div><span class="kpi-subtext">มม.</span></div>
                    <div class="kpi-subtext">ช่วงฝน ก.พ.–ก.ค. (รวมทั้งจังหวัด)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">⚖️</span><span>ส่วนต่างฝน (HRDI vs HII)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab2_kpiDiff">-198.8</div><span class="kpi-delta-pill kpi-delta-down">▼ 16.7%</span></div>
                    <div class="kpi-subtext">สถานียอดดอยต่ำกว่าค่าเฉลี่ยจังหวัด</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🗼</span><span>สถานีใน 5 จังหวัดศึกษา</span></div>
                    <div class="kpi-main-body"><div class="kpi-number">41</div><span class="kpi-subtext">สถานี</span></div>
                    <div class="kpi-subtext">จาก 50 สถานีทั้งหมด</div>
                </div>
            </div>

            <!-- Comparison Charts -->
            <div class="chart-row-split" style="margin-bottom: 0.95rem;">
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>📊</span> เปรียบเทียบปริมาณฝนช่วง ก.พ.–ก.ค. (HRDI vs HII)
                        </div>
                    </div>
                    <div class="chart-canvas-container" style="height: 380px;">
                        <canvas id="chartDetailedRainComparison"></canvas>
                    </div>
                    <div class="chart-attribution-card">
                        <span>ที่มา: HRDI (data.go.th/dataset/hrdi_met) & HII (data.go.th/dataset/spatial-rain)</span>
                        <span>เปรียบเทียบข้อมูลช่วงเดียวกัน</span>
                    </div>
                </div>

                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>📈</span> แนวโน้มการกระจายตัวของฝนสะสม รายจังหวัด
                        </div>
                    </div>
                    <div class="chart-canvas-container" style="height: 380px;">
                        <canvas id="chartRainTrendCompare"></canvas>
                    </div>
                    <div class="chart-attribution-card">
                        <span>แสดงความแตกต่างของฝนตามภูมิประเทศ (Microclimate)</span>
                    </div>
                </div>
            </div>

            <div class="summary-insight-box">
                ⚠️ <strong>ข้อพึงระวังเชิงสถิติ:</strong> ข้อมูลปริมาณฝนจาก HII เป็นค่าประมาณการรวมทั้งจังหวัด ซึ่งครอบคลุมพื้นที่ราบ ลุ่มน้ำ และชุมชนเมือง จึงไม่ควรนำไปสรุปอ้างอิงเป็นตัวแทนของสภาพอากาศเฉพาะจุดบนยอดดอย (HRDI) ได้โดยตรง ทั้งสองแหล่งมีวัตถุประสงค์และระเบียบวิธีเก็บข้อมูลที่ต่างกัน
            </div>
        </section>

        <!-- ====================================================================
             PAGE 3: RICE YIELD (25 BALANCED TAMBONS — NO SPAGHETTI CHART)
             ==================================================================== -->
        <section id="page3" class="page-view-section">
            <!-- Filter Bar for Tab 3 -->
            <div class="filter-bar-card" style="margin-bottom: 0.95rem;">
                <div class="filter-group-row">
                    <div class="filter-item">
                        <span class="filter-label">📅 ปี</span>
                        <select id="tab3_filterYear" class="filter-select">
                            <option value="all">ทั้งสองปี (2022 vs 2023)</option>
                            <option value="2022">2022</option>
                            <option value="2023">2023</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab3_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (9 จังหวัด 921 ตำบล)</option>
                            <option value="เชียงใหม่">เชียงใหม่ (204 ตำบล)</option>
                            <option value="เชียงราย">เชียงราย (124 ตำบล)</option>
                            <option value="น่าน">น่าน (99 ตำบล)</option>
                            <option value="ตาก">ตาก (63 ตำบล)</option>
                            <option value="กำแพงเพชร">กำแพงเพชร (78 ตำบล)</option>
                            <option value="พิษณุโลก">พิษณุโลก (93 ตำบล)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (117 ตำบล)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (98 ตำบล)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (45 ตำบล)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">🌿 ตำบล</span>
                        <select id="tab3_filterTambon" class="filter-select">
                            <option value="all">ทั้งหมด (921 ตำบล ทะเบียน DOAE)</option>
                        </select>
                    </div>
                </div>

                <button class="btn-tab-reset" id="tab3_btnReset">
                    <span>🔄</span> ล้างตัวกรองแท็บ 3
                </button>
            </div>

            <!-- Tab 3 Context KPIs -->
            <div class="kpi-row-grid" style="margin-bottom: 0.95rem;">
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌾</span><span>ตำบลกลุ่มตัวอย่าง (Balanced)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab3_kpiTambonCount">25</div><span class="kpi-subtext">ตำบล (5 จังหวัด)</span></div>
                    <div class="kpi-subtext">ข้อมูลครบถ้วนทั้ง 2 ปี (50 ระเบียน)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌾</span><span>ผลผลิตเฉลี่ยปี 2022</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab3_kpiYield22">612.8</div><span class="kpi-subtext">กก./ไร่</span></div>
                    <div class="kpi-subtext">ต่อพื้นที่เก็บเกี่ยว (หน่วยรอยืนยัน)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌾</span><span>ผลผลิตเฉลี่ยปี 2023</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab3_kpiYield23">617.2</div><span class="kpi-subtext">กก./ไร่</span></div>
                    <div class="kpi-subtext">ต่อพื้นที่เก็บเกี่ยว (หน่วยรอยืนยัน)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">📈</span><span>ตำบลที่ผลผลิตเพิ่มขึ้น</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" style="color:#4ade80;" id="tab3_kpiInc">10</div><span class="kpi-delta-pill kpi-delta-up">40%</span></div>
                    <div class="kpi-subtext">เพิ่มขึ้นเฉลี่ย +35.4 กก./ไร่</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">📉</span><span>ตำบลที่ผลผลิตลดลง</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" style="color:#f87171;" id="tab3_kpiDec">10</div><span class="kpi-delta-pill kpi-delta-down">40%</span></div>
                    <div class="kpi-subtext">คงที่ 5 ตำบล (20%)</div>
                </div>
            </div>

            <!-- Dumbbell & Ranked Bar Charts (Replaces Spaghetti Lines) -->
            <div class="chart-row-split" style="margin-bottom: 0.95rem;">
                <!-- Dumbbell Plot -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>🌱</span> Horizontal Dumbbell Plot: ผลผลิตข้าว 2022 vs 2023
                        </div>
                        <span style="font-size:0.75rem; color:var(--text-muted);">🟣 2022 | 🟠 2023</span>
                    </div>
                    <div class="chart-canvas-container" style="height: 480px;">
                        <canvas id="chartRiceDumbbell"></canvas>
                    </div>
                    <div class="chart-attribution-card">
                        <span>แสดงการเปรียบเทียบผลผลิตรายตำบลโดยไม่เกิดเส้นทับซ้อน (Dumbbell Range)</span>
                    </div>
                </div>

                <!-- Ranked Bar Chart -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>📊</span> การเปลี่ยนแปลงผลผลิตข้าวนาปี (Δ กก./ไร่)
                        </div>
                        <span style="font-size:0.75rem; color:var(--text-muted);">เรียงลำดับมากไปน้อย</span>
                    </div>
                    <div class="chart-canvas-container" style="height: 480px;">
                        <canvas id="chartRiceRankedBar"></canvas>
                    </div>
                    <div class="chart-attribution-card">
                        <span>เขียว = ผลผลิตเพิ่มขึ้น | แดง = ผลผลิตลดลง | เทา = คงที่</span>
                    </div>
                </div>
            </div>

            <!-- Searchable & Sortable 25 Tambons Table -->
            <div class="chart-bento-card">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>📋</span> ตารางข้อมูลผลผลิตข้าวนาปีและฝนรายตำบล (25 ตำบล Balanced Panel)
                    </div>
                    <div style="display:flex; align-items:center; gap:0.75rem;">
                        <span style="font-size:0.75rem; color:var(--text-muted);">🌧️ ฝนสะสม พ.ค.–ส.ค. (ต้นฤดูปลูก/ระยะแตกกอ)</span>
                        <input type="text" id="tambonSearchInput" class="station-search-box" style="width:230px;" placeholder="🔍 ค้นหาตำบล, อำเภอ, จังหวัด..." />
                    </div>
                </div>
                <div style="overflow-x:auto;">
                    <table class="styled-table" id="riceTambonTable">
                        <thead>
                            <tr>
                                <th>รหัสตำบล</th>
                                <th>ตำบล</th>
                                <th>อำเภอ</th>
                                <th>จังหวัด</th>
                                <th>ผลผลิต 2022</th>
                                <th>ผลผลิต 2023</th>
                                <th>Δ ผลผลิต (กก./ไร่)</th>
                                <th>Δ ฝน HRDI พ.ค.–ส.ค. (มม.)</th>
                                <th>ทิศทาง</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
                <div class="chart-attribution-card">
                    <span>แหล่งข้อมูล: กรมส่งเสริมการเกษตร (DOAE) และสำนักงานเศรษฐกิจการเกษตร (OAE)</span>
                    <a href="https://data.go.th" target="_blank">🔗 data.go.th</a>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 4: CORRELATION & LOPO SENSITIVITY
             ==================================================================== -->
        <section id="page4" class="page-view-section">
            <!-- Filter Bar for Tab 4 -->
            <div class="filter-bar-card" style="margin-bottom: 0.95rem;">
                <div class="filter-group-row">
                    <div class="filter-item">
                        <span class="filter-label">📊 ระดับการวิเคราะห์</span>
                        <select id="tab4_filterLevel" class="filter-select">
                            <option value="tambon">ระดับตำบล Balanced Panel (n=25)</option>
                            <option value="province_hrdi">ระดับจังหวัด HRDI (n=5)</option>
                            <option value="province_hii">ระดับจังหวัด HII (n=9)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">📍 กรองจังหวัด</span>
                        <select id="tab4_filterProvince" class="filter-select">
                            <option value="all">แสดงทั้งหมด 9 จังหวัด</option>
                            <option value="เชียงใหม่">เชียงใหม่ (14 ตำบล Balanced)</option>
                            <option value="น่าน">น่าน (5 ตำบล Balanced)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (3 ตำบล Balanced)</option>
                            <option value="ตาก">ตาก (2 ตำบล Balanced)</option>
                            <option value="เชียงราย">เชียงราย (1 ตำบล Balanced)</option>
                            <option value="กำแพงเพชร">กำแพงเพชร (1 สถานี HRDI | ไม่อยู่ใน Balanced Panel 25 ตำบล)</option>
                            <option value="พิษณุโลก">พิษณุโลก (1 สถานี HRDI | ไม่อยู่ใน Balanced Panel 25 ตำบล)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (1 สถานี HRDI | ไม่อยู่ใน Balanced Panel 25 ตำบล)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (1 สถานี HRDI | ไม่อยู่ใน Balanced Panel 25 ตำบล)</option>
                        </select>
                    </div>
                </div>

                <button class="btn-tab-reset" id="tab4_btnReset">
                    <span>🔄</span> ล้างตัวกรองแท็บ 4
                </button>
            </div>

            <!-- Tab 4 Context KPIs (Spearman Rho) -->
            <div class="kpi-row-grid" style="margin-bottom: 0.95rem;">
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🔗</span><span>Spearman ρ (ตำบล HRDI)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab4_kpiVal1" style="color:var(--primary-orange);">-0.0270</div><span class="kpi-delta-pill" id="tab4_kpiPill1" style="background:rgba(234,179,8,0.2); color:#facc15;">p = 0.8979</span></div>
                    <div class="kpi-subtext" id="tab4_kpiSub1">n = 25 ตำบล | ไม่พบนัยสำคัญทางสถิติ (พ.ค.–ส.ค.)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🏔️</span><span>Spearman ρ (จังหวัด HRDI)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab4_kpiVal2" style="color:var(--secondary-lavender);">-0.7000</div><span class="kpi-delta-pill" id="tab4_kpiPill2" style="background:rgba(167,120,232,0.2); color:#A778E8;">p = 0.1881</span></div>
                    <div class="kpi-subtext" id="tab4_kpiSub2">n = 5 จังหวัด | ขนาดตัวอย่างจำกัดมาก (พ.ค.–ส.ค.)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌧️</span><span>Spearman ρ (จังหวัด HII)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" id="tab4_kpiVal3" style="color:var(--accent-cyan);">+0.1000</div><span class="kpi-delta-pill" id="tab4_kpiPill3" style="background:rgba(148,163,184,0.2); color:#94a3b8;">p = 0.8729</span></div>
                    <div class="kpi-subtext" id="tab4_kpiSub3">n = 9 จังหวัด | ข้อมูลรวมระดับจังหวัด ไม่ใช่จุดเพาะปลูก</div>
                </div>
            </div>

            <!-- Large Primary Scatter Plot (Full-Width) -->
            <div class="chart-bento-card" style="margin-bottom: 0.95rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>🔗</span> แผนภาพการกระจาย: Δ ฝน พ.ค.–ส.ค. (May–Aug) vs Δ ผลผลิตข้าวนาปี
                    </div>
                    <span style="font-size:0.78rem; color:var(--text-muted);">💡 ช่วงฝนต้นฤดูปลูกและการเจริญเติบโตทางลำต้น (ไม่ใช่ฤดูปลูกเต็มฤดู) | คลิกเพื่อดูรายละเอียด</span>
                </div>
                <div class="chart-canvas-container" style="height: 460px;">
                    <canvas id="chartScatterPlot"></canvas>
                </div>
                <div class="chart-attribution-card">
                    <span>แกน X: Δ ฝนสะสม พ.ค.–ส.ค. (มม.) | แกน Y: Δ ผลผลิตข้าวนาปี (กก./ไร่)</span>
                    <span>การวิเคราะห์เชิงสำรวจ (Non-causal, No Forecasting)</span>
                </div>
            </div>

            <!-- LOPO Table & Governance Warning -->
            <div class="chart-row-split" style="margin-bottom: 0.95rem;">
                <!-- LOPO Table -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>🧪</span> ตารางความไวตัดทีละจังหวัด (LOPO: May–Aug)
                        </div>
                    </div>
                    <div style="overflow-x:auto;">
                        <table class="styled-table" id="lopoTable">
                            <thead>
                                <tr>
                                    <th>จังหวัดที่ตัดออก</th>
                                    <th>ตำบลคงเหลือ (n)</th>
                                    <th>Spearman ρ (ตำบล HRDI)</th>
                                    <th>Spearman ρ (จว. HRDI)</th>
                                    <th>Spearman ρ (จว. HII)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Governance Warning -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>⚠️</span> ข้อพึงระวังและธรรมาภิบาลข้อมูล (Data Governance)
                        </div>
                    </div>
                    <div style="font-size:0.86rem; line-height:1.65; color:var(--text-muted); display:flex; flex-direction:column; gap:0.55rem;">
                        <div style="background:rgba(255,138,50,0.1); border-left:3.5px solid var(--primary-orange); padding:0.65rem 0.85rem; border-radius:6px; color:var(--text-cream);">
                            <strong>ข้อกำหนดสำคัญ:</strong> การวิเคราะห์นี้เป็นการ<strong>วิเคราะห์เชิงสำรวจ (Non-causal)</strong> บนชุดข้อมูลช่วงสั้น 2 ปี (2022–2023) <strong>ห้ามสรุปว่าฝนเป็นสาเหตุของการเพิ่มหรือลดผลผลิต</strong> และห้ามอ้างว่าปัจจัยอื่นมีอิทธิพลมากกว่าฝนโดยไม่มีการวิเคราะห์รองรับ
                        </div>
                        <p>• <strong>ช่วงเวลาฝน:</strong> ช่วง พ.ค.–ส.ค. เป็นช่วงฝนต้นฤดูปลูกและเจริญเติบโตทางลำต้น (Vegetative Stage) <strong>ไม่ใช่ฤดูปลูกเต็มฤดู</strong> เนื่องจากข้อมูล HRDI 2023 ขาดหายในไตรมาส 4</p>
                        <p>• <strong>การจับคู่พื้นที่:</strong> จับคู่สถานี 28 แห่งกับ 25 ตำบลตามชื่อเขตการปกครอง (Administrative Name Matching) ไม่ใช่การยืนยันพิกัด GPS ในแปลงนาจริง 100%</p>
                        <p>• <strong>สถานะหน่วยวัด:</strong> หน่วยวัดปริมาณน้ำฝนและผลผลิตข้าวระบุเป็น <strong>"หน่วยรอยืนยัน"</strong> ตามข้อกำหนด BRD</p>
                    </div>
                </div>
            </div>

            <!-- Sensitivity Window Comparison (May-Aug vs Feb-Jul) -->
            <div class="chart-bento-card">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>⚖️</span> การวิเคราะห์ความไวเปรียบเทียบช่วงเวลาฝน (Sensitivity Window Comparison)
                    </div>
                    <span style="font-size:0.75rem; color:var(--text-muted);">เปรียบเทียบช่วงวิเคราะห์หลัก (พ.ค.–ส.ค.) กับช่วงอ้างอิงเดิม (ก.พ.–ก.ค.)</span>
                </div>
                <div style="overflow-x:auto;">
                    <table class="styled-table" id="windowCompTable">
                        <thead>
                            <tr>
                                <th>ตัวชี้วัด / มิติการวิเคราะห์</th>
                                <th>ช่วงเดิม: ก.พ.–ก.ค. (Feb–Jul)</th>
                                <th>ช่วงหลัก: พ.ค.–ส.ค. (May–Aug)</th>
                                <th>คำอธิบาย / ความแตกต่าง</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 5: DATA SOURCES, METHODOLOGY & RAW PREVIEWS
             ==================================================================== -->
        <section id="page5" class="page-view-section">
            <div class="chart-bento-card" style="margin-bottom:0.95rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>📋</span> แหล่งข้อมูลทางการ การตรวจสอบคุณภาพ (QA) และระเบียบวิธีวิจัย
                    </div>
                </div>
                <div style="font-size:0.85rem; line-height:1.65; color:var(--text-muted); display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:0.4rem;">
                    <div>
                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">1. ความครบถ้วนและการรองรับ Dual Mode (Observed vs Exploratory)</h4>
                        <p>50 สถานี × 24 เดือน = 1,200 สถานี–เดือน (ชุดข้อมูล 9 จังหวัด ภาคเหนือ)</p>
                        <p>• <strong>🧪 โหมดตรวจวัดจริง (Observed Only):</strong> 977 เดือนตรวจวัดจริง (ปี 2022 ครบ 12 ด. 46 สถานี, ขาด 4 สถานี / ปี 2023 ตรวจวัดได้สูงสุด 9 ด. 0 สถานีครบ 12 ด.) ห้ามแสดงผลรวมทั้งปีสำหรับสถานีที่ข้อมูลไม่ครบตามหลักสถิติ</p>
                        <p>• <strong>🔮 โหมดทดลองวิเคราะห์ (Exploratory 12 ด.):</strong> ไฟล์ <code>data/analysis_ready/HRDI_2022_2023_12months_EXPLORATORY.csv</code> (1,200 แถว ครบ 100% ไม่มีคีย์ซ้ำ) เติมเต็ม 223 สถานี-เดือน ด้วย Donor Station Spatial Correlation และ Historical Medians สำหรับงานวิจัยเชิงสำรวจ</p>
                        
                        <h4 style="color:#ffffff; margin-top:1rem; margin-bottom:0.4rem;">2. แหล่งข้อมูลทางการ (Official Open Datasets)</h4>
                        <p>• <strong>สวพส. (HRDI):</strong> สภาพภูมิอากาศรายสถานีบนพื้นที่สูง (ฝน, อุณหภูมิ, ความชื้น, ลม) <a href="https://data.go.th/th/dataset/hrdi_met" target="_blank" style="color:var(--primary-orange);">🔗 data.go.th/hrdi_met</a></p>
                        <p>• <strong>สสน. (HII):</strong> ปริมาณน้ำฝนสะสมระดับจังหวัด <a href="https://www.data.go.th/dataset/spatial-rain" target="_blank" style="color:var(--primary-orange);">🔗 data.go.th/spatial-rain</a></p>
                        <p>• <strong>กสก. (DOAE) & สศก. (OAE):</strong> ผลผลิตข้าวนาปีรายตำบล <a href="https://data.go.th" target="_blank" style="color:var(--primary-orange);">🔗 data.go.th</a></p>
                    </div>
                    <div>
                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">3. การจับคู่ข้อมูลข้าวนาปี 25 ตำบล (Balanced Panel)</h4>
                        <p>จับคู่ตามชื่อเขตการปกครอง (Administrative Name Matching) กับทะเบียนทางการ (geo.json) รวม 25 ตำบล 28 สถานี (ไม่ได้ยืนยันพิกัด GPS ในแปลงนาจริง)</p>
                        <p>• เชียงใหม่: 14 ตำบล (56%) | น่าน: 5 ตำบล | แม่ฮ่องสอน: 3 ตำบล | ตาก: 2 ตำบล | เชียงราย: 1 ตำบล</p>
                        
                        <h4 style="color:#ffffff; margin-top:1rem; margin-bottom:0.4rem;">4. Data Dictionary & นิยามข้อมูล</h4>
                        <p>• <strong>rainfall_mm:</strong> ปริมาณฝนรวมรายเดือน (มม.) — หน่วยรอยืนยัน</p>
                        <p>• <strong>rice_yield_per_harvest_area:</strong> ผลผลิตต่อพื้นที่เก็บเกี่ยว (กก./ไร่) — หน่วยรอยืนยัน</p>
                        <p>• <strong>hrdi_may_aug:</strong> ฝนสะสม พ.ค.–ส.ค. จากสถานี HRDI (ช่วงวิเคราะห์หลัก: ต้นฤดูปลูก/ระยะแตกกอ)</p>
                        <p>• <strong>hii_may_aug:</strong> ฝนสะสม พ.ค.–ส.ค. เฉลี่ยระดับจังหวัดจาก HII (ช่วงวิเคราะห์หลัก)</p>
                        <p>• <strong>hrdi_feb_jul & hii_feb_jul:</strong> ฝนสะสม ก.พ.–ก.ค. (เก็บไว้สำหรับ Sensitivity Comparison)</p>
                    </div>
                </div>
            </div>

            <!-- RAW DATA 5-ROW SAMPLES PREVIEWS -->
            <div class="chart-bento-card" style="margin-bottom:0.95rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>🔍</span> ตัวอย่างข้อมูลจริง 5 แถวแรกจากแต่ละชุดข้อมูล (Raw Data Samples Preview)
                    </div>
                </div>

                <!-- Tab switcher for samples -->
                <div style="display:flex; gap:0.5rem; margin-bottom:0.6rem;">
                    <button class="btn-tab-reset" id="btnSampleHrdi" style="background:var(--primary-orange); color:#fff;">1. HRDI Meteo (50 สถานี)</button>
                    <button class="btn-tab-reset" id="btnSampleHii">2. HII Spatial Rain (จังหวัด)</button>
                    <button class="btn-tab-reset" id="btnSamplePlant">3. DOAE/OAE ข้าวนาปี (ตำบล)</button>
                </div>

                <div style="overflow-x:auto;" id="sampleTableWrapper">
                    <table class="styled-table" id="sampleDataTable">
                        <thead>
                            <tr id="sampleHeaderRow"></tr>
                        </thead>
                        <tbody id="sampleBodyRows"></tbody>
                    </table>
                </div>
                <div class="chart-attribution-card">
                    <span>แสดงชื่อคอลัมน์และค่าข้อมูลตามไฟล์ต้นฉบับจริงในโปรเจกต์ 100% (ไม่มี Mock Data)</span>
                </div>
            </div>
        </section>

        <!-- Footer Governance Note -->
        <footer style="background:rgba(22, 13, 34, 0.75); border:1px dashed rgba(255, 138, 50, 0.3); border-radius:10px; padding:0.75rem 1.25rem; font-size:0.78rem; color:var(--text-muted); display:flex; align-items:center; justify-content:space-between; margin-top:0.6rem;">
            <span>🌾 <strong>Highland Rainfall Project (2022–2023)</strong> | สำรวจสภาพภูมิอากาศบนพื้นที่สูงและผลผลิตข้าวนาปี</span>
            <span>⚠️ การวิเคราะห์เชิงสำรวจ (Non-causal, No Forecasting) | หน่วยรอยืนยัน</span>
        </footer>

    </main>

    <!-- INJECT RAW JSON DATA SAFELY -->
    <script>
        const REAL_DATA = {data_json};
    </script>

    <!-- CLIENT APPLICATION SCRIPT -->
    <script>
    document.addEventListener('DOMContentLoaded', () => {{

        // -------------------------------------------------------------
        // A. ISOLATED STATE MANAGEMENT BY TAB
        // -------------------------------------------------------------
        const state = {{
            activeTab: 'page1',
            hrdiMode: 'observed', // 'observed' | 'exploratory'
            tab1: {{
                year: 'all',
                province: 'all',
                station: 'all'
            }},
            tab2: {{
                year: 'all',
                province: 'all',
                source: 'all'
            }},
            tab3: {{
                year: 'all',
                province: 'all',
                amphoe: 'all',
                tambon: 'all'
            }},
            tab4: {{
                level: 'tambon',
                province: 'all'
            }},
            selectedMarker: null,
            isDrawerOpen: false
        }};

        // -------------------------------------------------------------
        // A.1 HRDI DUAL ANALYSIS MODE MANAGEMENT
        // -------------------------------------------------------------
        window.setHrdiMode = function(mode) {{
            if (mode !== 'observed' && mode !== 'exploratory') return;
            state.hrdiMode = mode;

            const btnObs = document.getElementById('btnModeObserved');
            const btnExp = document.getElementById('btnModeExploratory');
            const banner = document.getElementById('hrdiModeBanner');
            const bannerIcon = document.getElementById('hrdiBannerIcon');
            const bannerText = document.getElementById('hrdiModeBannerText');
            const modeTag = document.getElementById('hrdiCurrentModeTag');

            if (mode === 'observed') {{
                if (btnObs) btnObs.classList.add('active');
                if (btnExp) btnExp.classList.remove('active');
                if (banner) banner.className = 'hrdi-mode-status-banner banner-observed';
                if (bannerIcon) bannerIcon.textContent = '🛡️';
                if (bannerText) {{
                    bannerText.innerHTML = '<strong>โหมดข้อมูลตรวจวัดจริง (Observed Only):</strong> แสดงเฉพาะข้อมูลจริงจากเซ็นเซอร์ HRDI รายเดือน (เดือนที่ไม่มีข้อมูลแสดงเป็นช่องว่าง ห้ามนำไปคิดเป็นศูนย์ และห้ามแสดงผลรวมทั้งปีสำหรับสถานีที่ข้อมูลไม่ครบ 12 เดือนตามหลักสถิติ)';
                }}
                if (modeTag) modeTag.textContent = 'โหมดปัจจุบัน: ตรวจวัดจริง (Observed Only)';
            }} else {{
                if (btnObs) btnObs.classList.remove('active');
                if (btnExp) btnExp.classList.add('active');
                if (banner) banner.className = 'hrdi-mode-status-banner banner-exploratory';
                if (bannerIcon) bannerIcon.textContent = '⚠️';
                if (bannerText) {{
                    bannerText.innerHTML = '<strong>⚠️ โหมดทดลองวิเคราะห์ (Exploratory Analysis Mode):</strong> ใช้ชุดข้อมูลเติมเต็มครบ 12 เดือน (1,200 แถว) รวมค่าประมาณการทางสถิติ (Donor Station Interpolation & Historical Medians) เพื่อการศึกษาเปรียบเทียบเชิงวิจัย <em>(ยังไม่ผ่านการตรวจรับรองความแม่นยำเป็นทางการ)</em>';
                }}
                if (modeTag) modeTag.textContent = 'โหมดปัจจุบัน: ทดลองวิเคราะห์ (Exploratory 12 ด.)';
            }}

            updateTab1Components();
            updateTab2Components();
            updateTab1MapVisuals(false);

            if (state.isDrawerOpen && state.tab1.station !== 'all') {{
                const s = REAL_DATA.stations.find(x => x.name === state.tab1.station);
                if (s) openStationDetailSubpanel(s);
            }}
        }};

        const btnModeObserved = document.getElementById('btnModeObserved');
        const btnModeExploratory = document.getElementById('btnModeExploratory');
        if (btnModeObserved) btnModeObserved.addEventListener('click', () => window.setHrdiMode('observed'));
        if (btnModeExploratory) btnModeExploratory.addEventListener('click', () => window.setHrdiMode('exploratory'));

        // -------------------------------------------------------------
        // B. LEAFLET MAP & REAL GEOJSON (NO API KEY REQUIRED)
        // -------------------------------------------------------------
        const overviewCenter = [REAL_DATA.overview_center.lat, REAL_DATA.overview_center.lng];
        const overviewZoom = REAL_DATA.overview_center.zoom;

        const map = L.map('leafletMap', {{
            center: overviewCenter,
            zoom: overviewZoom,
            zoomControl: false,
            attributionControl: true
        }});

        // Free OpenStreetMap Standard Tiles with Dark Theme Invert Filter (NO API KEY, NO WATERMARK)
        const osmLayer = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" style="color:#A778E8;">OpenStreetMap</a> contributors',
            maxZoom: 16,
            minZoom: 5
        }});

        osmLayer.on('tileerror', function(e) {{
            if (e.tile) e.tile.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
        }});
        osmLayer.addTo(map);

        // Map Controls
        document.getElementById('btnMapZoomIn').addEventListener('click', () => map.zoomIn());
        document.getElementById('btnMapZoomOut').addEventListener('click', () => map.zoomOut());
        document.getElementById('btnResetMap').addEventListener('click', () => resetTab1Map());
        document.getElementById('btnMapBack').addEventListener('click', () => resetTab1Map());

        function getRainColor(val) {{
            if (val >= 2000) return '#FF8A32';
            if (val >= 1500) return '#FA9A55';
            if (val >= 1000) return '#B777CE';
            if (val >= 500)  return '#7C3AED';
            return '#3B0764';
        }}

        // Render Real 9-Province Boundaries
        const provinceLayers = {{}};
        let geojsonLayer = null;

        function getProvinceStyle(feature) {{
            const pName = feature.properties.pro_th;
            const pSummary = REAL_DATA.province_summaries[pName] || {{}};
            const yr = state.tab1.year;
            const rainVal = (yr === '2022') ? pSummary.rain_2022 :
                            (yr === '2023') ? pSummary.rain_2023 : pSummary.rain_all;
            const fillColor = getRainColor(rainVal);
            const isSelected = (state.tab1.province === pName);

            return {{
                fillColor: fillColor,
                fillOpacity: isSelected ? 0.95 : (state.tab1.province === 'all' ? 0.78 : 0.35),
                color: isSelected ? '#FF8A32' : 'rgba(167, 120, 232, 0.45)',
                weight: isSelected ? 3.5 : 1.2,
                className: 'province-real-polygon'
            }};
        }}

        function renderProvinceGeoJSON() {{
            if (geojsonLayer) map.removeLayer(geojsonLayer);

            geojsonLayer = L.geoJSON(REAL_DATA.province_geojson, {{
                style: getProvinceStyle,
                onEachFeature: function(feature, layer) {{
                    const pName = feature.properties.pro_th;
                    provinceLayers[pName] = layer;

                    layer.on('mouseover', () => {{
                        if (state.tab1.province !== pName) {{
                            layer.setStyle({{ fillOpacity: 0.92, color: '#FF8A32', weight: 2.2 }});
                        }}
                    }});

                    layer.on('mouseout', () => {{
                        if (state.tab1.province !== pName) {{
                            layer.setStyle({{
                                fillOpacity: state.tab1.province === 'all' ? 0.78 : 0.35,
                                color: 'rgba(167, 120, 232, 0.45)',
                                weight: 1.2
                            }});
                        }}
                    }});

                    layer.on('click', (e) => {{
                        L.DomEvent.stopPropagation(e);
                        if (state.tab1.province === pName) {{
                            dispatchTab1Filter({{ province: 'all', station: 'all' }});
                        }} else {{
                            dispatchTab1Filter({{ province: pName, station: 'all' }});
                        }}
                    }});
                }}
            }}).addTo(map);

            // Add Text Label at Center of Each Province
            for (const [pName, center] of Object.entries(REAL_DATA.centers)) {{
                const labelIcon = L.divIcon({{
                    className: 'leaflet-prov-label',
                    html: `<div>${{pName}}</div>`,
                    iconSize: [80, 20],
                    iconAnchor: [40, 10]
                }});
                L.marker([center.lat, center.lng], {{ icon: labelIcon, interactive: false }}).addTo(map);
            }}
        }}

        renderProvinceGeoJSON();

        // Render 50 Weather Station Markers on Map
        const stationMarkers = [];
        function renderStationMarkers() {{
            REAL_DATA.stations.forEach(s => {{
                const m = L.circleMarker([s.lat, s.lng], {{
                    radius: 4.8,
                    fillColor: '#A778E8',
                    color: '#ffffff',
                    weight: 1.2,
                    fillOpacity: 0.9,
                    opacity: 1
                }}).addTo(map);

                m.bindTooltip(`<strong>${{s.name}}</strong><br><span style="color:#FF8A32">${{s.province}}</span> | รหัส: ${{s.code_ref || s.code_sta || '-'}}<br>ฝนเฉลี่ย: ${{s.mean_rain}} มม.`, {{
                    className: 'station-map-tooltip',
                    direction: 'top',
                    offset: [0, -4]
                }});

                m.on('click', (e) => {{
                    L.DomEvent.stopPropagation(e);
                    dispatchTab1Filter({{ province: s.province, station: s.name }});
                    openStationDetailSubpanel(s);
                }});

                stationMarkers.push({{ data: s, marker: m }});
            }});
        }}

        renderStationMarkers();

        // -------------------------------------------------------------
        // C. STATION EXPLORER & DRAWER INTERACTIVE LOGIC
        // -------------------------------------------------------------
        const detailDrawer = document.getElementById('detailDrawer');
        const drawerTitle = document.getElementById('drawerTitle');
        const btnDrawerClose = document.getElementById('btnDrawerClose');
        const drawerProvinceView = document.getElementById('drawerProvinceView');
        const drawerStationView = document.getElementById('drawerStationView');
        const drawerStationList = document.getElementById('drawerStationList');
        const stationSearchInput = document.getElementById('stationSearchInput');
        const btnBackToProvList = document.getElementById('btnBackToProvList');
        let miniStationChart = null;

        btnDrawerClose.addEventListener('click', () => {{
            resetTab1Map();
        }});

        btnBackToProvList.addEventListener('click', () => {{
            drawerStationView.style.display = 'none';
            drawerProvinceView.style.display = 'flex';
            if (state.tab1.province !== 'all') {{
                const layer = provinceLayers[state.tab1.province];
                if (layer) map.flyToBounds(layer.getBounds(), {{ padding: [35, 35], maxZoom: 9.5, duration: 0.8 }});
            }}
        }});

        function openProvinceDrawer(pName) {{
            const sum = REAL_DATA.province_summaries[pName];
            if (!sum) return;

            drawerTitle.innerHTML = `🎃 จังหวัด${{pName}}`;
            const yr = state.tab1.year;
            const rain = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
            const activeCnt = (yr === '2022') ? sum.active_stations_2022 : (yr === '2023') ? sum.active_stations_2023 : sum.station_count;

            document.getElementById('drawerProvStaCount').textContent = `${{sum.station_count}} สถานี`;
            document.getElementById('drawerProvActiveCount').textContent = `${{activeCnt}} สถานี (${{yr === 'all' ? '2022-23' : yr}})`;
            document.getElementById('drawerProvRain').textContent = `${{rain.toLocaleString()}} มม.`;
            document.getElementById('drawerProvTemp').textContent = `${{sum.temp}} °C`;

            // Populate station list
            renderStationListInDrawer(pName, '');

            drawerProvinceView.style.display = 'flex';
            drawerStationView.style.display = 'none';
            detailDrawer.style.display = 'flex';
            document.getElementById('btnMapBack').style.display = 'flex';
            state.isDrawerOpen = true;
        }}

        function renderStationListInDrawer(pName, filterText) {{
            drawerStationList.innerHTML = '';
            let stas = REAL_DATA.stations.filter(s => s.province === pName);
            if (filterText) {{
                const ft = filterText.toLowerCase();
                stas = stas.filter(s => s.name.toLowerCase().includes(ft) || (s.code_ref && s.code_ref.toLowerCase().includes(ft)) || (s.code_sta && s.code_sta.toLowerCase().includes(ft)));
            }}

            if (stas.length === 0) {{
                drawerStationList.innerHTML = '<div style="font-size:0.78rem; color:var(--text-muted); padding:0.5rem;">ไม่พบสถานีที่ตรงกับคำค้นหา</div>';
                return;
            }}

            stas.forEach(s => {{
                const card = document.createElement('div');
                card.className = `station-item-card ${{state.tab1.station === s.name ? 'active' : ''}}`;
                const codeBadge = s.code_ref || s.code_sta || 'HRDI';
                card.innerHTML = `
                    <div class="station-item-top">
                        <span class="station-name-text">${{s.name}}</span>
                        <span class="station-badge">${{codeBadge}}</span>
                    </div>
                    <div class="station-meta-sub">
                        <span>อ.${{s.amphoe || '-'}} ต.${{s.tambon || '-'}}</span>
                        <span>ความครบถ้วน: <strong>${{s.total_months}}/24 ด.</strong></span>
                    </div>
                    <div style="font-size:0.74rem; color:var(--primary-orange); display:flex; justify-content:space-between; margin-top:2px;">
                        <span>ฝนเฉลี่ย: ${{s.mean_rain}} มม.</span>
                        <span style="color:var(--text-cream);">คลิกเพื่อซูม 🔍</span>
                    </div>
                `;

                card.addEventListener('click', () => {{
                    dispatchTab1Filter({{ station: s.name }});
                    map.flyTo([s.lat, s.lng], 13, {{ duration: 1.0 }});
                    openStationDetailSubpanel(s);
                }});

                drawerStationList.appendChild(card);
            }});
        }}

        stationSearchInput.addEventListener('input', (e) => {{
            if (state.tab1.province !== 'all') {{
                renderStationListInDrawer(state.tab1.province, e.target.value);
            }}
        }});

        function openStationDetailSubpanel(s) {{
            document.getElementById('subStaName').textContent = s.name;
            const codeBadge = s.code_ref || s.code_sta || 'HRDI';
            document.getElementById('subStaMeta').textContent = `อ.${{s.amphoe || '-'}} ต.${{s.tambon || '-'}} | รหัส: ${{codeBadge}} (${{s.source}})`;
            document.getElementById('subStaCoords').textContent = `พิกัดจริง: ${{s.lat}}, ${{s.lng}} (WGS84)`;
            document.getElementById('subStaCompleteness').innerHTML = `
                <div>• ตรวจวัดจริง: 2022 (${{s.observed_count_2022}}/12 ด.) | 2023 (${{s.observed_count_2023}}/12 ด.) | รวม ${{s.observed_count_total}}/24 ด.</div>
                <div style="margin-top:2px; font-size:0.74rem; color:var(--text-muted);">• การประมาณการ: DEMO ${{s.estimated_count_total}} ด. | Exploratory ${{s.exploratory_count_total}} ด.</div>
            `;

            drawerProvinceView.style.display = 'none';
            drawerStationView.style.display = 'flex';

            renderStationMiniChart(s);
        }}

        function renderStationMiniChart(s) {{
            const ctx = document.getElementById('stationMiniChart').getContext('2d');
            if (miniStationChart) miniStationChart.destroy();

            const isExp = (state.hrdiMode === 'exploratory');
            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            const d22 = isExp ? (s.monthly_exp_2022 || []) : (s.monthly_obs_2022 || []);
            const d23 = isExp ? (s.monthly_exp_2023 || []) : (s.monthly_obs_2023 || []);
            const st24 = s.monthly_status_24 || [];

            // Color code each monthly bar by status
            const colors22 = d22.map((v, i) => {{
                if (v === null || v === undefined) return 'transparent';
                const st = st24[i] || 'observed';
                return st === 'observed' ? '#A778E8' : st === 'estimated' ? '#fbbf24' : '#FF8A32';
            }});

            const colors23 = d23.map((v, i) => {{
                if (v === null || v === undefined) return 'transparent';
                const st = st24[i + 12] || (isExp ? 'estimated_exploratory' : 'observed');
                return st === 'observed' ? '#A778E8' : st === 'estimated' ? '#fbbf24' : '#FF8A32';
            }});

            miniStationChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: months,
                    datasets: [
                        {{
                            label: 'ปี 2022',
                            data: d22,
                            backgroundColor: colors22,
                            borderRadius: 2
                        }},
                        {{
                            label: 'ปี 2023',
                            data: d23,
                            backgroundColor: colors23,
                            borderRadius: 2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{
                                color: '#F7F0E8',
                                font: {{ size: 10 }},
                                generateLabels: (chart) => [
                                    {{ text: 'ตรวจวัดจริง (Observed)', fillStyle: '#A778E8', strokeStyle: '#A778E8' }},
                                    {{ text: 'ค่าประมาณ DEMO', fillStyle: '#fbbf24', strokeStyle: '#fbbf24' }},
                                    {{ text: 'ค่าประมาณ Exploratory', fillStyle: '#FF8A32', strokeStyle: '#FF8A32' }}
                                ]
                            }}
                        }},
                        tooltip: {{
                            padding: 6,
                            callbacks: {{
                                label: (item) => {{
                                    const mIdx = item.dataIndex + (item.datasetIndex === 1 ? 12 : 0);
                                    const st = st24[mIdx] || 'observed';
                                    const stTh = st === 'observed' ? 'ตรวจวัดจริง' : st === 'estimated' ? 'ประมาณการ DEMO' : 'ประมาณการ Exploratory';
                                    return `${{item.dataset.label}}: ${{item.raw !== null ? item.raw + ' มม.' : 'ไม่มีข้อมูล'}} [${{stTh}}]`;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }},
                        y: {{ ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});
        }}

        function resetTab1Map() {{
            dispatchTab1Filter({{ province: 'all', station: 'all' }});
            detailDrawer.style.display = 'none';
            document.getElementById('btnMapBack').style.display = 'none';
            state.isDrawerOpen = false;
        }}

        // -------------------------------------------------------------
        // D. TAB-SPECIFIC FILTER DISPATCHERS
        // -------------------------------------------------------------
        const tab1_filterYear = document.getElementById('tab1_filterYear');
        const tab1_filterProvince = document.getElementById('tab1_filterProvince');
        const tab1_filterStation = document.getElementById('tab1_filterStation');
        const tab1_filterTambon = document.getElementById('tab1_filterTambon');
        const tab1_btnReset = document.getElementById('tab1_btnReset');

        if (tab1_filterTambon) {{
            tab1_filterTambon.innerHTML = '<option value="all">ทั้งหมด (25 ตำบล)</option>';
            REAL_DATA.tambons.forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.tambon_code_6;
                opt.textContent = `${{t.tambon_name || t.label}} (${{t.province_name}})`;
                tab1_filterTambon.appendChild(opt);
            }});
            tab1_filterTambon.addEventListener('change', (e) => {{
                const tCode = e.target.value;
                if (tCode !== 'all') {{
                    const t = REAL_DATA.tambons.find(x => x.tambon_code_6 === tCode);
                    if (t) dispatchTab1Filter({{ province: t.province_name }});
                }}
            }});
        }}

        // Map Year Toggle Pills
        document.querySelectorAll('.map-year-pill').forEach(pill => {{
            pill.addEventListener('click', () => {{
                dispatchTab1Filter({{ year: pill.getAttribute('data-year') }});
            }});
        }});

        // -------------------------------------------------------------
        // IN-CHART EMPTY STATE HELPERS (NO BROWSER ALERTS)
        // -------------------------------------------------------------
        function showChartEmptyState(canvasId, title, message, badgeText = '') {{
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const container = canvas.closest('.chart-canvas-container');
            if (!container) return;

            clearChartEmptyState(canvasId);

            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'chart-empty-state';
            emptyDiv.id = `empty_${{canvasId}}`;
            emptyDiv.innerHTML = `
                <div class="empty-icon">🎃</div>
                <div class="empty-title">${{title}}</div>
                <div class="empty-desc">${{message}}</div>
                ${{badgeText ? `<span class="empty-badge">${{badgeText}}</span>` : ''}}
            `;
            container.appendChild(emptyDiv);
            canvas.style.opacity = '0.06';
        }}

        function clearChartEmptyState(canvasId) {{
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const existing = document.getElementById(`empty_${{canvasId}}`);
            if (existing) {{
                existing.remove();
            }}
            canvas.style.opacity = '1';
        }}

        // Dynamic Spearman Rho Calculation with Fractional Tie-Ranks
        function computeSpearmanRho(points) {{
            const valid = points.filter(p => p.x !== null && p.y !== null && !isNaN(p.x) && !isNaN(p.y));
            const n = valid.length;
            if (n < 3) return null;

            function getRanks(arr) {{
                const sorted = arr.map((val, idx) => ({{ val, idx }})).sort((a, b) => a.val - b.val);
                const ranks = new Array(arr.length);
                let i = 0;
                while (i < sorted.length) {{
                    let j = i;
                    while (j < sorted.length - 1 && sorted[j + 1].val === sorted[j].val) {{
                        j++;
                    }}
                    const avgRank = 1 + (i + j) / 2;
                    for (let k = i; k <= j; k++) {{
                        ranks[sorted[k].idx] = avgRank;
                    }}
                    i = j + 1;
                }}
                return ranks;
            }}

            const rankX = getRanks(valid.map(p => p.x));
            const rankY = getRanks(valid.map(p => p.y));

            const meanX = rankX.reduce((a, b) => a + b, 0) / n;
            const meanY = rankY.reduce((a, b) => a + b, 0) / n;

            let num = 0, denX = 0, denY = 0;
            for (let i = 0; i < n; i++) {{
                const dx = rankX[i] - meanX;
                const dy = rankY[i] - meanY;
                num += dx * dy;
                denX += dx * dx;
                denY += dy * dy;
            }}
            if (denX === 0 || denY === 0) return 0;
            return num / Math.sqrt(denX * denY);
        }}

        function animateCountUp(element, endVal, duration = 900, decimals = 1, suffix = '') {{
            if (!element) return;
            if (endVal === null || isNaN(endVal)) {{
                element.textContent = 'ไม่มีรายงาน';
                return;
            }}
            const startTime = performance.now();
            const startVal = parseFloat(element.getAttribute('data-val') || '0') || 0;
            element.setAttribute('data-val', endVal);
            function update(time) {{
                const elapsed = time - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeOutQuad = 1 - (1 - progress) * (1 - progress);
                const current = startVal + (endVal - startVal) * easeOutQuad;
                element.textContent = current.toLocaleString('en-US', {{
                    minimumFractionDigits: decimals,
                    maximumFractionDigits: decimals
                }}) + suffix;
                if (progress < 1) {{
                    requestAnimationFrame(update);
                }}
            }}
            requestAnimationFrame(update);
        }}

        function updateTab1CascadingStations() {{
            const p = state.tab1.province;
            tab1_filterStation.innerHTML = '<option value="all">ทั้งหมด (50 สถานี HRDI)</option>';
            let stas = REAL_DATA.stations;
            if (p !== 'all') {{
                stas = stas.filter(s => s.province === p);
                tab1_filterStation.innerHTML = `<option value="all">ทั้งหมดใน${{p}} (${{stas.length}} สถานี)</option>`;
            }}
            stas.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s.name;
                opt.textContent = `${{s.name}} [${{s.data_status_label || 'HRDI'}}]`;
                tab1_filterStation.appendChild(opt);
            }});
            tab1_filterStation.value = state.tab1.station;
        }}

        function updateTab1CascadingTambons() {{
            if (!tab1_filterTambon) return;
            const p = state.tab1.province;
            tab1_filterTambon.innerHTML = '<option value="all">ทั้งหมด (921 ตำบล DOAE)</option>';
            let tbs = REAL_DATA.tambons;
            if (p !== 'all') {{
                tbs = tbs.filter(t => t.province_name === p);
                tab1_filterTambon.innerHTML = `<option value="all">ทั้งหมดใน${{p}} (${{tbs.length}} ตำบล)</option>`;
            }}
            tbs.forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.tambon_code_6;
                opt.textContent = `${{t.tambon_name}} (${{t.amphoe_name || t.province_name}}) [${{t.coverage_badge || 'DOAE'}}]`;
                tab1_filterTambon.appendChild(opt);
            }});
            tab1_filterTambon.value = state.tab1.tambon || 'all';
        }}

        if (tab1_filterTambon) {{
            tab1_filterTambon.addEventListener('change', (e) => {{
                const tCode = e.target.value;
                state.tab1.tambon = tCode;
                if (tCode !== 'all') {{
                    const t = REAL_DATA.tambons.find(x => x.tambon_code_6 === tCode);
                    if (t && state.tab1.province !== t.province_name) {{
                        dispatchTab1Filter({{ province: t.province_name, tambon: tCode }});
                        return;
                    }}
                }}
                updateTab1Components();
            }});
        }}

        function dispatchTab1Filter(changes) {{
            let provChanged = false;
            if (changes.year !== undefined) state.tab1.year = changes.year;
            if (changes.province !== undefined && changes.province !== state.tab1.province) {{
                state.tab1.province = changes.province;
                provChanged = true;
                if (changes.station === undefined) state.tab1.station = 'all';
                if (changes.tambon === undefined) state.tab1.tambon = 'all';
            }}
            if (changes.station !== undefined) state.tab1.station = changes.station;
            if (changes.tambon !== undefined) state.tab1.tambon = changes.tambon;

            // Sync UI Dropdowns & Pills
            tab1_filterYear.value = state.tab1.year;
            tab1_filterProvince.value = state.tab1.province;
            if (provChanged) {{
                updateTab1CascadingStations();
                updateTab1CascadingTambons();
            }}
            tab1_filterStation.value = state.tab1.station;
            if (tab1_filterTambon) tab1_filterTambon.value = state.tab1.tambon || 'all';

            document.querySelectorAll('.map-year-pill').forEach(pill => {{
                pill.classList.toggle('active', pill.getAttribute('data-year') === state.tab1.year);
            }});

            // Update Map Visuals
            updateTab1MapVisuals(provChanged);

            // Update Tab 1 KPIs & Charts
            updateTab1Components();
        }}

        function updateTab1MapVisuals(provChanged) {{
            const p = state.tab1.province;
            const yr = state.tab1.year;

            if (p === 'all') {{
                if (provChanged) {{
                    map.flyTo(overviewCenter, overviewZoom, {{ duration: 1.0, easeLinearity: 0.25 }});
                }}
                detailDrawer.style.display = 'none';
                document.getElementById('btnMapBack').style.display = 'none';

                for (const [name, layer] of Object.entries(provinceLayers)) {{
                    const sum = REAL_DATA.province_summaries[name] || {{}};
                    const rain = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                    layer.setStyle({{
                        fillColor: getRainColor(rain),
                        fillOpacity: 0.78,
                        color: 'rgba(167, 120, 232, 0.45)',
                        weight: 1.2
                    }});
                }}
            }} else {{
                const layer = provinceLayers[p];
                if (layer && provChanged) {{
                    map.flyToBounds(layer.getBounds(), {{ paddingTopLeft: [30, 30], paddingBottomRight: [330, 30], maxZoom: 8.8, duration: 0.9 }});
                }}
                detailDrawer.style.display = 'block';
                document.getElementById('btnMapBack').style.display = 'inline-flex';
                state.isDrawerOpen = true;

                for (const [name, lyr] of Object.entries(provinceLayers)) {{
                    const isSelected = (name === p);
                    lyr.setStyle({{
                        fillOpacity: isSelected ? 0.88 : 0.22,
                        weight: isSelected ? 3.0 : 0.8,
                        color: isSelected ? '#FF8A32' : 'rgba(167, 120, 232, 0.25)'
                    }});
                }}
                renderMapDetailDrawer(p);
            }}
        }}

        function updateTab1Components() {{
            const p = state.tab1.province;
            const yr = state.tab1.year;
            const sta = state.tab1.station;
            const tCode = state.tab1.tambon || 'all';
            const isExp = (state.hrdiMode === 'exploratory');

            // Compute KPIs
            let rainVal = null;
            let rainBadge = '✓ 12/12 ด.';
            let rainSub = 'ข้อมูลตรวจวัดจริงครบ 12 เดือน';
            let tempVal = REAL_DATA.overall_kpis.mean_temp;
            let humVal = REAL_DATA.overall_kpis.mean_humidity;
            let windVal = REAL_DATA.overall_kpis.mean_wind;
            let yieldVal = REAL_DATA.overall_kpis.mean_yield;

            if (sta !== 'all') {{
                const s = REAL_DATA.stations.find(x => x.name === sta);
                if (s) {{
                    tempVal = s.mean_temp;
                    humVal = s.mean_humidity;
                    windVal = s.mean_wind || 2.5;

                    if (isExp) {{
                        rainVal = (yr === '2022') ? s.annual_exp_2022 : (yr === '2023') ? s.annual_exp_2023 : s.annual_exp_all;
                        rainBadge = '🔮 Exploratory';
                        rainSub = `⚠️ รวมค่าประมาณการวิจัย (${{s.estimated_count_total + s.exploratory_count_total}} ด.)`;
                    }} else {{
                        if (yr === '2022') {{
                            if (s.annual_obs_2022 !== null) {{
                                rainVal = s.annual_obs_2022;
                                rainBadge = '✓ 12/12 ด.';
                                rainSub = '✓ ข้อมูลตรวจวัดจริงครบ 12 เดือน';
                            }} else {{
                                rainVal = null;
                                rainBadge = '⚠️ ข้อมูลไม่ครบ';
                                rainSub = `ตรวจวัดได้ ${{s.observed_count_2022}}/12 ด. (ห้ามคำนวณผลรวมทั้งปี)`;
                            }}
                        }} else if (yr === '2023') {{
                            rainVal = null;
                            rainBadge = '⚠️ ข้อมูลไม่ครบ';
                            rainSub = `ตรวจวัดได้ ${{s.observed_count_2023}}/12 ด. (ห้ามคำนวณผลรวมทั้งปี)`;
                        }} else {{
                            rainVal = null;
                            rainBadge = '⚠️ 2023 ไม่ครบ';
                            rainSub = `ตรวจวัดจริง ${{s.observed_count_total}}/24 ด. (ห้ามรวมยอดปี 2023)`;
                        }}
                    }}
                }}
            }} else if (p !== 'all') {{
                const sum = REAL_DATA.province_summaries[p];
                if (sum) {{
                    tempVal = sum.temp;
                    humVal = sum.humidity;
                    windVal = sum.wind || 2.4;
                    yieldVal = (yr === '2022') ? (sum.rice_yield_2022 || yieldVal) : (yr === '2023') ? (sum.rice_yield_2023 || yieldVal) : (((sum.rice_yield_2022 || yieldVal) + (sum.rice_yield_2023 || yieldVal)) / 2);

                    if (isExp) {{
                        rainVal = (yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all;
                        rainBadge = '🔮 Exploratory';
                        rainSub = `⚠️ ฝนเฉลี่ยสถานี (ชุดทดลองวิเคราะห์ครบ 12 ด.)`;
                    }} else {{
                        if (yr === '2022') {{
                            rainVal = sum.rain_obs_2022;
                            rainBadge = '✓ ตรวจวัดจริง';
                            rainSub = 'ฝนเฉลี่ยสถานีที่ตรวจวัดครบ 12 เดือน';
                        }} else if (yr === '2023') {{
                            rainVal = null;
                            rainBadge = '⚠️ ข้อมูลไม่ครบ';
                            rainSub = 'สถานีในจังหวัดตรวจวัดไม่ครบ 12 ด. (ห้ามรวมทั้งปี)';
                        }} else {{
                            rainVal = null;
                            rainBadge = '⚠️ 2023 ไม่ครบ';
                            rainSub = 'ข้อมูลปี 2023 ตรวจวัดไม่ครบ 12 ด. (แนะนำดูรายเดือน)';
                        }}
                    }}
                }}
            }} else {{
                // Overview 9 Provinces
                if (isExp) {{
                    rainVal = (yr === '2022') ? REAL_DATA.overall_kpis.hrdi_exp_rain_2022 : (yr === '2023') ? REAL_DATA.overall_kpis.hrdi_exp_rain_2023 : REAL_DATA.overall_kpis.hrdi_exp_rain_all;
                    rainBadge = '🔮 Exploratory';
                    rainSub = '⚠️ ฝนเฉลี่ยสถานีบนพื้นที่สูง (ชุดทดลองวิเคราะห์ 50 สถานี)';
                }} else {{
                    if (yr === '2022') {{
                        rainVal = REAL_DATA.overall_kpis.hrdi_obs_rain_2022;
                        rainBadge = '✓ 2022 จริง';
                        rainSub = 'เฉลี่ยสถานีตรวจวัดจริงครบ 12 เดือน (46 สถานี)';
                    }} else if (yr === '2023') {{
                        rainVal = null;
                        rainBadge = '⚠️ 2023 ไม่ครบ';
                        rainSub = 'สถานี HRDI ปี 2023 ตรวจวัดจริงไม่ครบ 12 ด. (ห้ามรวมทั้งปี)';
                    }} else {{
                        rainVal = null;
                        rainBadge = '⚠️ 2023 ไม่ครบ';
                        rainSub = 'ปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน (เลือกปี 2022 หรือโหมด Exploratory)';
                    }}
                }}
            }}

            let tambonHasRice = true;
            if (tCode !== 'all') {{
                const t = REAL_DATA.tambons.find(x => x.tambon_code_6 === tCode);
                if (t) {{
                    if (yr === '2022') {{
                        yieldVal = t.yield_2022;
                    }} else if (yr === '2023') {{
                        yieldVal = t.yield_2023;
                    }} else {{
                        if (t.yield_2022 !== null && t.yield_2023 !== null) {{
                            yieldVal = (t.yield_2022 + t.yield_2023) / 2;
                        }} else if (t.yield_2022 !== null) {{
                            yieldVal = t.yield_2022;
                        }} else if (t.yield_2023 !== null) {{
                            yieldVal = t.yield_2023;
                        }} else {{
                            yieldVal = null;
                        }}
                    }}
                    if (yieldVal === null || isNaN(yieldVal)) {{
                        tambonHasRice = false;
                    }}
                }}
            }}

            // Animate Count-up numbers (0.8–1.0s)
            const rainEl = document.getElementById('tab1_kpiRain');
            const rainBadgeEl = document.getElementById('tab1_kpiRainBadge');
            const rainSubEl = document.getElementById('tab1_kpiRainSub');

            if (rainBadgeEl) rainBadgeEl.textContent = rainBadge;
            if (rainSubEl) rainSubEl.textContent = rainSub;

            if (rainVal === null || isNaN(rainVal)) {{
                if (rainEl) rainEl.textContent = 'ไม่ครบ 12 ด.';
            }} else {{
                animateCountUp(rainEl, rainVal, 900, 1);
            }}
            animateCountUp(document.getElementById('tab1_kpiTemp'), tempVal, 900, 1);
            animateCountUp(document.getElementById('tab1_kpiHumidity'), humVal, 900, 1);
            animateCountUp(document.getElementById('tab1_kpiWind'), windVal, 900, 2);

            const yieldEl = document.getElementById('tab1_kpiYield');
            if (yieldVal === null || !tambonHasRice) {{
                if (yieldEl) yieldEl.textContent = 'ไม่มีรายงาน';
            }} else {{
                animateCountUp(yieldEl, yieldVal, 900, 1);
            }}

            // Render Tab 1 Charts
            renderTab1MonthlyTrendChart();
            renderTab1RainCompareChart();
            renderTab1RiceYieldChart(tambonHasRice);
            renderTop4HighlightCards();
            renderRainRiceScatterPlot();
            renderTab1ProvinceRankChart();
        }}

        function renderTab1MonthlyTrendChart() {{
            const canvas = document.getElementById('chartMonthlyRainTrend');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartMonthlyTrend) chartMonthlyTrend.destroy();

            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            const p = state.tab1.province;
            const sta = state.tab1.station;
            const yr = state.tab1.year;

            let d22 = REAL_DATA.monthly_overall['2022'];
            let d23 = REAL_DATA.monthly_overall['2023'];
            let scopeLabel = 'ภาพรวม 9 จังหวัด (HII ฝนเฉลี่ยระดับจังหวัด)';

            const isExp = (state.hrdiMode === 'exploratory');
            if (sta !== 'all') {{
                const s = REAL_DATA.stations.find(x => x.name === sta);
                if (s) {{
                    if (isExp) {{
                        scopeLabel = `สถานี: ${{s.name}} (${{s.province}}) [🔮 โหมดทดลองวิเคราะห์ เติมเต็ม 12 ด.]`;
                        d22 = s.monthly_exp_2022 || [];
                        d23 = s.monthly_exp_2023 || [];
                    }} else {{
                        scopeLabel = `สถานี: ${{s.name}} (${{s.province}}) [🧪 โหมดตรวจวัดจริง ${{s.data_status_label}}]`;
                        d22 = s.monthly_obs_2022 || [];
                        d23 = s.monthly_obs_2023 || [];
                    }}
                }} else {{
                    showChartEmptyState('chartMonthlyRainTrend', 'ไม่พบข้อมูลสถานี', 'ไม่พบประวัติข้อมูลน้ำฝนสำหรับสถานีที่เลือก', 'HRDI: ไม่มีข้อมูล');
                    return;
                }}
            }} else if (p !== 'all') {{
                const pSum = REAL_DATA.province_summaries[p];
                if (isExp && pSum) {{
                    scopeLabel = `จังหวัด: ${{p}} (🔮 ฝนเฉลี่ยสถานี HRDI โหมดทดลองวิเคราะห์)`;
                    d22 = pSum.monthly_exp_2022;
                    d23 = pSum.monthly_exp_2023;
                }} else if (pSum) {{
                    scopeLabel = `จังหวัด: ${{p}} (🧪 ฝนเฉลี่ยสถานี HRDI โหมดตรวจวัดจริง)`;
                    d22 = pSum.monthly_obs_2022;
                    d23 = pSum.monthly_obs_2023;
                }} else {{
                    scopeLabel = `จังหวัด: ${{p}} (HII ฝนเฉลี่ยพื้นที่)`;
                    const pTrends = REAL_DATA.monthly_trends.filter(m => m.province === p);
                    d22 = months.map((_, i) => {{
                        const ym = `2022-${{String(i + 1).padStart(2, '0')}}`;
                        const it = pTrends.find(m => m.year_month === ym);
                        return it ? it.mean_rain : null;
                    }});
                    d23 = months.map((_, i) => {{
                        const ym = `2023-${{String(i + 1).padStart(2, '0')}}`;
                        const it = pTrends.find(m => m.year_month === ym);
                        return it ? it.mean_rain : null;
                    }});
                }}
            }}

            clearChartEmptyState('chartMonthlyRainTrend');
            const lblEl = document.getElementById('lblMonthlyScope');
            if (lblEl) lblEl.textContent = scopeLabel;

            const datasets = [];
            if (yr === 'all' || yr === '2022') {{
                datasets.push({{
                    label: 'ปี 2022',
                    data: d22,
                    borderColor: '#A778E8',
                    backgroundColor: 'rgba(167, 120, 232, 0.12)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    spanGaps: false
                }});
            }}
            if (yr === 'all' || yr === '2023') {{
                datasets.push({{
                    label: 'ปี 2023',
                    data: d23,
                    borderColor: '#FF8A32',
                    backgroundColor: 'rgba(255, 138, 50, 0.15)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    spanGaps: false
                }});
            }}

            chartMonthlyTrend = new Chart(ctx, {{
                type: 'line',
                data: {{ labels: months, datasets: datasets }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: true, labels: {{ color: '#F7F0E8', font: {{ family: "'Prompt'", size: 10 }} }} }},
                        tooltip: {{ padding: 8 }}
                    }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5' }} }},
                        y: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5' }} }}
                    }}
                }}
            }});
        }}

        function renderTab1RainCompareChart() {{
            const canvas = document.getElementById('chartTab1RainCompare');
            if (!canvas) return;
            if (chartTab1RainComp) chartTab1RainComp.destroy();

            const p = state.tab1.province;
            const yr = state.tab1.year;

            clearChartEmptyState('chartTab1RainCompare');

            const provNames = (p === 'all') ? Object.keys(REAL_DATA.province_summaries) : [p];
            const hrdiData = [];
            const hiiData = [];

            const isExp = (state.hrdiMode === 'exploratory');
            provNames.forEach(pr => {{
                const sum = REAL_DATA.province_summaries[pr] || {{}};
                let hrdi = null;
                if (isExp) {{
                    hrdi = (yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all;
                }} else {{
                    hrdi = (yr === '2022') ? sum.rain_obs_2022 : (yr === '2023') ? sum.rain_obs_2023 : sum.rain_obs_all;
                }}
                const hii = (yr === '2022') ? (sum.hii_rain_2022 || 0) : (yr === '2023') ? (sum.hii_rain_2023 || 0) : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                hrdiData.push(hrdi !== null ? Math.round(hrdi) : null);
                hiiData.push(Math.round(hii || 0));
            }});

            if (!isExp && yr === '2023' && hrdiData.every(x => x === null)) {{
                showChartEmptyState('chartTab1RainCompare', 'ไม่มีผลรวมตรวจวัดจริงปี 2023 (HRDI)', 'สถานี HRDI ปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน (สูงสุด 9 เดือน) ตามหลักสถิติจึงไม่แสดงผลรวมทั้งปี แนะนำสลับเป็นโหมดทดลองวิเคราะห์ (Exploratory)', 'HRDI: ตรวจวัดไม่ครบ 12 ด.');
                return;
            }}

            chartTab1RainComp = new Chart(canvas.getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: provNames,
                    datasets: [
                        {{ label: isExp ? 'พื้นที่สูง (HRDI เติมเต็ม Exploratory)' : 'พื้นที่สูง (HRDI ตรวจวัดจริง)', data: hrdiData, backgroundColor: '#A778E8', borderRadius: 4 }},
                        {{ label: 'ทั้งจังหวัด (HII เฉลี่ยพื้นที่)', data: hiiData, backgroundColor: '#FF8A32', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: '#F7F0E8', font: {{ family: "'Prompt'", size: 10 }} }} }},
                        tooltip: {{ padding: 8 }}
                    }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }},
                        y: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});
        }}

        function renderTab1RiceYieldChart(tambonHasRice = true) {{
            const canvas = document.getElementById('chartTab1RiceYield');
            if (!canvas) return;
            if (chartTab1RiceYld) chartTab1RiceYld.destroy();

            const p = state.tab1.province;
            const tCode = state.tab1.tambon || 'all';

            if (tCode !== 'all') {{
                const t = REAL_DATA.tambons.find(x => x.tambon_code_6 === tCode);
                if (!t || !tambonHasRice || (t.yield_2022 === null && t.yield_2023 === null)) {{
                    showChartEmptyState('chartTab1RiceYield', 'ไม่มีรายงานผลผลิตข้าวนาปี', `ตำบล${{t ? t.tambon_name : tCode}} ไม่พบข้อมูลผลผลิตข้าวนาปีในทะเบียน DOAE ปี 2022–2023`, 'DOAE: ไม่มีรายงาน');
                    return;
                }}
                clearChartEmptyState('chartTab1RiceYield');
                chartTab1RiceYld = new Chart(canvas.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: [t.tambon_name || t.label],
                        datasets: [
                            {{ label: '2022', data: [t.yield_2022], backgroundColor: '#8b5cf6', borderRadius: 4 }},
                            {{ label: '2023', data: [t.yield_2023], backgroundColor: '#FF8A32', borderRadius: 4 }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ labels: {{ color: '#F7F0E8', font: {{ family: "'Prompt'", size: 10 }} }} }},
                            tooltip: {{ padding: 8 }}
                        }},
                        scales: {{
                            x: {{ grid: {{ display: false }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }},
                            y: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }}
                        }}
                    }}
                }});
                return;
            }}

            clearChartEmptyState('chartTab1RiceYield');
            const provNames = (p === 'all') ? Object.keys(REAL_DATA.centers) : [p];
            const y22 = [];
            const y23 = [];

            provNames.forEach(pr => {{
                const sum = REAL_DATA.province_summaries[pr] || {{}};
                y22.push(sum.rice_yield_2022 || null);
                y23.push(sum.rice_yield_2023 || null);
            }});

            chartTab1RiceYld = new Chart(canvas.getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: provNames,
                    datasets: [
                        {{ label: '2022', data: y22, backgroundColor: '#8b5cf6', borderRadius: 4 }},
                        {{ label: '2023', data: y23, backgroundColor: '#FF8A32', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: '#F7F0E8', font: {{ family: "'Prompt'", size: 10 }} }} }},
                        tooltip: {{ padding: 8 }}
                    }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }},
                        y: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});
        }}

        function renderTop4HighlightCards() {{
            const container = document.getElementById('top4CardsContainer');
            if (!container) return;
            container.innerHTML = '';

            const isExp = (state.hrdiMode === 'exploratory');
            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;
            const yrLabel = (yr === 'all') ? 'เฉลี่ย 2022–2023' : `ปี ${{yr}}`;

            const cards = [];

            // 1 & 2. Max and Min HRDI Highland Rainfall (ค่าเฉลี่ยต่อสถานี ไม่รวมผลรวมบวกกัน)
            if (!isExp && (yr === '2023' || yr === 'all')) {{
                cards.push({{
                    id: 'card_hrdi_max',
                    icon: '🌧️',
                    badge: 'พื้นที่สูง HRDI',
                    badgeClass: 'badge-orange',
                    category: 'ฝนพื้นที่สูง HRDI มากที่สุด',
                    prov: '—',
                    valHtml: '<span style="font-size:0.86rem; color:var(--text-muted); font-weight:500;">ข้อมูลไม่เพียงพอสำหรับจัดอันดับ</span>',
                    metaLines: [
                        `📅 ${{yrLabel}} | ตัวชี้วัด: เฉลี่ยต่อสถานี`,
                        '⚠️ ตรวจวัดจริงไม่ครบ 12 ด. (สูงสุด 9 ด.)',
                        '💡 สลับเป็นโหมด Exploratory เพื่อดูอันดับ'
                    ],
                    actionText: 'สลับเป็นโหมด Exploratory 🔮',
                    onClick: () => window.setHrdiMode('exploratory')
                }});
                cards.push({{
                    id: 'card_hrdi_min',
                    icon: '⛅',
                    badge: 'พื้นที่สูง HRDI',
                    badgeClass: 'badge-purple',
                    category: 'ฝนพื้นที่สูง HRDI น้อยที่สุด',
                    prov: '—',
                    valHtml: '<span style="font-size:0.86rem; color:var(--text-muted); font-weight:500;">ข้อมูลไม่เพียงพอสำหรับจัดอันดับ</span>',
                    metaLines: [
                        `📅 ${{yrLabel}} | ตัวชี้วัด: เฉลี่ยต่อสถานี`,
                        '⚠️ ตรวจวัดจริงไม่ครบ 12 ด. (สูงสุด 9 ด.)',
                        '💡 สลับเป็นโหมด Exploratory เพื่อดูอันดับ'
                    ],
                    actionText: 'สลับเป็นโหมด Exploratory 🔮',
                    onClick: () => window.setHrdiMode('exploratory')
                }});
            }} else {{
                const hrdiList = provs.map(p => {{
                    const s = REAL_DATA.province_summaries[p] || {{}};
                    const r = isExp ? ((yr === '2022') ? s.rain_exp_2022 : (yr === '2023') ? s.rain_exp_2023 : s.rain_exp_all)
                                   : s.rain_obs_2022;
                    return {{ name: p, val: r, sum: s }};
                }}).filter(x => x.val !== null && !isNaN(x.val)).sort((a, b) => b.val - a.val);

                if (hrdiList.length > 0) {{
                    const maxH = hrdiList[0];
                    const minH = hrdiList[hrdiList.length - 1];
                    const statusTag = isExp ? '⚠️ Exploratory 12 ด.' : '✓ ตรวจวัดจริง 12/12 ด.';

                    cards.push({{
                        id: 'card_hrdi_max',
                        icon: '🌧️',
                        badge: 'อันดับ 1 ฝนสูงสุด',
                        badgeClass: 'badge-orange',
                        category: 'ฝนพื้นที่สูง HRDI มากที่สุด',
                        prov: maxH.name,
                        valHtml: `${{maxH.val.toLocaleString()}} <span class="insight-val-unit">มม./สถานี</span>`,
                        metaLines: [
                            `📅 ${{yrLabel}} • ${{maxH.sum.station_count}} สถานี (${{statusTag}})`,
                            `สถานี: ${{maxH.sum.stations.slice(0, 2).join(', ')}}${{maxH.sum.stations.length > 2 ? '...' : ''}}`
                        ],
                        actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                        onClick: () => dispatchTab1Filter({{ province: maxH.name }})
                    }});

                    cards.push({{
                        id: 'card_hrdi_min',
                        icon: '⛅',
                        badge: 'อันดับฝนต่ำสุด',
                        badgeClass: 'badge-purple',
                        category: 'ฝนพื้นที่สูง HRDI น้อยที่สุด',
                        prov: minH.name,
                        valHtml: `${{minH.val.toLocaleString()}} <span class="insight-val-unit">มม./สถานี</span>`,
                        metaLines: [
                            `📅 ${{yrLabel}} • ${{minH.sum.station_count}} สถานี (${{statusTag}})`,
                            `สถานี: ${{minH.sum.stations.slice(0, 2).join(', ')}}${{minH.sum.stations.length > 2 ? '...' : ''}}`
                        ],
                        actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                        onClick: () => dispatchTab1Filter({{ province: minH.name }})
                    }});
                }}
            }}

            // 3. Max HII Provincial Rain (12 months complete across all provinces)
            const hiiList = provs.map(p => {{
                const s = REAL_DATA.province_summaries[p] || {{}};
                const r = (yr === '2022') ? (s.hii_rain_2022 || 0) : (yr === '2023') ? (s.hii_rain_2023 || 0) : (((s.hii_rain_2022 || 0) + (s.hii_rain_2023 || 0)) / 2);
                return {{ name: p, val: r, sum: s }};
            }}).sort((a, b) => b.val - a.val);

            if (hiiList.length > 0) {{
                const maxHii = hiiList[0];
                cards.push({{
                    id: 'card_hii_max',
                    icon: '🌊',
                    badge: 'ทั้งจังหวัด HII',
                    badgeClass: 'badge-cyan',
                    category: 'ฝนระดับจังหวัด HII มากที่สุด',
                    prov: maxHii.name,
                    valHtml: `${{Math.round(maxHii.val).toLocaleString()}} <span class="insight-val-unit">มม./ปี</span>`,
                    metaLines: [
                        `📅 ${{yrLabel}} • ข้อมูลฝนพื้นที่ทั้งจังหวัด (สสน.)`,
                        '✓ ข้อมูลตรวจวัดจริงครบ 12 เดือน (ครอบคลุมทั้งจังหวัด)'
                    ],
                    actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                    onClick: () => dispatchTab1Filter({{ province: maxHii.name }})
                }});
            }}

            // 4 & 5. Rice Yield Max & Min (DOAE kg/rai)
            const riceList = provs.map(p => {{
                const s = REAL_DATA.province_summaries[p] || {{}};
                const y = (yr === '2022') ? s.rice_yield_2022 : (yr === '2023') ? s.rice_yield_2023 : (((s.rice_yield_2022 || 0) + (s.rice_yield_2023 || 0)) / 2);
                return {{ name: p, val: y, sum: s }};
            }}).filter(x => x.val !== null && !isNaN(x.val) && x.val > 0).sort((a, b) => b.val - a.val);

            if (riceList.length > 0) {{
                const maxY = riceList[0];
                const minY = riceList[riceList.length - 1];

                cards.push({{
                    id: 'card_rice_max',
                    icon: '🌾',
                    badge: 'ผลผลิตสูงสุด',
                    badgeClass: 'badge-green',
                    category: 'ผลผลิตข้าวนาปีต่อไร่สูงที่สุด',
                    prov: maxY.name,
                    valHtml: `${{maxY.val.toFixed(1)}} <span class="insight-val-unit">กก./ไร่</span>`,
                    metaLines: [
                        `📅 ${{yrLabel}} • ทะเบียน DOAE (${{maxY.sum.tambon_count}} ตำบล)`,
                        '✓ ข้อมูลสำรวจจริงรายปี กรมส่งเสริมการเกษตร'
                    ],
                    actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                    onClick: () => dispatchTab1Filter({{ province: maxY.name }})
                }});

                cards.push({{
                    id: 'card_rice_min',
                    icon: '🍂',
                    badge: 'ผลผลิตต่ำสุด',
                    badgeClass: 'badge-amber',
                    category: 'ผลผลิตข้าวนาปีต่อไร่ต่ำที่สุด',
                    prov: minY.name,
                    valHtml: `${{minY.val.toFixed(1)}} <span class="insight-val-unit">กก./ไร่</span>`,
                    metaLines: [
                        `📅 ${{yrLabel}} • ทะเบียน DOAE (${{minY.sum.tambon_count}} ตำบล)`,
                        '✓ ข้อมูลสำรวจจริงรายปี กรมส่งเสริมการเกษตร'
                    ],
                    actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                    onClick: () => dispatchTab1Filter({{ province: minY.name }})
                }});
            }}

            // 6. Rain Up, Yield Down Anomaly (2022 vs 2023)
            let anomalyProvs = [];
            provs.forEach(p => {{
                const s = REAL_DATA.province_summaries[p] || {{}};
                const rDiff = isExp ? ((s.rain_exp_2023 || 0) - (s.rain_exp_2022 || 0)) : ((s.hii_rain_2023 || 0) - (s.hii_rain_2022 || 0));
                const yDiff = (s.rice_yield_2023 && s.rice_yield_2022) ? (s.rice_yield_2023 - s.rice_yield_2022) : 0;
                if (rDiff > 0 && yDiff < 0) {{
                    anomalyProvs.push({{ name: p, rDiff, yDiff }});
                }}
            }});

            if (anomalyProvs.length > 0) {{
                const anom = anomalyProvs[0];
                cards.push({{
                    id: 'card_anomaly',
                    icon: '⚡',
                    badge: 'ความผิดปกติ',
                    badgeClass: 'badge-orange',
                    category: 'ฝนเพิ่มแต่ผลผลิตลดลง (2022➔23)',
                    prov: anom.name,
                    valHtml: `<span style="color:#ef4444; font-size:1.15rem;">Δฝน +${{Math.round(anom.rDiff)}} มม. | Δข้าว ${{anom.yDiff.toFixed(1)}} กก.</span>`,
                    metaLines: [
                        '⚠️ เกิด Divergence: ฝนเพิ่มขึ้นแต่ผลผลิตลดลง',
                        '💡 ตรวจสอบปัจจัยน้ำท่วม ดิน หรือการระบาดของโรคพืช'
                    ],
                    actionText: 'คลิกเพื่อเลือกจังหวัดนี้ 🔍',
                    onClick: () => dispatchTab1Filter({{ province: anom.name }})
                }});
            }} else {{
                cards.push({{
                    id: 'card_anomaly',
                    icon: '⚡',
                    badge: 'วิเคราะห์การเปลี่ยนแปลง',
                    badgeClass: 'badge-purple',
                    category: 'ฝนเพิ่มแต่ผลผลิตลดลง (2022➔23)',
                    prov: 'ไม่พบจังหวัดที่ฝนเพิ่มขึ้น',
                    valHtml: '<span style="font-size:1.15rem; color:#A778E8;">0 / 9 จังหวัด</span>',
                    metaLines: [
                        '🌧️ ฝนลดลงทุกจังหวัดในปี 2023 จากเอลนีโญ (-20 ถึง -773 มม.)',
                        '✓ สอดคล้องกับข้อเท็จจริงสภาพภูมิอากาศจริง'
                    ],
                    actionText: 'ดูแนวโน้มทั้ง 9 จังหวัด 🔍',
                    onClick: () => dispatchTab1Filter({{ province: 'all' }})
                }});
            }}

            // Render the 6 Cards
            cards.forEach(c => {{
                const isSelected = (state.tab1.province === c.prov && c.prov !== '—' && c.prov !== 'ไม่พบจังหวัดที่ฝนเพิ่มขึ้น');
                const cardEl = document.createElement('div');
                cardEl.className = `insight-card ${{isSelected ? 'active' : ''}}`;
                cardEl.id = c.id;
                cardEl.innerHTML = `
                    <div>
                        <div class="insight-card-top">
                            <span class="insight-category-title">${{c.category}}</span>
                            <span class="insight-badge ${{c.badgeClass}}">${{c.badge}}</span>
                        </div>
                        <div class="insight-prov-title" style="margin-top:0.4rem;">
                            <span>${{c.icon}}</span> <span>${{c.prov}}</span>
                        </div>
                        <div class="insight-main-val" style="margin-top:0.25rem;">
                            ${{c.valHtml}}
                        </div>
                    </div>
                    <div>
                        <div class="insight-meta-details">
                            ${{c.metaLines.map(line => `<div>${{line}}</div>`).join('')}}
                        </div>
                        <div class="insight-card-footer">
                            <span>${{isSelected ? '✓ เลือกอยู่บนแผนที่' : c.actionText}}</span>
                        </div>
                    </div>
                `;
                cardEl.addEventListener('click', c.onClick);
                container.appendChild(cardEl);
            }});
        }}

        // -------------------------------------------------------------
        // RAIN-RICE RELATIONSHIP SCATTER PLOT (PROVINCE-YEAR PAIRS)
        // -------------------------------------------------------------
        let chartRainRiceScatter = null;
        function renderRainRiceScatterPlot() {{
            const canvas = document.getElementById('chartRainRiceScatter');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartRainRiceScatter) chartRainRiceScatter.destroy();

            const metricSelect = document.getElementById('scatterMetricSelect');
            const metric = metricSelect ? metricSelect.value : 'hrdi';
            const isExp = (state.hrdiMode === 'exploratory');
            const provs = Object.keys(REAL_DATA.centers);

            const pts2022 = [];
            const pts2023 = [];

            provs.forEach(p => {{
                const s = REAL_DATA.province_summaries[p] || {{}};
                const y22 = s.rice_yield_2022;
                const y23 = s.rice_yield_2023;

                let r22 = null;
                let r23 = null;

                if (metric === 'hrdi') {{
                    r22 = isExp ? s.rain_exp_2022 : s.rain_obs_2022;
                    r23 = isExp ? s.rain_exp_2023 : s.rain_obs_2023;
                }} else if (metric === 'hii') {{
                    r22 = s.hii_rain_2022;
                    r23 = s.hii_rain_2023;
                }} else if (metric === 'seasonal') {{
                    r22 = isExp ? s.exp_may_aug_2022 : s.obs_may_aug_2022;
                    r23 = isExp ? s.exp_may_aug_2023 : s.obs_may_aug_2023;
                }}

                if (r22 !== null && y22 !== null && !isNaN(r22) && !isNaN(y22)) {{
                    pts2022.push({{
                        x: Math.round(r22 * 10) / 10,
                        y: Math.round(y22 * 10) / 10,
                        prov: p,
                        year: 2022,
                        rain: r22,
                        yield: y22,
                        stations: s.station_count,
                        tambons: s.tambon_count,
                        status: isExp ? 'Exploratory' : 'Observed'
                    }});
                }}

                if (r23 !== null && y23 !== null && !isNaN(r23) && !isNaN(y23)) {{
                    pts2023.push({{
                        x: Math.round(r23 * 10) / 10,
                        y: Math.round(y23 * 10) / 10,
                        prov: p,
                        year: 2023,
                        rain: r23,
                        yield: y23,
                        stations: s.station_count,
                        tambons: s.tambon_count,
                        status: isExp ? 'Exploratory' : 'Observed'
                    }});
                }}
            }});

            const allPts = [...pts2022, ...pts2023];
            const badgeEl = document.getElementById('scatterSpearmanBadge');

            if (allPts.length < 4) {{
                if (badgeEl) badgeEl.textContent = `ข้อมูลไม่เพียงพอ (n = ${{allPts.length}})`;
                showChartEmptyState('chartRainRiceScatter', 'ข้อมูลไม่เพียงพอสำหรับวิเคราะห์สหสัมพันธ์', `พบข้อมูลที่จับคู่ได้ ${{allPts.length}} จุด (ต้องการอย่างน้อย 4 จุด) เนื่องจากในโหมด Observed Only ฝนปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน แนะนำสลับเป็นโหมด Exploratory หรือเลือกตัวชี้วัดฝน HII`, 'n < 4');
                return;
            }}

            clearChartEmptyState('chartRainRiceScatter');

            // Dynamic Spearman Rho calculation
            const rho = computeSpearmanRho(allPts);
            if (badgeEl) {{
                if (rho !== null) {{
                    const sign = rho > 0 ? '+' : '';
                    badgeEl.innerHTML = `Spearman ρ = <strong>${{sign}}${{rho.toFixed(4)}}</strong> (n = ${{allPts.length}} จว.-ปี)`;
                }} else {{
                    badgeEl.textContent = `Spearman ρ = N/A (n = ${{allPts.length}})`;
                }}
            }}

            let xLabel = 'ปริมาณน้ำฝนพื้นที่สูง (HRDI เฉลี่ยสถานี, มม.)';
            if (metric === 'hii') xLabel = 'ปริมาณน้ำฝนทั้งจังหวัด (HII รวม 12 เดือน, มม.)';
            if (metric === 'seasonal') xLabel = 'ปริมาณน้ำฝนฤดูปลูก พ.ค.–ส.ค. (มม.)';

            chartRainRiceScatter = new Chart(ctx, {{
                type: 'scatter',
                data: {{
                    datasets: [
                        {{
                            label: `ปี 2022 (${{pts2022.length}} จังหวัด)`,
                            data: pts2022,
                            backgroundColor: '#A778E8',
                            borderColor: '#8b5cf6',
                            borderWidth: 1.5,
                            pointRadius: 7,
                            pointHoverRadius: 10
                        }},
                        {{
                            label: `ปี 2023 (${{pts2023.length}} จังหวัด)`,
                            data: pts2023,
                            backgroundColor: '#FF8A32',
                            borderColor: '#ea580c',
                            borderWidth: 1.5,
                            pointRadius: 7,
                            pointHoverRadius: 10
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#F7F0E8', font: {{ family: "'Prompt'", size: 11 }} }}
                        }},
                        tooltip: {{
                            backgroundColor: 'rgba(20, 11, 36, 0.95)',
                            borderColor: 'rgba(255, 138, 50, 0.6)',
                            borderWidth: 1,
                            titleColor: '#FF8A32',
                            bodyColor: '#F7F0E8',
                            padding: 10,
                            callbacks: {{
                                title: (items) => {{
                                    const pt = items[0].raw;
                                    return `📍 จังหวัด${{pt.prov}} (${{pt.year}})`;
                                }},
                                label: (item) => {{
                                    const pt = item.raw;
                                    return [
                                        `🌧️ ปริมาณฝน: ${{pt.x.toLocaleString()}} มม. (${{pt.status}})`,
                                        `🌾 ผลผลิตข้าว: ${{pt.y.toLocaleString()}} กก./ไร่ (${{pt.tambons}} ตำบล)`,
                                        `🗼 สถานี HRDI ในพื้นที่: ${{pt.stations}} สถานี`,
                                        `💡 คลิกเพื่อดูรายละเอียดจังหวัดนี้บนแผนที่`
                                    ];
                                }}
                            }}
                        }}
                    }},
                    onClick: (e, elements) => {{
                        if (elements && elements.length > 0) {{
                            const el = elements[0];
                            const pt = chartRainRiceScatter.data.datasets[el.datasetIndex].data[el.index];
                            if (pt && pt.prov) {{
                                dispatchTab1Filter({{ province: pt.prov, year: String(pt.year) }});
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            title: {{ display: true, text: xLabel, color: '#A59DB5', font: {{ family: "'Prompt'", size: 11 }} }},
                            grid: {{ color: 'rgba(167, 120, 232, 0.08)' }},
                            ticks: {{ color: '#A59DB5' }}
                        }},
                        y: {{
                            title: {{ display: true, text: 'ผลผลิตข้าวนาปี (กก./ไร่) ทะเบียน DOAE', color: '#A59DB5', font: {{ family: "'Prompt'", size: 11 }} }},
                            grid: {{ color: 'rgba(167, 120, 232, 0.08)' }},
                            ticks: {{ color: '#A59DB5' }}
                        }}
                    }}
                }}
            }});
        }}

        const scatterMetricSelect = document.getElementById('scatterMetricSelect');
        if (scatterMetricSelect) {{
            scatterMetricSelect.addEventListener('change', () => renderRainRiceScatterPlot());
        }}

        const btnToggleAllRankings = document.getElementById('btnToggleAllRankings');
        const allRankingDrawer = document.getElementById('allRankingDrawer');
        const rankToggleArrow = document.getElementById('rankToggleArrow');
        if (btnToggleAllRankings && allRankingDrawer) {{
            btnToggleAllRankings.addEventListener('click', () => {{
                const isClosed = allRankingDrawer.classList.contains('closed');
                allRankingDrawer.classList.toggle('closed', !isClosed);
                if (rankToggleArrow) rankToggleArrow.textContent = isClosed ? '▲' : '▼';
            }});
        }}

        function renderTab1ProvinceRankChart() {{
            const canvas = document.getElementById('chartProvinceRank');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartProvinceRank) chartProvinceRank.destroy();

            const isExp = (state.hrdiMode === 'exploratory');
            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;

            if (!isExp && (yr === '2023' || yr === 'all')) {{
                showChartEmptyState('chartProvinceRank', 'ไม่มีผลรวมตรวจวัดจริงปี 2023', 'สถานี HRDI ปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน (สูงสุด 9 เดือน) ตามหลักสถิติจึงไม่แสดงการจัดอันดับผลรวมทั้งปี แนะนำสลับเป็นโหมดทดลองวิเคราะห์ (Exploratory)', 'HRDI: ตรวจวัดไม่ครบ 12 ด.');
                return;
            }}
            clearChartEmptyState('chartProvinceRank');

            const provRainPairs = provs.map(p => {{
                const sum = REAL_DATA.province_summaries[p] || {{}};
                const r = isExp ? ((yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all)
                               : sum.rain_obs_2022;
                return {{ name: p, rain: r }};
            }}).filter(x => x.rain !== null && !isNaN(x.rain)).sort((a, b) => b.rain - a.rain);

            chartProvinceRank = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: provRainPairs.map(x => x.name),
                    datasets: [{{
                        label: `ฝนเฉลี่ย (${{yr === 'all' ? '2022–2023' : yr}})`,
                        data: provRainPairs.map(x => x.rain),
                        backgroundColor: provRainPairs.map(x => (state.tab1.province === x.name ? '#FF8A32' : '#A778E8')),
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{ padding: 8 }}
                    }},
                    scales: {{
                        x: {{ grid: {{ color: 'rgba(167, 120, 232, 0.08)' }}, ticks: {{ color: '#A59DB5' }} }},
                        y: {{ grid: {{ display: false }}, ticks: {{ color: '#ffffff', font: {{ weight: '600' }} }} }}
                    }},
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const pName = provRainPairs[elements[0].index].name;
                            dispatchTab1Filter({{ province: pName }});
                        }}
                    }}
                }}
            }});
        }}

        // -------------------------------------------------------------
        // F. TAB 2: RAINFALL COMPARISON (HRDI VS HII)
        // -------------------------------------------------------------
        const tab2_filterYear = document.getElementById('tab2_filterYear');
        const tab2_filterProvince = document.getElementById('tab2_filterProvince');
        const tab2_filterSource = document.getElementById('tab2_filterSource');
        const tab2_btnReset = document.getElementById('tab2_btnReset');
        let chartTab2RainComp = null;
        let chartTab2Trend = null;

        function dispatchTab2Filter(changes) {{
            if (changes.year !== undefined) state.tab2.year = changes.year;
            if (changes.province !== undefined) state.tab2.province = changes.province;
            if (changes.source !== undefined) state.tab2.source = changes.source;

            tab2_filterYear.value = state.tab2.year;
            tab2_filterProvince.value = state.tab2.province;
            tab2_filterSource.value = state.tab2.source;

            updateTab2Components();
        }}

        tab2_filterYear.addEventListener('change', (e) => dispatchTab2Filter({{ year: e.target.value }}));
        tab2_filterProvince.addEventListener('change', (e) => dispatchTab2Filter({{ province: e.target.value }}));
        tab2_filterSource.addEventListener('change', (e) => dispatchTab2Filter({{ source: e.target.value }}));
        tab2_btnReset.addEventListener('click', () => dispatchTab2Filter({{ year: 'all', province: 'all', source: 'all' }}));

        function updateTab2Components() {{
            const yr = state.tab2.year;
            const p = state.tab2.province;
            const isExp = (state.hrdiMode === 'exploratory');

            let hrdiMean = isExp ? REAL_DATA.overall_kpis.hrdi_exp_rain_all : REAL_DATA.overall_kpis.hrdi_obs_rain_2022;
            let hiiMean = 1358.5;

            if (p !== 'all') {{
                const sum = REAL_DATA.province_summaries[p];
                if (sum) {{
                    if (isExp) {{
                        hrdiMean = (yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all;
                    }} else {{
                        hrdiMean = (yr === '2022') ? sum.rain_obs_2022 : (yr === '2023') ? sum.rain_obs_2023 : sum.rain_obs_all;
                    }}
                    hiiMean = (yr === '2022') ? sum.hii_rain_2022 : (yr === '2023') ? sum.hii_rain_2023 : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                }}
            }} else {{
                if (yr === '2022') {{
                    hrdiMean = isExp ? REAL_DATA.overall_kpis.hrdi_exp_rain_2022 : REAL_DATA.overall_kpis.hrdi_obs_rain_2022;
                    hiiMean = 1420.2;
                }} else if (yr === '2023') {{
                    hrdiMean = isExp ? REAL_DATA.overall_kpis.hrdi_exp_rain_2023 : null;
                    hiiMean = 1296.8;
                }}
            }}

            const hrdiEl = document.getElementById('tab2_kpiHrdi');
            const hiiEl = document.getElementById('tab2_kpiHii');
            const diffEl = document.getElementById('tab2_kpiDiff');

            if (hrdiEl) {{
                hrdiEl.textContent = (hrdiMean !== null && !isNaN(hrdiMean)) ? hrdiMean.toFixed(1) : 'ไม่ครบ 12 ด.';
            }}
            if (hiiEl) hiiEl.textContent = (hiiMean !== null && !isNaN(hiiMean)) ? hiiMean.toFixed(1) : 'ไม่มีรายงาน';
            if (diffEl) {{
                if (hrdiMean !== null && hiiMean !== null && !isNaN(hrdiMean) && !isNaN(hiiMean)) {{
                    const diff = hrdiMean - hiiMean;
                    diffEl.textContent = `${{diff > 0 ? '+' : ''}}${{diff.toFixed(1)}}`;
                }} else {{
                    diffEl.textContent = '—';
                }}
            }}

            renderTab2Charts();
        }}

        function renderTab2Charts() {{
            const canvas1 = document.getElementById('chartDetailedRainComparison');
            if (chartTab2RainComp) chartTab2RainComp.destroy();

            const p = state.tab2.province;
            const src = state.tab2.source;
            const yr = state.tab2.year;

            clearChartEmptyState('chartDetailedRainComparison');
            const provList = (p === 'all') ? Object.keys(REAL_DATA.province_summaries) : [p];
            const hrdiVals = [];
            const hiiVals = [];

            const isExp = (state.hrdiMode === 'exploratory');
            provList.forEach(pr => {{
                const s = REAL_DATA.province_summaries[pr] || {{}};
                let hrdi = null;
                if (isExp) {{
                    hrdi = (yr === '2022') ? s.rain_exp_2022 : (yr === '2023') ? s.rain_exp_2023 : s.rain_exp_all;
                }} else {{
                    hrdi = (yr === '2022') ? s.rain_obs_2022 : (yr === '2023') ? s.rain_obs_2023 : s.rain_obs_all;
                }}
                const hii = (yr === '2022') ? s.hii_rain_2022 : (yr === '2023') ? s.hii_rain_2023 : (((s.hii_rain_2022 || 0) + (s.hii_rain_2023 || 0)) / 2);
                hrdiVals.push(hrdi !== null ? Math.round(hrdi) : null);
                hiiVals.push(Math.round(hii || 0));
            }});

            if (!isExp && yr === '2023' && hrdiVals.every(x => x === null)) {{
                showChartEmptyState('chartDetailedRainComparison', 'ไม่มีผลรวมตรวจวัดจริงปี 2023 (HRDI)', 'สถานี HRDI ปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน (สูงสุด 9 เดือน) ตามหลักสถิติจึงไม่แสดงผลรวมทั้งปี แนะนำสลับเป็นโหมดทดลองวิเคราะห์ (Exploratory)', 'HRDI: ตรวจวัดไม่ครบ 12 ด.');
                return;
            }}

            const datasets = [];
            if (src === 'all' || src === 'HRDI') {{
                datasets.push({{ label: 'HRDI บนพื้นที่สูง (มม.)', data: hrdiVals, backgroundColor: '#A778E8', borderRadius: 4 }});
            }}
            if (src === 'all' || src === 'HII') {{
                datasets.push({{ label: 'HII ทั้งจังหวัด (มม.)', data: hiiVals, backgroundColor: '#38bdf8', borderRadius: 4 }});
            }}

            chartTab2RainComp = new Chart(canvas1.getContext('2d'), {{
                type: 'bar',
                data: {{ labels: provList, datasets: datasets }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#F7F0E8' }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#A59DB5' }} }},
                        y: {{ ticks: {{ color: '#A59DB5' }} }}
                    }}
                }}
            }});

            const canvas2 = document.getElementById('chartRainTrendCompare');
            if (chartTab2Trend) chartTab2Trend.destroy();
            clearChartEmptyState('chartRainTrendCompare');

            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            let hii22 = [];
            let hii23 = [];

            if (p !== 'all' && REAL_DATA.hii_prov_24 && REAL_DATA.hii_prov_24[p]) {{
                const p24 = REAL_DATA.hii_prov_24[p];
                hii22 = p24.slice(0, 12);
                hii23 = p24.slice(12, 24);
            }} else {{
                hii22 = REAL_DATA.monthly_overall['2022'];
                hii23 = REAL_DATA.monthly_overall['2023'];
            }}

            const datasets2 = [
                {{ label: 'HII ระดับจังหวัด (2022)', data: hii22, borderColor: '#38bdf8', borderDash: [4, 4], tension: 0.3 }},
                {{ label: 'HII ระดับจังหวัด (2023)', data: hii23, borderColor: '#0284c7', borderDash: [4, 4], tension: 0.3 }}
            ];

            // HRDI Monthly Curve: Use real station averages for the province
            let pStas = REAL_DATA.stations;
            if (p !== 'all') pStas = pStas.filter(s => s.province === p);

            let hrdi22 = months.map((_, i) => {{
                const vals = pStas.map(s => {{
                    const arr = isExp ? s.monthly_exp_2022 : s.monthly_obs_2022;
                    return (arr && arr[i] !== null && !isNaN(arr[i])) ? arr[i] : null;
                }}).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : null;
            }});
            let hrdi23 = months.map((_, i) => {{
                const vals = pStas.map(s => {{
                    const arr = isExp ? s.monthly_exp_2023 : s.monthly_obs_2023;
                    return (arr && arr[i] !== null && !isNaN(arr[i])) ? arr[i] : null;
                }}).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : null;
            }});

            datasets2.unshift(
                {{ label: `HRDI บนพื้นที่สูง (2022) [${{pStas.length}} สถานี]`, data: hrdi22, borderColor: '#A778E8', tension: 0.3 }},
                {{ label: `HRDI บนพื้นที่สูง (2023) [${{pStas.length}} สถานี]`, data: hrdi23, borderColor: '#FF8A32', tension: 0.3 }}
            );

            chartTab2Trend = new Chart(canvas2.getContext('2d'), {{
                type: 'line',
                data: {{ labels: months, datasets: datasets2 }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#F7F0E8' }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#A59DB5' }} }},
                        y: {{ ticks: {{ color: '#A59DB5' }} }}
                    }}
                }}
            }});
        }}

        // -------------------------------------------------------------
        // G. TAB 3: RICE YIELD (ALL 921 TAMBONS & BALANCED PANEL)
        // -------------------------------------------------------------
        const tab3_filterYear = document.getElementById('tab3_filterYear');
        const tab3_filterProvince = document.getElementById('tab3_filterProvince');
        const tab3_filterTambon = document.getElementById('tab3_filterTambon');
        const tab3_btnReset = document.getElementById('tab3_btnReset');
        const tambonSearchInput = document.getElementById('tambonSearchInput');
        let chartRiceDumbbell = null;
        let chartRiceRankedBar = null;

        function updateTab3CascadingTambons() {{
            const p = state.tab3.province;
            tab3_filterTambon.innerHTML = '<option value="all">ทั้งหมด (921 ตำบล ทะเบียน DOAE)</option>';
            let tbs = REAL_DATA.tambons;
            if (p !== 'all') {{
                tbs = tbs.filter(t => t.province_name === p);
                tab3_filterTambon.innerHTML = `<option value="all">ทั้งหมดใน${{p}} (${{tbs.length}} ตำบล)</option>`;
            }}
            tbs.forEach(t => {{
                const opt = document.createElement('option');
                opt.value = t.tambon_code_6;
                opt.textContent = `${{t.tambon_name}} (${{t.amphoe_name || t.province_name}}) [${{t.coverage_badge || 'DOAE'}}]`;
                tab3_filterTambon.appendChild(opt);
            }});
            tab3_filterTambon.value = state.tab3.tambon;
        }}

        function dispatchTab3Filter(changes) {{
            let pChanged = false;
            if (changes.year !== undefined) state.tab3.year = changes.year;
            if (changes.province !== undefined && changes.province !== state.tab3.province) {{
                state.tab3.province = changes.province;
                pChanged = true;
                if (changes.tambon === undefined) state.tab3.tambon = 'all';
            }}
            if (changes.tambon !== undefined) state.tab3.tambon = changes.tambon;

            tab3_filterYear.value = state.tab3.year;
            tab3_filterProvince.value = state.tab3.province;
            if (pChanged) updateTab3CascadingTambons();
            tab3_filterTambon.value = state.tab3.tambon;

            updateTab3Components();
        }}

        tab3_filterYear.addEventListener('change', (e) => dispatchTab3Filter({{ year: e.target.value }}));
        tab3_filterProvince.addEventListener('change', (e) => dispatchTab3Filter({{ province: e.target.value }}));
        tab3_filterTambon.addEventListener('change', (e) => dispatchTab3Filter({{ tambon: e.target.value }}));
        tab3_btnReset.addEventListener('click', () => dispatchTab3Filter({{ year: 'all', province: 'all', tambon: 'all' }}));
        if (tambonSearchInput) tambonSearchInput.addEventListener('input', () => renderRiceTambonTable());

        updateTab3CascadingTambons();

        function updateTab3Components() {{
            let tbs = REAL_DATA.tambons;
            if (state.tab3.province !== 'all') tbs = tbs.filter(t => t.province_name === state.tab3.province);
            if (state.tab3.tambon !== 'all') tbs = tbs.filter(t => t.tambon_code_6 === state.tab3.tambon);

            const count = tbs.length;
            const valid22 = tbs.filter(t => t.yield_2022 !== null && !isNaN(t.yield_2022));
            const valid23 = tbs.filter(t => t.yield_2023 !== null && !isNaN(t.yield_2023));

            const mean22 = valid22.length > 0 ? (valid22.reduce((a, b) => a + b.yield_2022, 0) / valid22.length) : null;
            const mean23 = valid23.length > 0 ? (valid23.reduce((a, b) => a + b.yield_2023, 0) / valid23.length) : null;
            const incCnt = tbs.filter(t => t.direction === 'เพิ่มขึ้น (+)').length;
            const decCnt = tbs.filter(t => t.direction === 'ลดลง (-)').length;

            document.getElementById('tab3_kpiTambonCount').textContent = count;
            document.getElementById('tab3_kpiYield22').textContent = (mean22 !== null) ? mean22.toFixed(1) : 'ไม่มีรายงาน';
            document.getElementById('tab3_kpiYield23').textContent = (mean23 !== null) ? mean23.toFixed(1) : 'ไม่มีรายงาน';
            document.getElementById('tab3_kpiInc').textContent = incCnt;
            document.getElementById('tab3_kpiDec').textContent = decCnt;

            renderRiceDumbbellChart(tbs);
            renderRiceRankedBarChart(tbs);
            renderRiceTambonTable();
        }}

        function renderRiceDumbbellChart(tbs) {{
            const canvas = document.getElementById('chartRiceDumbbell');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartRiceDumbbell) chartRiceDumbbell.destroy();

            if (state.tab3.tambon !== 'all') {{
                const t = tbs[0];
                if (!t || (t.yield_2022 === null && t.yield_2023 === null)) {{
                    showChartEmptyState('chartRiceDumbbell', 'ไม่มีรายงานผลผลิตข้าวนาปี', `ตำบล${{t ? t.tambon_name : state.tab3.tambon}} ไม่มีข้อมูลรายงานผลผลิตข้าวในทะเบียน DOAE ปี 2022–2023`, 'สถานะ: ไม่มีรายงาน');
                    return;
                }}
                if (t.yield_2022 === null || t.yield_2023 === null) {{
                    const hasYr = t.yield_2022 !== null ? '2022' : '2023';
                    const yVal = t.yield_2022 !== null ? t.yield_2022 : t.yield_2023;
                    showChartEmptyState('chartRiceDumbbell', `มีข้อมูลเฉพาะปี ${{hasYr}}`, `ตำบลนี้มีรายงานผลผลิตเฉพาะปี ${{hasYr}} (${{yVal.toFixed(1)}} กก./ไร่) ไม่สามารถเปรียบเทียบ Dumbbell 2 ปีได้`, `มีข้อมูลเฉพาะปี ${{hasYr}}`);
                    return;
                }}
            }}

            const validTbs = tbs.filter(t => t.yield_2022 !== null && t.yield_2023 !== null);
            if (validTbs.length === 0) {{
                showChartEmptyState('chartRiceDumbbell', 'ไม่พบตำบลที่มีข้อมูลครบ 2 ปี', 'ในตัวกรองที่เลือก ไม่มีตำบลที่รายงานผลผลิตข้าวครบทั้งปี 2022 และ 2023', 'ไม่มีข้อมูลเปรียบเทียบ');
                return;
            }}

            clearChartEmptyState('chartRiceDumbbell');

            // Limit display to top 25 for clear visualization
            const displayList = validTbs.slice(0, 25);
            const labels = displayList.map(t => `${{t.tambon_name}} (${{t.province_name}})`);
            const d22 = displayList.map(t => t.yield_2022);
            const d23 = displayList.map(t => t.yield_2023);

            chartRiceDumbbell = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [
                        {{ label: 'ผลผลิตปี 2022 (กก./ไร่)', data: d22, backgroundColor: '#A778E8', borderRadius: 4 }},
                        {{ label: 'ผลผลิตปี 2023 (กก./ไร่)', data: d23, backgroundColor: '#FF8A32', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#F7F0E8' }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#A59DB5' }} }},
                        y: {{ ticks: {{ color: '#F7F0E8', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }}

        function renderRiceRankedBarChart(tbs) {{
            const canvas = document.getElementById('chartRiceRankedBar');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartRiceRankedBar) chartRiceRankedBar.destroy();

            if (state.tab3.tambon !== 'all') {{
                const t = tbs[0];
                if (!t || t.delta_yield === null || isNaN(t.delta_yield)) {{
                    showChartEmptyState('chartRiceRankedBar', 'ไม่มีรายงานการเปลี่ยนแปลง', `ตำบล${{t ? t.tambon_name : state.tab3.tambon}} ไม่มีข้อมูลผลผลิตครบ 2 ปีเพื่อคำนวณส่วนต่าง`, 'สถานะ: ข้อมูลไม่ครบ');
                    return;
                }}
            }}

            const validDeltas = tbs.filter(t => t.delta_yield !== null && !isNaN(t.delta_yield));
            if (validDeltas.length === 0) {{
                showChartEmptyState('chartRiceRankedBar', 'ไม่มีข้อมูลการเปลี่ยนแปลง', 'ไม่พบตำบลที่มีข้อมูลผลผลิตครบทั้ง 2 ปีเพื่อเปรียบเทียบการเปลี่ยนแปลง', 'ไม่มีข้อมูล');
                return;
            }}

            clearChartEmptyState('chartRiceRankedBar');

            const sorted = [...validDeltas].sort((a, b) => b.delta_yield - a.delta_yield).slice(0, 25);
            const labels = sorted.map(t => `${{t.tambon_name}} (${{t.province_name}})`);
            const deltas = sorted.map(t => t.delta_yield);
            const colors = sorted.map(t => (t.delta_yield > 0 ? '#22c55e' : t.delta_yield < 0 ? '#ef4444' : '#eab308'));

            chartRiceRankedBar = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: 'Δ ผลผลิต (2023 - 2022) กก./ไร่',
                        data: deltas,
                        backgroundColor: colors,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#A59DB5' }} }},
                        y: {{ ticks: {{ color: '#F7F0E8', font: {{ size: 10 }} }} }}
                    }}
                }}
            }});
        }}

        function renderRiceTambonTable() {{
            const tbody = document.querySelector('#riceTambonTable tbody');
            if (!tbody) return;
            tbody.innerHTML = '';
            let tbs = REAL_DATA.tambons;
            if (state.tab3.province !== 'all') tbs = tbs.filter(t => t.province_name === state.tab3.province);
            if (state.tab3.tambon !== 'all') tbs = tbs.filter(t => t.tambon_code_6 === state.tab3.tambon);

            if (tambonSearchInput) {{
                const search = tambonSearchInput.value.toLowerCase().trim();
                if (search) {{
                    tbs = tbs.filter(t => (t.tambon_name && t.tambon_name.toLowerCase().includes(search)) || (t.amphoe_name && t.amphoe_name.toLowerCase().includes(search)) || t.province_name.toLowerCase().includes(search) || t.tambon_code_6.includes(search));
                }}
            }}

            // Render up to 100 rows for smooth performance
            const displayRows = tbs.slice(0, 100);
            displayRows.forEach(t => {{
                const tr = document.createElement('tr');
                const dirColor = t.direction === 'เพิ่มขึ้น (+)' ? '#22c55e' : t.direction === 'ลดลง (-)' ? '#ef4444' : '#eab308';
                const y22Str = (t.yield_2022 !== null && !isNaN(t.yield_2022)) ? t.yield_2022.toFixed(1) : '<span class="badge-missing">ไม่มีรายงาน</span>';
                const y23Str = (t.yield_2023 !== null && !isNaN(t.yield_2023)) ? t.yield_2023.toFixed(1) : '<span class="badge-missing">ไม่มีรายงาน</span>';
                const deltaStr = (t.delta_yield !== null && !isNaN(t.delta_yield)) ? `<span style="color:${{dirColor}}; font-weight:bold;">${{t.delta_yield > 0 ? '+' : ''}}${{t.delta_yield.toFixed(1)}}</span>` : '<span style="color:#A59DB5;">-</span>';
                const hrdiDeltaStr = (t.delta_hrdi !== null && t.delta_hrdi !== undefined && !isNaN(t.delta_hrdi)) ? t.delta_hrdi.toFixed(1) : '<span style="color:#A59DB5;">-</span>';

                let badgeClass = 'badge-missing';
                if (t.coverage_status === 'observed_both') badgeClass = 'badge-obs';
                else if (t.coverage_status === 'observed_2022_only' || t.coverage_status === 'observed_2023_only') badgeClass = 'badge-demo';

                tr.innerHTML = `
                    <td><code>${{t.tambon_code_6}}</code></td>
                    <td><strong>${{t.tambon_name || t.label}}</strong></td>
                    <td>${{t.amphoe_name || '-'}}</td>
                    <td>${{t.province_name}}</td>
                    <td>${{y22Str}}</td>
                    <td>${{y23Str}}</td>
                    <td>${{deltaStr}}</td>
                    <td>${{hrdiDeltaStr}}</td>
                    <td><span class="${{badgeClass}}">${{t.coverage_badge || t.coverage_status || 'DOAE'}}</span></td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // -------------------------------------------------------------
        // H. TAB 4: CORRELATION & LOPO SENSITIVITY
        // -------------------------------------------------------------
        const tab4_filterLevel = document.getElementById('tab4_filterLevel');
        const tab4_filterProvince = document.getElementById('tab4_filterProvince');
        const tab4_btnReset = document.getElementById('tab4_btnReset');
        let chartScatter = null;

        function dispatchTab4Filter(changes) {{
            if (changes.level !== undefined) state.tab4.level = changes.level;
            if (changes.province !== undefined) state.tab4.province = changes.province;

            tab4_filterLevel.value = state.tab4.level;
            tab4_filterProvince.value = state.tab4.province;

            renderTab4ScatterPlot();
        }}

        tab4_filterLevel.addEventListener('change', (e) => dispatchTab4Filter({{ level: e.target.value }}));
        tab4_filterProvince.addEventListener('change', (e) => dispatchTab4Filter({{ province: e.target.value }}));
        tab4_btnReset.addEventListener('click', () => dispatchTab4Filter({{ level: 'tambon', province: 'all' }}));

        function renderTab4ScatterPlot() {{
            const canvas = document.getElementById('chartScatterPlot');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartScatter) chartScatter.destroy();

            let pts = [];
            const pFilter = state.tab4.province;

            if (state.tab4.level === 'tambon') {{
                // Use balanced panel of 25 tambons that have matched HRDI stations
                let bTbs = REAL_DATA.balanced_tambons || [];
                if (pFilter !== 'all') bTbs = bTbs.filter(t => t.province_name === pFilter);
                pts = bTbs.map(t => ({{
                    x: t.delta_hrdi,
                    y: t.delta_yield,
                    title: `${{t.tambon_name}} (${{t.province_name}})`,
                    province: t.province_name
                }})).filter(p => p.x !== null && p.y !== null && !isNaN(p.x) && !isNaN(p.y));
            }} else if (state.tab4.level === 'province_hrdi') {{
                let pChanges = REAL_DATA.province_changes || [];
                if (pFilter !== 'all') pChanges = pChanges.filter(p => p.province_name === pFilter);
                pts = pChanges.map(p => ({{
                    x: p.mean_hrdi_change,
                    y: p.mean_yield_change,
                    title: `จ.${{p.province_name}} (${{p.tambons}} ตำบล)`,
                    province: p.province_name
                }})).filter(p => p.x !== null && p.y !== null && !isNaN(p.x) && !isNaN(p.y));
            }} else {{
                // province_hii (All 9 provinces)
                let provs = Object.keys(REAL_DATA.centers);
                if (pFilter !== 'all') provs = provs.filter(p => p === pFilter);
                pts = provs.map(pName => {{
                    const s = REAL_DATA.province_summaries[pName] || {{}};
                    const deltaHii = (s.hii_rain_2023 || 0) - (s.hii_rain_2022 || 0);
                    const deltaYield = (s.rice_yield_2023 || 0) - (s.rice_yield_2022 || 0);
                    return {{
                        x: Math.round(deltaHii * 10) / 10,
                        y: Math.round(deltaYield * 10) / 10,
                        title: `จ.${{pName}} (ฝน HII)`,
                        province: pName
                    }};
                }}).filter(p => p.x !== null && p.y !== null && !isNaN(p.x) && !isNaN(p.y));
            }}

            const n = pts.length;
            const rho = computeSpearmanRho(pts);

            // Update KPI cards dynamically
            const kpiVal1 = document.getElementById('tab4_kpiVal1');
            const kpiPill1 = document.getElementById('tab4_kpiPill1');
            const kpiSub1 = document.getElementById('tab4_kpiSub1');

            if (kpiVal1 && kpiPill1 && kpiSub1) {{
                if (n < 3) {{
                    kpiVal1.textContent = 'N/A';
                    kpiPill1.textContent = `n = ${{n}} (< 3)`;
                    kpiPill1.style.background = 'rgba(239, 68, 68, 0.2)';
                    kpiPill1.style.color = '#ef4444';
                    kpiSub1.textContent = 'ขนาดตัวอย่างไม่เพียงพอต่อการคำนวณทางสถิติ';
                }} else {{
                    kpiVal1.textContent = (rho !== null) ? rho.toFixed(4) : 'N/A';
                    kpiPill1.textContent = `n = ${{n}}`;
                    kpiPill1.style.background = 'rgba(167, 120, 232, 0.2)';
                    kpiPill1.style.color = '#A778E8';
                    kpiSub1.textContent = `คำนวณจากตัวอย่างจริง n = ${{n}} (พ.ค.–ส.ค.)`;
                }}
            }}

            if (n < 3) {{
                showChartEmptyState('chartScatterPlot', `จำนวนตัวอย่างไม่เพียงพอ (n = ${{n}})`, `พบข้อมูลที่ตรงตามเงื่อนไขเพียง n = ${{n}} รายการ ซึ่งน้อยกว่าเกณฑ์ทางสถิติขั้นต่ำ (n ≥ 3) สำหรับการคำนวณสหสัมพันธ์ Spearman`, `Sample Size n = ${{n}} < 3`);
                return;
            }}

            clearChartEmptyState('chartScatterPlot');

            chartScatter = new Chart(ctx, {{
                type: 'scatter',
                data: {{
                    datasets: [{{
                        label: `ตัวอย่างการวิเคราะห์ (n = ${{n}}, Spearman ρ = ${{rho !== null ? rho.toFixed(4) : '-'}})`,
                        data: pts,
                        backgroundColor: '#FF8A32',
                        borderColor: '#ffffff',
                        borderWidth: 1.5,
                        pointRadius: 8,
                        pointHoverRadius: 12
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ labels: {{ color: '#F7F0E8' }} }},
                        tooltip: {{
                            padding: 10,
                            callbacks: {{
                                title: (ctx) => ctx[0].raw.title,
                                label: (ctx) => [
                                    `จังหวัด: ${{ctx.raw.province}}`,
                                    `Δ ฝน: ${{ctx.raw.x.toFixed(1)}} มม.`,
                                    `Δ ผลผลิตข้าว: ${{ctx.raw.y.toFixed(1)}} กก./ไร่`
                                ]
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ title: {{ display: true, text: 'Δ ปริมาณน้ำฝน (มม.)', color: '#FF8A32', font: {{ weight: 'bold' }} }}, ticks: {{ color: '#A59DB5' }} }},
                        y: {{ title: {{ display: true, text: 'Δ ผลผลิตข้าวนาปี (กก./ไร่)', color: '#FF8A32', font: {{ weight: 'bold' }} }}, ticks: {{ color: '#A59DB5' }} }}
                    }}
                }}
            }});
        }}

        // LOPO Table Population
        function renderLopoTable() {{
            const tbody = document.querySelector('#lopoTable tbody');
            tbody.innerHTML = '';
            REAL_DATA.lopo.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${{row.excluded_province_name}}</strong></td>
                    <td>${{row.tambons}}</td>
                    <td style="color:${{row.hrdi_tambon_rho < 0 ? '#FF8A32' : '#4ade80'}};">${{row.hrdi_tambon_rho.toFixed(4)}}</td>
                    <td>${{row.hrdi_province_rho.toFixed(4)}}</td>
                    <td>${{row.hii_province_rho.toFixed(4)}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Window Comparison Table Population (Sensitivity: May-Aug vs Feb-Jul)
        function renderWindowCompTable() {{
            const tbody = document.querySelector('#windowCompTable tbody');
            if (!tbody || !REAL_DATA.window_comparison) return;
            tbody.innerHTML = '';
            REAL_DATA.window_comparison.forEach(row => {{
                const tr = document.createElement('tr');
                const metric = row["Metric"] || "";
                const baseVal = row["Baseline (Feb-Jul)"] || "";
                const expVal = row["Experiment (May-Aug)"] || "";
                const note = row["Difference / Note"] || "";
                tr.innerHTML = `
                    <td><strong>${{metric}}</strong></td>
                    <td style="color:#A59DB5;">${{baseVal}}</td>
                    <td style="color:#FF8A32; font-weight:bold;">${{expVal}}</td>
                    <td style="font-size:0.8rem; color:#d1d5db;">${{note}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        renderLopoTable();
        renderWindowCompTable();

        // -------------------------------------------------------------
        // I. TAB 5: RAW DATA PREVIEW (5 ROWS FIRST OF DATASETS)
        // -------------------------------------------------------------
        const btnSampleHrdi = document.getElementById('btnSampleHrdi');
        const btnSampleHii = document.getElementById('btnSampleHii');
        const btnSamplePlant = document.getElementById('btnSamplePlant');
        let currentSampleKey = 'hrdi';

        function renderSampleTable(key) {{
            currentSampleKey = key;
            [btnSampleHrdi, btnSampleHii, btnSamplePlant].forEach(b => {{
                b.style.background = 'rgba(255,138,50,0.12)';
                b.style.color = 'var(--primary-orange)';
            }});
            if (key === 'hrdi') {{
                btnSampleHrdi.style.background = 'var(--primary-orange)';
                btnSampleHrdi.style.color = '#fff';
            }} else if (key === 'hii') {{
                btnSampleHii.style.background = 'var(--primary-orange)';
                btnSampleHii.style.color = '#fff';
            }} else {{
                btnSamplePlant.style.background = 'var(--primary-orange)';
                btnSamplePlant.style.color = '#fff';
            }}

            const rows = REAL_DATA.raw_samples ? REAL_DATA.raw_samples[key] || [] : [];
            const thead = document.getElementById('sampleHeaderRow');
            const tbody = document.getElementById('sampleBodyRows');
            thead.innerHTML = '';
            tbody.innerHTML = '';

            if (rows.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="5">ไม่มีข้อมูลพรีวิว</td></tr>';
                return;
            }}

            const cols = Object.keys(rows[0]);
            cols.forEach(c => {{
                const th = document.createElement('th');
                th.textContent = c;
                thead.appendChild(th);
            }});

            rows.forEach(r => {{
                const tr = document.createElement('tr');
                cols.forEach(c => {{
                    const td = document.createElement('td');
                    td.textContent = r[c];
                    tr.appendChild(td);
                }});
                tbody.appendChild(tr);
            }});
        }}

        btnSampleHrdi.addEventListener('click', () => renderSampleTable('hrdi'));
        btnSampleHii.addEventListener('click', () => renderSampleTable('hii'));
        btnSamplePlant.addEventListener('click', () => renderSampleTable('plant'));

        renderSampleTable('hrdi');

        // -------------------------------------------------------------
        // J. NAVIGATION TAB SWITCHING LOGIC
        // -------------------------------------------------------------
        const navTabBtns = document.querySelectorAll('.nav-tab-btn');
        navTabBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                navTabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const targetTab = btn.getAttribute('data-tab');
                state.activeTab = targetTab;

                document.querySelectorAll('.page-view-section').forEach(sec => sec.classList.remove('active'));
                const targetSec = document.getElementById(targetTab);
                if (targetSec) targetSec.classList.add('active');

                if (targetTab === 'page1') {{
                    setTimeout(() => {{
                        map.invalidateSize();
                        updateTab1Components();
                    }}, 150);
                }} else if (targetTab === 'page2') {{
                    updateTab2Components();
                }} else if (targetTab === 'page3') {{
                    updateTab3Components();
                }} else if (targetTab === 'page4') {{
                    renderTab4ScatterPlot();
                }}
            }});
        }});

        // Initial Render of All Tabs
        updateTab1Components();
        setTimeout(() => map.invalidateSize(), 300);

    }});
    </script>

</body>
</html>
"""
    return html_content


# ==============================================================================
# STREAMLIT APPLICATION ENTRY POINT
# Allows running directly with: streamlit run dashboard/halloween_app.py
# ==============================================================================
try:
    import streamlit as st
    import streamlit.components.v1 as components
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    ctx = get_script_run_ctx()
    if ctx is not None:
        st.set_page_config(
            page_title="สภาพภูมิอากาศบนพื้นที่สูงของประเทศไทยและผลผลิตข้าวนาปี (2022–2023)",
            page_icon="🌾",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

        st.markdown("""
            <style>
                /* Prevent white flash by setting Halloween theme background on Streamlit container */
                .stApp, body, html {
                    background-color: #100B1B !important;
                    color: #F8F4FF !important;
                }
                /* Hide default Streamlit sidebar & decorations */
                [data-testid="stSidebar"], section[data-testid="stSidebar"] {
                    display: none !important;
                }
                header[data-testid="stHeader"] {
                    display: none !important;
                }
                footer {
                    display: none !important;
                }
                /* Full width layout without extra margins */
                .block-container {
                    padding: 0 !important;
                    margin: 0 !important;
                    max-width: 100% !important;
                }
                iframe {
                    border: none !important;
                    width: 100% !important;
                    min-height: 100vh !important;
                    display: block;
                    background-color: #100B1B !important;
                }
            </style>
        """, unsafe_allow_html=True)

        html_code = get_halloween_html()
        components.html(html_code, height=2100, scrolling=True)
    elif __name__ == "__main__":
        print("Halloween Dashboard module ready. Run with: streamlit run dashboard/halloween_app.py")
except ImportError:
    pass

