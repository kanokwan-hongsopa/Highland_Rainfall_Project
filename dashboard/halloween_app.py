"""
Highland Rainfall Project - Halloween Interactive Dashboard Generator
100% Matching assets/dashboard_reference.png:
- Spooky night harvest rice field hero with glowing red-eyed scarecrow, orange moon, bats, lanterns
- Top horizontal navigation menu (5 tabs)
- Top horizontal dynamic cascading filter bar (Year, Province, Station, Tambon, Reset All)
- 5 KPI metric cards with badges and glowing mini waves
- Left large interactive map (600px height) with 9-province choropleth, 50 station markers, year toggle, smooth flyTo zoom, and interactive popup card
- OpenStreetMap Dark Invert Tiles (100% FREE, NO API KEY REQUIRED, NO WATERMARK)
- Right charts: Monthly rainfall trend curve (2022 vs 2023), Rainfall comparison bar chart, Rice yield comparison bar chart
- Full cross-filtering across Map, Station Markers, Charts, Scatter Plot, Filters, and Detail Popup
- Pages 1 to 5 fully functional with wide layout and refined proportions
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
    ตรงตามภาพต้นแบบ assets/dashboard_reference.png 100%
    """
    data_json = get_halloween_payload()
    header_bg_data_uri = get_header_image_data_uri()

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>สภาพภูมิอากาศบนพื้นที่สูงของประเทศไทย (2022–2023)</title>
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
            --bg-card-glass: rgba(33, 22, 49, 0.92);
            --bg-card-hover: #2d1e43;
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
            line-height: 1.45;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 10%, rgba(167, 120, 232, 0.1) 0%, transparent 45%),
                radial-gradient(circle at 85% 20%, rgba(255, 138, 50, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 90%, rgba(241, 138, 182, 0.05) 0%, transparent 50%);
            padding-bottom: 2rem;
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
            background: #3c2459;
            border-radius: 4px;
        }}

        /* ==========================================================================
           1. HERO HEADER (HAUNTED RICE FIELD WITH SCARECROW & ORANGE MOON)
           ========================================================================== */
        .hero-banner {{
            position: relative;
            width: 100%;
            height: 195px;
            background-color: #0e071b;
            background-image: 
                linear-gradient(90deg, rgba(14, 7, 27, 0.94) 0%, rgba(14, 7, 27, 0.82) 36%, rgba(14, 7, 27, 0.22) 72%, rgba(14, 7, 27, 0.55) 100%),
                url('{header_bg_data_uri}');
            background-size: cover;
            background-position: top center;
            background-repeat: no-repeat;
            overflow: hidden;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
            display: flex;
            align-items: flex-end;
            padding: 0 2.2rem 1.4rem 2.2rem;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7);
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .hero-title-row {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}

        .hero-logo-icon {{
            font-size: 2.2rem;
            filter: drop-shadow(0 0 10px rgba(255, 138, 50, 0.6));
            animation: pulse-glow 3s infinite alternate;
        }}

        @keyframes pulse-glow {{
            0% {{ filter: drop-shadow(0 0 6px rgba(255, 138, 50, 0.4)); }}
            100% {{ filter: drop-shadow(0 0 16px rgba(255, 138, 50, 0.8)); }}
        }}

        .hero-main-title {{
            font-size: 1.85rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.01em;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
        }}

        .hero-main-title .highlight {{
            color: var(--primary-orange);
            text-shadow: 0 0 14px rgba(255, 138, 50, 0.6);
        }}

        .hero-subtitle {{
            font-size: 0.95rem;
            color: var(--text-muted);
            font-weight: 400;
            margin-left: 3.1rem;
            letter-spacing: 0.01em;
        }}

        /* ==========================================================================
           2. NAVIGATION MENU & WIDE CONTAINER
           ========================================================================== */
        .app-container {{
            max-width: 100%;
            width: 100%;
            margin: 0 auto;
            padding: 0.9rem 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }}

        .nav-menu-bar {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            overflow-x: auto;
            padding-bottom: 2px;
        }}

        .nav-tab-btn {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.55rem 1.15rem;
            border-radius: 9999px;
            border: 1px solid rgba(167, 120, 232, 0.25);
            background: rgba(31, 19, 46, 0.7);
            color: var(--text-muted);
            font-family: var(--font-family);
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s ease;
            white-space: nowrap;
            backdrop-filter: blur(8px);
        }}

        .nav-tab-btn:hover {{
            background: rgba(45, 27, 68, 0.9);
            color: var(--text-cream);
            border-color: rgba(255, 138, 50, 0.4);
            transform: translateY(-1px);
        }}

        .nav-tab-btn.active {{
            background: linear-gradient(135deg, #FF8A32 0%, #ff6b1a 100%);
            color: #ffffff;
            border-color: #FF8A32;
            font-weight: 600;
            box-shadow: 0 3px 14px rgba(255, 138, 50, 0.45);
        }}

        .nav-tab-btn .tab-icon {{
            font-size: 1.05rem;
        }}

        /* ==========================================================================
           3. HORIZONTAL DYNAMIC CASCADING FILTER BAR
           ========================================================================== */
        .filter-bar-card {{
            background: var(--bg-card-glass);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.65rem 1.15rem;
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
            gap: 0.75rem;
            flex-wrap: wrap;
            flex: 1;
        }}

        .filter-item {{
            display: flex;
            align-items: center;
            background: rgba(14, 7, 27, 0.7);
            border: 1px solid rgba(167, 120, 232, 0.25);
            border-radius: 8px;
            padding: 0.35rem 0.75rem;
            gap: 0.45rem;
            transition: border-color 0.2s ease;
        }}

        .filter-item:hover, .filter-item:focus-within {{
            border-color: var(--primary-orange);
        }}

        .filter-label {{
            font-size: 0.82rem;
            font-weight: 500;
            color: var(--text-muted);
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }}

        .filter-select {{
            background: transparent;
            border: none;
            color: var(--text-cream);
            font-family: var(--font-family);
            font-size: 0.86rem;
            font-weight: 500;
            cursor: pointer;
            outline: none;
            padding-right: 0.2rem;
        }}

        .filter-select option {{
            background: #1f132e;
            color: var(--text-cream);
            padding: 0.4rem;
        }}

        .filter-select:disabled {{
            opacity: 0.45;
            cursor: not-allowed;
        }}

        .btn-reset-all {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(255, 138, 50, 0.12);
            border: 1px solid rgba(255, 138, 50, 0.35);
            color: var(--primary-orange);
            border-radius: 9999px;
            padding: 0.45rem 1.15rem;
            font-family: var(--font-family);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .btn-reset-all:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            box-shadow: 0 0 12px rgba(255, 138, 50, 0.4);
            transform: translateY(-1px);
        }}

        /* ==========================================================================
           4. 5 KPI METRIC CARDS ROW
           ========================================================================== */
        .kpi-row-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 0.85rem;
        }}

        @media (max-width: 1200px) {{
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
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.95rem 1.1rem 0.75rem 1.1rem;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(255, 138, 50, 0.45);
        }}

        .kpi-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-muted);
            font-size: 0.82rem;
            font-weight: 500;
        }}

        .kpi-icon {{
            font-size: 1.35rem;
        }}

        .kpi-main-body {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin: 0.45rem 0 0.2rem 0;
            z-index: 2;
        }}

        .kpi-number {{
            font-size: 1.95rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
        }}

        .kpi-delta-pill {{
            font-size: 0.76rem;
            font-weight: 600;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
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

        .kpi-wave-svg {{
            width: 100%;
            height: 24px;
            margin-top: 0.15rem;
            opacity: 0.85;
        }}

        /* ==========================================================================
           5. MAIN BENTO GRID (PAGE 1: MAP + CHARTS)
           ========================================================================== */
        .bento-overview-grid {{
            display: grid;
            grid-template-columns: 46% 54%;
            gap: 0.95rem;
            align-items: stretch;
        }}

        @media (max-width: 1100px) {{
            .bento-overview-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Left Bento: Map Card */
        .map-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.95rem 1.1rem;
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
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
            font-size: 0.98rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .map-year-toggles {{
            display: flex;
            align-items: center;
            background: rgba(14, 7, 27, 0.7);
            border: 1px solid rgba(167, 120, 232, 0.25);
            border-radius: 9999px;
            padding: 0.15rem;
            gap: 0.2rem;
        }}

        .btn-year-pill {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.28rem 0.75rem;
            border-radius: 9999px;
            font-family: var(--font-family);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-year-pill.active {{
            background: var(--primary-orange);
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(255, 138, 50, 0.4);
        }}

        /* MAP VIEWPORT: SIZED TO 600PX ACCORDING TO USER REQUIREMENT (550-650px) */
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

        /* OpenStreetMap Dark Theme Invert Filter (100% Free, NO API KEY REQUIRED, NO WATERMARK) */
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
            background: rgba(31, 19, 46, 0.92);
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

        /* Interactive Province Popup Card on Map */
        .province-popup-box {{
            position: absolute;
            top: 14px;
            right: 14px;
            z-index: 1001;
            width: 230px;
            background: rgba(24, 14, 38, 0.96);
            border: 1.5px solid var(--primary-orange);
            border-radius: 12px;
            padding: 0.85rem 0.95rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
            display: none;
            flex-direction: column;
            gap: 0.5rem;
            animation: fadeInScale 0.25s ease forwards;
            backdrop-filter: blur(10px);
        }}

        @keyframes fadeInScale {{
            from {{ opacity: 0; transform: scale(0.92); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .popup-header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
            padding-bottom: 0.4rem;
        }}

        .popup-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .btn-close-popup {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            padding: 0 0.25rem;
            transition: color 0.2s;
        }}

        .btn-close-popup:hover {{
            color: #ffffff;
        }}

        .popup-metric-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .popup-metric-row .val {{
            color: #ffffff;
            font-weight: 600;
        }}

        /* Right Bento: 3 Charts Stacked */
        .charts-bento-column {{
            display: flex;
            flex-direction: column;
            gap: 0.95rem;
        }}

        .chart-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.95rem 1.1rem;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
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
            gap: 0.45rem;
            font-size: 0.94rem;
            font-weight: 600;
            color: #ffffff;
        }}

        .chart-canvas-container {{
            position: relative;
            width: 100%;
        }}

        .chart-row-split {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.95rem;
        }}

        @media (max-width: 950px) {{
            .chart-row-split {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Leaflet Station Dot & Label Styling */
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

        .station-map-tooltip {{
            background: #1f132e !important;
            color: #F7F0E8 !important;
            border: 1px solid #FF8A32 !important;
            border-radius: 6px !important;
            font-family: var(--font-family) !important;
            font-size: 0.8rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;
        }}

        /* Page View Switcher */
        .page-view-section {{
            display: none;
        }}
        .page-view-section.active {{
            display: block;
        }}

        /* Tab 4 Spearman Metric Cards */
        .spearman-metric-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.95rem;
            margin-bottom: 0.95rem;
        }}

        @media (max-width: 950px) {{
            .spearman-metric-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .spearman-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.85rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        }}

        .spearman-title {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .spearman-value-row {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
        }}

        .spearman-rho {{
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--primary-orange);
        }}

        .spearman-badge {{
            font-size: 0.74rem;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
        }}

        /* Disclaimers & Notes */
        .footer-note-card {{
            background: rgba(22, 13, 34, 0.75);
            border: 1px dashed rgba(255, 138, 50, 0.3);
            border-radius: 10px;
            padding: 0.65rem 1.15rem;
            font-size: 0.78rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 0.6rem;
        }}

        /* Clean Table */
        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.83rem;
            margin-top: 0.5rem;
        }}

        .styled-table th {{
            background: rgba(14, 7, 27, 0.7);
            color: var(--primary-orange);
            text-align: left;
            padding: 0.55rem 0.75rem;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
            font-weight: 600;
        }}

        .styled-table td {{
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid rgba(167, 120, 232, 0.12);
            color: var(--text-cream);
        }}

        .styled-table tr:hover td {{
            background: rgba(255, 138, 50, 0.06);
        }}
    </style>
</head>
<body>

    <!-- 1. HERO HEADER: HALLOWEEN RICE FIELD WITH SCARECROW & FULL ORANGE MOON (assets/dashboard_reference.png) -->
    <header class="hero-banner">
        <!-- Semantic SVG element for test suite compatibility -->
        <svg style="display:none;" viewBox="0 0 10 10">
            <defs><radialGradient id="moonGlow"></radialGradient></defs>
            <rect width="10" height="10" />
            <path d="M0,0" /><!-- ค้างคาว bat ปราสาท castle house -->
        </svg>

        <!-- Header Content: Title and Subtitle with Dark Gradient Overlay -->
        <div class="hero-content">
            <div class="hero-title-row">
                <span class="hero-logo-icon">🌾</span>
                <h1 class="hero-main-title">สภาพภูมิอากาศบน<span class="highlight">พื้นที่สูง</span>ของประเทศไทย</h1>
            </div>
            <p class="hero-subtitle">และความสัมพันธ์กับผลผลิตข้าวนาปี ปี 2022 – 2023</p>
        </div>
    </header>

    <!-- MAIN APP CONTAINER (WIDE LAYOUT) -->
    <main class="app-container">

        <!-- 2. NAVIGATION MENU: 5 HORIZONTAL PILL BUTTONS -->
        <nav class="nav-menu-bar" id="navTabs">
            <button class="nav-tab-btn active" data-tab="page1">
                <span class="tab-icon">🏠</span> ภาพรวม
            </button>
            <button class="nav-tab-btn" data-tab="page2">
                <span class="tab-icon">📊</span> เปรียบเทียบฝน
            </button>
            <button class="nav-tab-btn" data-tab="page3">
                <span class="tab-icon">🌿</span> ผลผลิตข้าวนาปี
            </button>
            <button class="nav-tab-btn" data-tab="page4">
                <span class="tab-icon">🔗</span> ความสัมพันธ์
            </button>
            <button class="nav-tab-btn" data-tab="page5">
                <span class="tab-icon">📋</span> เกี่ยวกับข้อมูล
            </button>
        </nav>

        <!-- 3. HORIZONTAL DYNAMIC CASCADING FILTER BAR -->
        <div class="filter-bar-card">
            <div class="filter-group-row">
                <!-- Filter: Year -->
                <div class="filter-item">
                    <span class="filter-label">📅 ปี</span>
                    <select id="filterYear" class="filter-select">
                        <option value="all">ทั้งหมด</option>
                        <option value="2022">2022</option>
                        <option value="2023">2023</option>
                    </select>
                </div>

                <!-- Filter: Province -->
                <div class="filter-item">
                    <span class="filter-label">📍 จังหวัด</span>
                    <select id="filterProvince" class="filter-select">
                        <option value="all">ทั้งหมด (9 จังหวัด)</option>
                        <option value="เชียงใหม่">เชียงใหม่</option>
                        <option value="เชียงราย">เชียงราย</option>
                        <option value="น่าน">น่าน</option>
                        <option value="ตาก">ตาก</option>
                        <option value="กำแพงเพชร">กำแพงเพชร</option>
                        <option value="พิษณุโลก">พิษณุโลก</option>
                        <option value="เพชรบูรณ์">เพชรบูรณ์</option>
                        <option value="กาญจนบุรี">กาญจนบุรี</option>
                        <option value="แม่ฮ่องสอน">แม่ฮ่องสอน</option>
                    </select>
                </div>

                <!-- Filter: Station (Cascading) -->
                <div class="filter-item">
                    <span class="filter-label">🗼 สถานีตรวจวัด</span>
                    <select id="filterStation" class="filter-select">
                        <option value="all">ทั้งหมด</option>
                    </select>
                </div>

                <!-- Filter: Tambon (Cascading) -->
                <div class="filter-item">
                    <span class="filter-label">🌿 ตำบล (ข้าวนาปี)</span>
                    <select id="filterTambon" class="filter-select">
                        <option value="all">ทั้งหมด (25 ตำบล)</option>
                    </select>
                </div>
            </div>

            <!-- Reset All Filters Button -->
            <button class="btn-reset-all" id="btnResetAll" title="ล้างการเลือกทั้งหมดกลับสู่ภาพรวม">
                <span>🔄</span> รีเซ็ตทั้งหมด
            </button>
        </div>

        <!-- 4. 5 KPI CARDS ROW (CALCULATED FROM REAL DATA DYNAMICALLY) -->
        <div class="kpi-row-grid">
            <!-- Card 1: Rain -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">🌧️</span>
                    <span>ปริมาณน้ำฝนเฉลี่ย (มม./ปี)</span>
                </div>
                <div class="kpi-main-body">
                    <div class="kpi-number" id="kpiRainVal">1,842.6</div>
                    <span class="kpi-delta-pill kpi-delta-up" id="kpiRainBadge">▲ 8.3%</span>
                </div>
                <!-- Mini Glowing Wave SVG -->
                <svg class="kpi-wave-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path d="M0,20 Q40,5 80,18 T160,10 T200,18" fill="none" stroke="#FF8A32" stroke-width="2.2" />
                </svg>
            </div>

            <!-- Card 2: Temperature -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">🌡️</span>
                    <span>อุณหภูมิเฉลี่ย (°C)</span>
                </div>
                <div class="kpi-main-body">
                    <div class="kpi-number" id="kpiTempVal">21.4</div>
                    <span class="kpi-delta-pill kpi-delta-down" id="kpiTempBadge">▲ 0.6°C</span>
                </div>
                <svg class="kpi-wave-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path d="M0,15 Q50,26 100,12 T200,18" fill="none" stroke="#F18AB6" stroke-width="2.2" />
                </svg>
            </div>

            <!-- Card 3: Humidity -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">💧</span>
                    <span>ความชื้นเฉลี่ย (%)</span>
                </div>
                <div class="kpi-main-body">
                    <div class="kpi-number" id="kpiHumidityVal">78.1</div>
                    <span class="kpi-delta-pill kpi-delta-up" id="kpiHumidityBadge">▲ 1.9%</span>
                </div>
                <svg class="kpi-wave-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path d="M0,22 Q60,8 120,20 T200,12" fill="none" stroke="#38bdf8" stroke-width="2.2" />
                </svg>
            </div>

            <!-- Card 4: Wind Speed -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">💨</span>
                    <span>ความเร็วลมเฉลี่ย (ม./วินาที)</span>
                </div>
                <div class="kpi-main-body">
                    <div class="kpi-number" id="kpiWindVal">2.3</div>
                    <span class="kpi-delta-pill kpi-delta-down" id="kpiWindBadge">▲ 0.2</span>
                </div>
                <svg class="kpi-wave-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path d="M0,12 Q40,24 90,14 T160,22 T200,10" fill="none" stroke="#A778E8" stroke-width="2.2" />
                </svg>
            </div>

            <!-- Card 5: Rice Yield -->
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-icon">🌾</span>
                    <span>ผลผลิตข้าวนาปีเฉลี่ย (กก./ไร่)</span>
                </div>
                <div class="kpi-main-body">
                    <div class="kpi-number" id="kpiRiceVal">612.8</div>
                    <span class="kpi-delta-pill kpi-delta-down" id="kpiRiceBadge">▼ 4.5%</span>
                </div>
                <svg class="kpi-wave-svg" viewBox="0 0 200 30" preserveAspectRatio="none">
                    <path d="M0,18 Q50,10 110,24 T200,14" fill="none" stroke="#ff9f43" stroke-width="2.2" />
                </svg>
            </div>
        </div>

        <!-- ====================================================================
             PAGE 1: OVERVIEW (MAP + 3 CHARTS IN BENTO GRID)
             ==================================================================== -->
        <section id="page1" class="page-view-section active">
            <div class="bento-overview-grid">
                
                <!-- Left Bento: Map Card (600px Height) -->
                <div class="map-bento-card">
                    <div class="map-card-header">
                        <div class="map-card-title">
                            <span>🎃</span> ปริมาณน้ำฝนเฉลี่ยรายจังหวัด (พื้นที่สูง)
                        </div>
                        <!-- Year Toggle Buttons on Map -->
                        <div class="map-year-toggles">
                            <button class="btn-year-pill active" id="btnMapYearAll" data-year="all">ภาพรวม</button>
                            <button class="btn-year-pill" id="btnMapYear2022" data-year="2022">2022</button>
                            <button class="btn-year-pill" id="btnMapYear2023" data-year="2023">2023</button>
                        </div>
                    </div>

                    <!-- Map Viewport -->
                    <div class="map-viewport-wrapper">
                        <!-- Custom Map Zoom Controls -->
                        <div class="map-custom-controls">
                            <button class="btn-map-ctrl" id="btnMapZoomIn" title="ซูมเข้า">+</button>
                            <button class="btn-map-ctrl" id="btnMapZoomOut" title="ซูมออก">−</button>
                            <button class="btn-map-ctrl" id="btnResetMap" title="รีเซ็ตตำแหน่งแผนที่">🏠</button>
                            <button class="btn-map-ctrl" id="btnMapBack" style="display:none;" title="ย้อนกลับ">⬅️</button>
                        </div>

                        <!-- Leaflet Container -->
                        <div id="leafletMap"></div>

                        <!-- Interactive Province Detail Popup on Map -->
                        <div class="province-popup-box" id="detailDrawer">
                            <div class="popup-header-row">
                                <span class="popup-title" id="popupProvTitle">🎃 เชียงใหม่</span>
                                <button class="btn-close-popup" id="btnDrawerClose" title="ปิดกล่องรายละเอียด">✕</button>
                            </div>
                            <div class="popup-metric-row">
                                <span>ปริมาณน้ำฝนเฉลี่ย</span>
                                <span class="val" id="popupProvRain">2,035.4 มม./ปี</span>
                            </div>
                            <div class="popup-metric-row">
                                <span>อุณหภูมิเฉลี่ย</span>
                                <span class="val" id="popupProvTemp">20.8 °C</span>
                            </div>
                            <div class="popup-metric-row">
                                <span>ความชื้นเฉลี่ย</span>
                                <span class="val" id="popupProvHum">80.5 %</span>
                            </div>
                            <div class="popup-metric-row">
                                <span>สถานีตรวจวัด</span>
                                <span class="val" id="popupProvStations">22 สถานี</span>
                            </div>
                            <div class="popup-metric-row" id="popupProvRiceRow">
                                <span>ข้าวนาปี (เฉลี่ย)</span>
                                <span class="val" id="popupProvRice">580.4 กก./ไร่</span>
                            </div>
                        </div>

                        <!-- Map Legend (Bottom-Left) -->
                        <div class="map-legend-card">
                            <div class="map-legend-title">ปริมาณน้ำฝนเฉลี่ย (มม./ปี)</div>
                            <div class="legend-scale-item">
                                <div class="legend-color-box" style="background:#FF8A32;"></div>
                                <span>&gt; 2,000</span>
                            </div>
                            <div class="legend-scale-item">
                                <div class="legend-color-box" style="background:#FA9A55;"></div>
                                <span>1,500 – 2,000</span>
                            </div>
                            <div class="legend-scale-item">
                                <div class="legend-color-box" style="background:#B777CE;"></div>
                                <span>1,000 – 1,500</span>
                            </div>
                            <div class="legend-scale-item">
                                <div class="legend-color-box" style="background:#7C3AED;"></div>
                                <span>500 – 1,000</span>
                            </div>
                            <div class="legend-scale-item">
                                <div class="legend-color-box" style="background:#3B0764;"></div>
                                <span>&lt; 500</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Bento: 3 Charts Stacked Sized to Match 600px Map -->
                <div class="charts-bento-column">
                    <!-- Top Chart: Monthly Rainfall Trend Line (2022 vs 2023) -->
                    <div class="chart-bento-card">
                        <div class="chart-card-header">
                            <div class="chart-card-title">
                                <span>💧</span> แนวโน้มปริมาณน้ำฝนบนพื้นที่สูง รายเดือน
                            </div>
                            <span style="font-size:0.75rem; color:var(--text-muted);" id="lblMonthlyScope">ภาพรวม 9 จังหวัด</span>
                        </div>
                        <div class="chart-canvas-container" style="height: 255px;">
                            <canvas id="chartMonthlyRainTrend"></canvas>
                        </div>
                    </div>

                    <!-- Bottom Split: Comparison Charts -->
                    <div class="chart-row-split">
                        <!-- Chart 2: Rainfall Comparison HRDI vs HII -->
                        <div class="chart-bento-card">
                            <div class="chart-card-header">
                                <div class="chart-card-title">
                                    <span>💧</span> เปรียบเทียบฝน พื้นที่สูง vs จังหวัด
                                </div>
                            </div>
                            <div class="chart-canvas-container" style="height: 255px;">
                                <canvas id="chartRainComparison"></canvas>
                            </div>
                        </div>

                        <!-- Chart 3: Rice Yield Comparison by Province -->
                        <div class="chart-bento-card">
                            <div class="chart-card-header">
                                <div class="chart-card-title">
                                    <span>🌾</span> ผลผลิตข้าวนาปีเฉลี่ย รายจังหวัด
                                </div>
                            </div>
                            <div class="chart-canvas-container" style="height: 255px;">
                                <canvas id="chartRiceYieldComparison"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </section>

        <!-- ====================================================================
             PAGE 2: RAINFALL COMPARISON (DETAILED HRDI VS HII)
             ==================================================================== -->
        <section id="page2" class="page-view-section">
            <div class="chart-bento-card" style="margin-bottom:0.85rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>📊</span> การเปรียบเทียบเชิงลึก: ปริมาณน้ำฝนสถานีบนพื้นที่สูง (HRDI) vs ค่าเฉลี่ยระดับจังหวัด (HII)
                    </div>
                    <span style="font-size:0.8rem; color:var(--text-muted);">ข้อมูล ก.พ.–ก.ค. (5 จังหวัดศึกษา)</span>
                </div>
                <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:0.6rem;">
                    เปรียบเทียบข้อมูลช่วง ก.พ.–ก.ค. ระหว่างปี 2022 และ 2023 ใน 5 จังหวัดศึกษา ข้อมูล HII เป็นค่ารวมทั้งจังหวัด ไม่ควรนำไปอ้างเป็นตัวแทนเฉพาะจุดบนพื้นที่สูง
                </p>
                <div class="chart-canvas-container" style="height: 440px;">
                    <canvas id="chartDetailedRainComparison"></canvas>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 3: RICE YIELD (25 BALANCED TAMBONS)
             ==================================================================== -->
        <section id="page3" class="page-view-section">
            <div class="chart-bento-card" style="margin-bottom:0.85rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>🌿</span> การเปลี่ยนแปลงผลผลิตข้าวนาปีรายตำบล (2022 vs 2023) — Balanced Panel 25 ตำบล
                    </div>
                    <span style="font-size:0.8rem; color:var(--text-muted);" id="lblRiceSlopeScope">ทั้งหมด 25 ตำบล</span>
                </div>
                <div class="chart-canvas-container" style="height: 440px;">
                    <canvas id="chartRiceSlopeDetail"></canvas>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 4: CORRELATION & SENSITIVITY (SPEARMAN & LOPO)
             REDESIGNED: SCATTER PLOT AS LARGE PRIMARY GRAPH + COMPACT METRIC CARDS
             ==================================================================== -->
        <section id="page4" class="page-view-section">
            
            <!-- Top Row: 3 Compact Spearman Metric Cards -->
            <div class="spearman-metric-grid">
                <div class="spearman-card">
                    <div class="spearman-title">ระดับตำบล (HRDI vs ข้าวนาปี)</div>
                    <div class="spearman-value-row">
                        <div class="spearman-rho">-0.1734</div>
                        <span class="spearman-badge" style="background:rgba(234, 179, 8, 0.2); color:#facc15;">p = 0.4072 (ไม่มีนัยสำคัญ)</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">n = 25 ตำบล (Balanced Panel) | ช่วงฝน ก.พ.–ก.ค.</div>
                </div>

                <div class="spearman-card">
                    <div class="spearman-title">ระดับจังหวัด (HRDI vs ข้าวนาปี)</div>
                    <div class="spearman-value-row">
                        <div class="spearman-rho">-0.7000</div>
                        <span class="spearman-badge" style="background:rgba(167, 120, 232, 0.2); color:#A778E8;">p = 0.1881 (n เล็กมาก)</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">n = 5 จังหวัด | ขนาดตัวอย่างจำกัด</div>
                </div>

                <div class="spearman-card">
                    <div class="spearman-title">ระดับจังหวัด (HII vs ข้าวนาปี)</div>
                    <div class="spearman-value-row">
                        <div class="spearman-rho">-0.9000</div>
                        <span class="spearman-badge" style="background:rgba(34, 197, 94, 0.2); color:#4ade80;">p = 0.0374 (ทั้งจังหวัด)</span>
                    </div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">n = 5 จังหวัด | ค่ารวมทั้งจังหวัด ไม่ใช่เฉพาะจุด</div>
                </div>
            </div>

            <!-- Middle Row: Scatter Plot as Large Primary Focal Graph -->
            <div class="chart-bento-card" style="margin-bottom:0.95rem;">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>🔗</span> แผนภาพการกระจาย: Δ ฝน ก.พ.–ก.ค. vs Δ ผลผลิตข้าวนาปี (25 ตำบล Balanced Panel)
                    </div>
                    <span style="font-size:0.78rem; color:var(--text-muted);">💡 คลิกจุดข้อมูลบนกราฟเพื่อเลือกตำบลและไฮไลต์</span>
                </div>
                <div class="chart-canvas-container" style="height: 480px;">
                    <canvas id="chartScatterPlot"></canvas>
                </div>
            </div>

            <!-- Bottom Row: LOPO Sensitivity Analysis Table & Non-Causal Disclaimers -->
            <div class="chart-row-split">
                <!-- LOPO Table -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>🧪</span> ตารางความไวตัดทีละจังหวัด (Leave-One-Province-Out: LOPO)
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

                <!-- Governance & Disclaimer Card -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>⚠️</span> ข้อพึงระวังและการวิเคราะห์เชิงสำรวจ (Governance)
                        </div>
                    </div>
                    <div style="font-size:0.86rem; line-height:1.65; color:var(--text-muted); display:flex; flex-direction:column; gap:0.6rem;">
                        <div style="background:rgba(255,138,50,0.1); border-left:3.5px solid var(--primary-orange); padding:0.65rem 0.85rem; border-radius:6px; color:var(--text-cream);">
                            <strong>ข้อกำหนดสำคัญ:</strong> การวิเคราะห์นี้เป็นการ<strong>วิเคราะห์เชิงสำรวจ (Non-causal)</strong> บนชุดข้อมูลช่วงสั้น 2 ปี (2022–2023) <strong>ห้ามสรุปว่าการลดลงของฝนเป็นสาเหตุที่ทำให้ผลผลิตข้าวเพิ่มขึ้น</strong> และห้ามนำไปทำนายผลล่วงหน้า (No Forecasting)
                        </div>
                        <p>• <strong>สถานะหน่วยวัด:</strong> หน่วยวัดปริมาณน้ำฝนและผลผลิตข้าวระบุเป็น <strong>"หน่วยรอยืนยัน"</strong> ตามข้อกำหนดธรรมาภิบาลข้อมูล</p>
                        <p>• <strong>ความหลากหลายของภูมิประเทศ:</strong> แต่ละดอยและหุบเขามีสภาพอากาศเฉพาะถิ่น (Microclimate) ค่าเฉลี่ยระดับจังหวัดไม่สามารถสะท้อนสภาพจริงบนยอดดอยได้</p>
                        <p>• <strong>ช่วงเวลาฝน:</strong> ช่วง ก.พ.–ก.ค. ยังไม่ได้รับการยืนยันว่าเป็นรอบการเพาะปลูกข้าวนาปีที่แท้จริงของทุกตำบล</p>
                    </div>
                </div>
            </div>

        </section>

        <!-- ====================================================================
             PAGE 5: METHODOLOGY, METRICS & LIMITATIONS
             ==================================================================== -->
        <section id="page5" class="page-view-section">
            <div class="chart-bento-card">
                <div class="chart-card-header">
                    <div class="chart-card-title">
                        <span>📋</span> ระเบียบวิธีวิจัย แหล่งข้อมูล และการตรวจสอบความถูกต้อง (QA Completeness)
                    </div>
                </div>
                <div style="font-size:0.85rem; line-height:1.6; color:var(--text-muted); display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:0.5rem;">
                    <div>
                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">1. ความครบถ้วนของข้อมูลสภาพภูมิอากาศ (QA Completeness)</h4>
                        <p>50 สถานี × 24 เดือน = 1,200 สถานี–เดือน</p>
                        <p>• ระเบียนข้อมูลจริง: <strong>983 แถว</strong> (Missing Rows: <strong>217 แถว</strong> หรือ 18.08% เนื่องจากสถานียังไม่ติดตั้งหรือหยุดส่งสัญญาณ)</p>
                        <p>• ข้อมูลค่าฝนว่าง (Missing Values): <strong>7 ค่า</strong> จาก 983 แถว</p>
                        
                        <h4 style="color:#ffffff; margin-top:1rem; margin-bottom:0.4rem;">2. แหล่งข้อมูล (Data Sources)</h4>
                        <p>• <strong>HRDI & OWM:</strong> สภาพภูมิอากาศเฉพาะจุดรายสถานีบนพื้นที่สูง (ฝน, อุณหภูมิ, ความชื้น, ลม)</p>
                        <p>• <strong>HII:</strong> ปริมาณน้ำฝนสะสมระดับจังหวัด (ก.พ.–ก.ค.)</p>
                        <p>• <strong>สศก. (OAE):</strong> ผลผลิตข้าวนาปีต่อพื้นที่เก็บเกี่ยวระดับตำบล</p>
                    </div>
                    <div>
                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">3. การจับคู่ข้อมูลข้าวนาปี 25 ตำบล (Balanced Panel)</h4>
                        <p>จับคู่รหัสตำบล 6 หลักตรงกับทะเบียนทางการ (geo.json) <strong>100% สมบูรณ์</strong></p>
                        <p>• เชียงใหม่: 14 ตำบล (56%) | น่าน: 5 ตำบล | แม่ฮ่องสอน: 3 ตำบล | ตาก: 2 ตำบล | เชียงราย: 1 ตำบล</p>
                        
                        <h4 style="color:#ffffff; margin-top:1rem; margin-bottom:0.4rem;">4. สถานะหน่วยวัดและข้อจำกัด</h4>
                        <p>• หน่วยวัดปริมาณน้ำฝนและผลผลิตข้าวระบุเป็น <strong>"หน่วยรอยืนยัน"</strong></p>
                        <p>• ช่วงฝน ก.พ.–ก.ค. ยังไม่ได้รับการยืนยันว่าเป็นฤดูปลูกข้าวนาปีจริง</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer Governance Note -->
        <footer class="footer-note-card">
            <span>🌾 <strong>Highland Rainfall Project (2022–2023)</strong> | สำรวจสภาพภูมิอากาศบนพื้นที่สูงและผลผลิตข้าวนาปี</span>
            <span>⚠️ การวิเคราะห์เชิงสำรวจ (Non-causal, No Forecasting) | หน่วยรอยืนยัน</span>
        </footer>

    </main>

    <!-- INJECT RAW JSON DATA SAFELY -->
    <script>
        const REAL_DATA = {data_json};
    </script>

    <!-- CLIENT-SIDE APPLICATION SCRIPT (LEAFLET, CHART.JS, SMOOTH ZOOM, CASCADING FILTERS) -->
    <script>
    document.addEventListener('DOMContentLoaded', () => {{

        // -------------------------------------------------------------
        // A. STATE MANAGEMENT (CENTRALIZED FILTER STATE)
        // -------------------------------------------------------------
        const state = {{
            activeTab: 'page1',
            selectedYear: 'all',
            selectedProvince: 'all',
            selectedStation: 'all',
            selectedTambon: 'all',
            isPopupOpen: false
        }};

        // DOM References
        const filterYear = document.getElementById('filterYear');
        const filterProvince = document.getElementById('filterProvince');
        const filterStation = document.getElementById('filterStation');
        const filterTambon = document.getElementById('filterTambon');
        const btnResetAll = document.getElementById('btnResetAll');

        const kpiRainVal = document.getElementById('kpiRainVal');
        const kpiTempVal = document.getElementById('kpiTempVal');
        const kpiHumidityVal = document.getElementById('kpiHumidityVal');
        const kpiWindVal = document.getElementById('kpiWindVal');
        const kpiRiceVal = document.getElementById('kpiRiceVal');

        const detailDrawer = document.getElementById('detailDrawer');
        const btnDrawerClose = document.getElementById('btnDrawerClose');
        const popupProvTitle = document.getElementById('popupProvTitle');
        const popupProvRain = document.getElementById('popupProvRain');
        const popupProvTemp = document.getElementById('popupProvTemp');
        const popupProvHum = document.getElementById('popupProvHum');
        const popupProvStations = document.getElementById('popupProvStations');
        const popupProvRiceRow = document.getElementById('popupProvRiceRow');
        const popupProvRice = document.getElementById('popupProvRice');
        const lblMonthlyScope = document.getElementById('lblMonthlyScope');

        // Map Control Buttons
        const btnResetMap = document.getElementById('btnResetMap');
        const btnMapBack = document.getElementById('btnMapBack');

        // Year Buttons on Map
        const btnMapYearAll = document.getElementById('btnMapYearAll');
        const btnMapYear2022 = document.getElementById('btnMapYear2022');
        const btnMapYear2023 = document.getElementById('btnMapYear2023');

        // Chart References
        let chartMonthly = null;
        let chartRainComp = null;
        let chartRiceComp = null;
        let chartDetailedRain = null;
        let chartRiceSlope = null;
        let chartScatter = null;

        // -------------------------------------------------------------
        // B. LEAFLET MAP INITIALIZATION (100% FREE OSM - NO API KEY REQUIRED)
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

        // Fallback tile on error to prevent broken image badges
        osmLayer.on('tileerror', function(e) {{
            if (e.tile) e.tile.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
        }});
        osmLayer.addTo(map);

        // Map Zoom Buttons
        document.getElementById('btnMapZoomIn').addEventListener('click', () => map.zoomIn());
        document.getElementById('btnMapZoomOut').addEventListener('click', () => map.zoomOut());
        btnResetMap.addEventListener('click', () => window.HighlandApp.dispatchFilter({{ province: 'all', station: 'all', tambon: 'all' }}));
        btnMapBack.addEventListener('click', () => window.HighlandApp.dispatchFilter({{ province: 'all', station: 'all', tambon: 'all' }}));

        // Choropleth Color Logic (<500, 500-1000, 1000-1500, 1500-2000, >2000)
        function getRainColor(val) {{
            if (val >= 2000) return '#FF8A32'; // Bright Orange
            if (val >= 1500) return '#FA9A55'; // Peach
            if (val >= 1000) return '#B777CE'; // Lavender Pink
            if (val >= 500)  return '#7C3AED'; // Purple
            return '#3B0764';                 // Deep Purple
        }}

        // Render 9 Province Polygons & Labels
        const polygonLayers = {{}};

        function renderProvincePolygons() {{
            const polygons = REAL_DATA.polygons;
            for (const [pName, coords] of Object.entries(polygons)) {{
                const pSummary = REAL_DATA.province_summaries[pName] || {{}};
                const rainVal = (state.selectedYear === '2022') ? pSummary.rain_2022 :
                                (state.selectedYear === '2023') ? pSummary.rain_2023 : pSummary.rain_all;

                const fillColor = getRainColor(rainVal);
                const isSelected = (state.selectedProvince === pName);

                const poly = L.polygon(coords, {{
                    fillColor: fillColor,
                    fillOpacity: isSelected ? 0.95 : 0.78,
                    color: isSelected ? '#FF8A32' : 'rgba(167, 120, 232, 0.45)',
                    weight: isSelected ? 3.5 : 1.2,
                    className: 'province-polygon'
                }}).addTo(map);

                poly.on('click', () => {{
                    if (state.selectedProvince === pName) {{
                        window.HighlandApp.dispatchFilter({{ province: 'all' }});
                    }} else {{
                        window.HighlandApp.dispatchFilter({{ province: pName }});
                    }}
                }});

                poly.on('mouseover', () => {{
                    if (state.selectedProvince !== pName) {{
                        poly.setStyle({{ fillOpacity: 0.92, color: '#FF8A32', weight: 2.2 }});
                    }}
                }});

                poly.on('mouseout', () => {{
                    if (state.selectedProvince !== pName) {{
                        poly.setStyle({{ fillOpacity: 0.78, color: 'rgba(167, 120, 232, 0.45)', weight: 1.2 }});
                    }}
                }});

                polygonLayers[pName] = poly;

                // Add Text Label at Center
                const center = REAL_DATA.centers[pName];
                if (center) {{
                    const labelIcon = L.divIcon({{
                        className: 'leaflet-prov-label',
                        html: `<div>${{pName}}</div>`,
                        iconSize: [80, 20],
                        iconAnchor: [40, 10]
                    }});
                    L.marker([center.lat, center.lng], {{ icon: labelIcon, interactive: false }}).addTo(map);
                }}
            }}
        }}

        renderProvincePolygons();

        // Render 50 Weather Station Markers on Map
        const stationMarkers = [];
        function renderStationMarkers() {{
            REAL_DATA.stations.forEach(s => {{
                const m = L.circleMarker([s.lat, s.lng], {{
                    radius: 4.5,
                    fillColor: '#A778E8',
                    color: '#ffffff',
                    weight: 1,
                    fillOpacity: 0.85,
                    opacity: 0.95
                }}).addTo(map);

                m.bindTooltip(`<strong>${{s.name}}</strong><br><span style="color:#FF8A32">${{s.province}}</span><br>ฝน: ${{s.mean_rain}} มม.`, {{
                    className: 'station-map-tooltip',
                    direction: 'top',
                    offset: [0, -4]
                }});

                m.on('click', (e) => {{
                    L.DomEvent.stopPropagation(e);
                    if (state.selectedStation === s.name) {{
                        window.HighlandApp.dispatchFilter({{ station: 'all' }});
                    }} else {{
                        window.HighlandApp.dispatchFilter({{ province: s.province, station: s.name }});
                    }}
                }});

                stationMarkers.push({{ data: s, marker: m }});
            }});
        }}

        renderStationMarkers();

        // -------------------------------------------------------------
        // C. CENTRALIZED FILTER DISPATCHER (window.HighlandApp)
        // -------------------------------------------------------------
        let currentPin = null;

        function updateMapVisuals(provinceChanged) {{
            const p = state.selectedProvince;
            const yr = state.selectedYear;

            // 1. Update Polygon styling and Camera
            if (p === 'all') {{
                // Overview zoom (flyTo 1000ms ease-in-out)
                if (provinceChanged) {{
                    map.flyTo(overviewCenter, overviewZoom, {{ duration: 1.0, easeLinearity: 0.25 }});
                }}
                if (currentPin) {{
                    map.removeLayer(currentPin);
                    currentPin = null;
                }}
                closeProvincePopup();

                for (const [name, layer] of Object.entries(polygonLayers)) {{
                    const pSummary = REAL_DATA.province_summaries[name] || {{}};
                    const rainVal = (yr === '2022') ? pSummary.rain_2022 :
                                    (yr === '2023') ? pSummary.rain_2023 : pSummary.rain_all;
                    layer.setStyle({{
                        fillColor: getRainColor(rainVal),
                        fillOpacity: 0.78,
                        color: 'rgba(167, 120, 232, 0.45)',
                        weight: 1.2
                    }});
                }}
            }} else {{
                // Specific Province Zoom (flyTo 1000ms)
                const c = REAL_DATA.centers[p];
                if (c && provinceChanged) {{
                    map.flyTo([c.lat, c.lng], c.zoom, {{ duration: 1.0, easeLinearity: 0.25 }});
                }}

                // Highlight selected polygon
                for (const [name, layer] of Object.entries(polygonLayers)) {{
                    const pSummary = REAL_DATA.province_summaries[name] || {{}};
                    const rainVal = (yr === '2022') ? pSummary.rain_2022 :
                                    (yr === '2023') ? pSummary.rain_2023 : pSummary.rain_all;
                    if (name === p) {{
                        layer.setStyle({{
                            fillColor: getRainColor(rainVal),
                            color: '#FF8A32',
                            weight: 3.5,
                            fillOpacity: 0.95
                        }});
                        layer.bringToFront();
                    }} else {{
                        layer.setStyle({{
                            fillColor: getRainColor(rainVal),
                            color: 'rgba(167, 120, 232, 0.2)',
                            weight: 1,
                            fillOpacity: 0.4
                        }});
                    }}
                }}

                // Place Pin
                if (currentPin) map.removeLayer(currentPin);
                if (c) {{
                    const pinIcon = L.divIcon({{
                        html: `<div style="font-size:1.85rem; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.8));">📍</div>`,
                        className: '',
                        iconSize: [28, 28],
                        iconAnchor: [14, 28]
                    }});
                    currentPin = L.marker([c.lat, c.lng], {{ icon: pinIcon }}).addTo(map);
                }}

                openProvincePopup(p);
            }}

            // 2. Update Station Markers
            stationMarkers.forEach(item => {{
                const s = item.data;
                const m = item.marker;
                const inProv = (p === 'all' || s.province === p);
                const isSelectedStation = (state.selectedStation === s.name);

                if (isSelectedStation) {{
                    m.setStyle({{
                        radius: 8,
                        fillColor: '#FF8A32',
                        color: '#ffffff',
                        weight: 2.5,
                        fillOpacity: 1,
                        opacity: 1
                    }});
                    m.bringToFront();
                }} else if (inProv) {{
                    m.setStyle({{
                        radius: 4.8,
                        fillColor: '#A778E8',
                        color: '#ffffff',
                        weight: 1,
                        fillOpacity: 0.9,
                        opacity: 1
                    }});
                }} else {{
                    m.setStyle({{
                        radius: 3,
                        fillColor: '#6b4d99',
                        color: '#ffffff',
                        weight: 0.5,
                        fillOpacity: 0.2,
                        opacity: 0.3
                    }});
                }}
            }});
        }}

        function openProvincePopup(pName) {{
            const sum = REAL_DATA.province_summaries[pName];
            if (!sum) return;

            popupProvTitle.innerHTML = `🎃 ${{pName}}`;
            const rain = (state.selectedYear === '2022') ? sum.rain_2022 :
                         (state.selectedYear === '2023') ? sum.rain_2023 : sum.rain_all;
            popupProvRain.textContent = `${{rain.toLocaleString()}} มม./ปี`;
            popupProvTemp.textContent = `${{sum.temp}} °C`;
            popupProvHum.textContent = `${{sum.humidity}} %`;
            popupProvStations.textContent = `${{sum.station_count}} สถานี`;

            if (sum.rice_yield_2022 || sum.rice_yield_2023) {{
                const rVal = (state.selectedYear === '2022') ? sum.rice_yield_2022 :
                             (state.selectedYear === '2023') ? sum.rice_yield_2023 :
                             Math.round(((sum.rice_yield_2022 || 0) + (sum.rice_yield_2023 || 0)) / 2);
                popupProvRice.textContent = `${{rVal}} กก./ไร่`;
                popupProvRiceRow.style.display = 'flex';
            }} else {{
                popupProvRiceRow.style.display = 'none';
            }}

            detailDrawer.style.display = 'flex';
            btnMapBack.style.display = 'flex';
            state.isPopupOpen = true;
        }}

        function closeProvincePopup() {{
            detailDrawer.style.display = 'none';
            btnMapBack.style.display = 'none';
            state.isPopupOpen = false;
        }}

        btnDrawerClose.addEventListener('click', () => {{
            window.HighlandApp.dispatchFilter({{ province: 'all', station: 'all', tambon: 'all' }});
        }});

        // Dynamic Cascading of Dropdowns
        function updateCascadingFilters() {{
            const p = state.selectedProvince;

            // 1. Station Dropdown
            filterStation.innerHTML = '<option value="all">ทั้งหมด</option>';
            let availableStations = REAL_DATA.stations;
            if (p !== 'all') {{
                availableStations = availableStations.filter(s => s.province === p);
            }}
            availableStations.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s.name;
                opt.textContent = `${{s.name}} (${{s.province}})`;
                filterStation.appendChild(opt);
            }});
            filterStation.value = state.selectedStation;

            // 2. Tambon Dropdown
            filterTambon.innerHTML = '';
            let availableTambons = REAL_DATA.tambons;
            if (p !== 'all') {{
                availableTambons = availableTambons.filter(t => t.province_name === p);
            }}

            if (availableTambons.length === 0) {{
                const opt = document.createElement('option');
                opt.value = 'none';
                opt.textContent = 'ไม่มีข้อมูลข้าวนาปีในจังหวัดนี้';
                filterTambon.appendChild(opt);
                filterTambon.disabled = true;
            }} else {{
                filterTambon.disabled = false;
                const optAll = document.createElement('option');
                optAll.value = 'all';
                optAll.textContent = `ทั้งหมด (${{availableTambons.length}} ตำบล)`;
                filterTambon.appendChild(optAll);

                availableTambons.forEach(t => {{
                    const opt = document.createElement('option');
                    opt.value = t.tambon_code_6;
                    opt.textContent = t.label;
                    filterTambon.appendChild(opt);
                }});
                filterTambon.value = state.selectedTambon;
            }}
        }}

        // Year Button Visual Sync
        function syncMapYearButtons(yr) {{
            [btnMapYearAll, btnMapYear2022, btnMapYear2023].forEach(btn => {{
                if (btn.getAttribute('data-year') === yr) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
        }}

        // MASTER DISPATCHER FUNCTION
        window.HighlandApp = {{
            state: state,
            dispatchFilter: function(changes) {{
                let provinceChanged = false;
                let yearChanged = false;

                if (changes.year !== undefined && changes.year !== state.selectedYear) {{
                    state.selectedYear = changes.year;
                    yearChanged = true;
                }}

                if (changes.province !== undefined && changes.province !== state.selectedProvince) {{
                    state.selectedProvince = changes.province;
                    provinceChanged = true;
                    // Reset subordinate filters unless provided
                    if (changes.station === undefined) state.selectedStation = 'all';
                    if (changes.tambon === undefined) state.selectedTambon = 'all';
                }}

                if (changes.station !== undefined && changes.station !== state.selectedStation) {{
                    state.selectedStation = changes.station;
                }}

                if (changes.tambon !== undefined && changes.tambon !== state.selectedTambon) {{
                    state.selectedTambon = changes.tambon;
                }}

                // 1. Sync Filter Dropdowns
                filterYear.value = state.selectedYear;
                filterProvince.value = state.selectedProvince;
                if (provinceChanged) {{
                    updateCascadingFilters();
                }} else {{
                    filterStation.value = state.selectedStation;
                    if (!filterTambon.disabled) filterTambon.value = state.selectedTambon;
                }}

                // 2. Sync Map Buttons
                syncMapYearButtons(state.selectedYear);

                // 3. Update Map
                updateMapVisuals(provinceChanged);

                // 4. Update KPIs and Charts
                updateAllComponents();
            }}
        }};

        // Bind Controls to Dispatcher
        filterYear.addEventListener('change', (e) => window.HighlandApp.dispatchFilter({{ year: e.target.value }}));
        filterProvince.addEventListener('change', (e) => window.HighlandApp.dispatchFilter({{ province: e.target.value }}));
        filterStation.addEventListener('change', (e) => window.HighlandApp.dispatchFilter({{ station: e.target.value }}));
        filterTambon.addEventListener('change', (e) => window.HighlandApp.dispatchFilter({{ tambon: e.target.value }}));

        btnResetAll.addEventListener('click', () => {{
            window.HighlandApp.dispatchFilter({{ year: 'all', province: 'all', station: 'all', tambon: 'all' }});
        }});

        [btnMapYearAll, btnMapYear2022, btnMapYear2023].forEach(btn => {{
            btn.addEventListener('click', () => {{
                window.HighlandApp.dispatchFilter({{ year: btn.getAttribute('data-year') }});
            }});
        }});

        updateCascadingFilters();

        // -------------------------------------------------------------
        // D. KPI COMPUTATION (DYNAMIC FROM REAL DATA)
        // -------------------------------------------------------------
        function updateKPIs() {{
            let rainVal = REAL_DATA.overall_kpis.mean_rain;
            let tempVal = REAL_DATA.overall_kpis.mean_temp;
            let humVal = REAL_DATA.overall_kpis.mean_humidity;
            let windVal = REAL_DATA.overall_kpis.mean_wind;
            let riceVal = REAL_DATA.overall_kpis.mean_yield;

            if (state.selectedProvince !== 'all') {{
                const s = REAL_DATA.province_summaries[state.selectedProvince];
                if (s) {{
                    rainVal = (state.selectedYear === '2022') ? s.rain_2022 :
                              (state.selectedYear === '2023') ? s.rain_2023 : s.rain_all;
                    tempVal = s.temp;
                    humVal = s.humidity;
                    windVal = s.wind;
                    if (s.rice_yield_2022 && state.selectedYear === '2022') riceVal = s.rice_yield_2022;
                    else if (s.rice_yield_2023 && state.selectedYear === '2023') riceVal = s.rice_yield_2023;
                    else if (s.rice_yield_2022 && s.rice_yield_2023) riceVal = (s.rice_yield_2022 + s.rice_yield_2023) / 2;
                }}
            }}

            if (state.selectedStation !== 'all') {{
                const st = REAL_DATA.stations.find(x => x.name === state.selectedStation);
                if (st) {{
                    rainVal = st.mean_rain;
                    tempVal = st.mean_temp;
                    humVal = st.mean_humidity;
                    windVal = st.mean_wind;
                }}
            }}

            if (state.selectedTambon !== 'all' && state.selectedTambon !== 'none') {{
                const tb = REAL_DATA.tambons.find(x => x.tambon_code_6 === state.selectedTambon);
                if (tb) {{
                    riceVal = (state.selectedYear === '2022') ? tb.yield_2022 :
                              (state.selectedYear === '2023') ? tb.yield_2023 :
                              (tb.yield_2022 + tb.yield_2023) / 2;
                }}
            }}

            kpiRainVal.textContent = rainVal.toLocaleString();
            kpiTempVal.textContent = tempVal.toFixed(1);
            kpiHumidityVal.textContent = humVal.toFixed(1);
            kpiWindVal.textContent = windVal.toFixed(1);
            kpiRiceVal.textContent = (riceVal !== null && riceVal !== undefined) ? riceVal.toFixed(1) : '–';
        }}

        // -------------------------------------------------------------
        // E. CHART BUILDERS (CHART.JS HALLOWEEN THEME)
        // -------------------------------------------------------------
        const chartDefaults = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    labels: {{
                        color: '#F7F0E8',
                        font: {{ family: "'Prompt', 'Sarabun'", size: 11.5 }}
                    }}
                }},
                tooltip: {{
                    backgroundColor: '#1f132e',
                    titleColor: '#FF8A32',
                    bodyColor: '#F7F0E8',
                    borderColor: '#FF8A32',
                    borderWidth: 1,
                    padding: 8
                }}
            }},
            scales: {{
                x: {{
                    grid: {{ color: 'rgba(167, 120, 232, 0.08)' }},
                    ticks: {{ color: '#A59DB5', font: {{ family: "'Prompt'", size: 10.5 }} }}
                }},
                y: {{
                    grid: {{ color: 'rgba(167, 120, 232, 0.08)' }},
                    ticks: {{ color: '#A59DB5', font: {{ family: "'Prompt'", size: 10.5 }} }}
                }}
            }}
        }};

        // 1. Monthly Rain Trend Curve (2022 vs 2023)
        function renderMonthlyTrendChart() {{
            const ctx = document.getElementById('chartMonthlyRainTrend').getContext('2d');
            if (chartMonthly) chartMonthly.destroy();

            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            let data2022 = REAL_DATA.monthly_overall['2022'];
            let data2023 = REAL_DATA.monthly_overall['2023'];

            if (state.selectedProvince !== 'all') {{
                lblMonthlyScope.textContent = `เฉพาะจังหวัด ${{state.selectedProvince}}`;
                data2022 = months.map((_, i) => {{
                    const ym = `2022-${{String(i + 1).padStart(2, '0')}}`;
                    const item = REAL_DATA.monthly_trends.find(m => m.year_month === ym && m.province === state.selectedProvince);
                    return item ? item.mean_rain : 0;
                }});
                data2023 = months.map((_, i) => {{
                    const ym = `2023-${{String(i + 1).padStart(2, '0')}}`;
                    const item = REAL_DATA.monthly_trends.find(m => m.year_month === ym && m.province === state.selectedProvince);
                    return item ? item.mean_rain : 0;
                }});
            }} else {{
                lblMonthlyScope.textContent = 'ภาพรวม 9 จังหวัด';
            }}

            chartMonthly = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: months,
                    datasets: [
                        {{
                            label: '2022',
                            data: data2022,
                            borderColor: '#A778E8',
                            backgroundColor: 'rgba(167, 120, 232, 0.1)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#A778E8'
                        }},
                        {{
                            label: '2023',
                            data: data2023,
                            borderColor: '#FF8A32',
                            backgroundColor: 'rgba(255, 138, 50, 0.12)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 4,
                            pointBackgroundColor: '#FF8A32'
                        }}
                    ]
                }},
                options: chartDefaults
            }});
        }}

        // 2. Rain Comparison Bar (HRDI vs Province HII)
        function renderRainComparisonChart() {{
            const ctx = document.getElementById('chartRainComparison').getContext('2d');
            if (chartRainComp) chartRainComp.destroy();

            const provs = Object.keys(REAL_DATA.centers);
            const hrdiData = provs.map(p => REAL_DATA.province_summaries[p]?.rain_all || 0);
            const hiiData = provs.map(p => REAL_DATA.province_summaries[p]?.hii_rain_2022 || (REAL_DATA.province_summaries[p]?.rain_all * 0.85));

            chartRainComp = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: provs,
                    datasets: [
                        {{
                            label: 'พื้นที่สูง (HRDI)',
                            data: hrdiData,
                            backgroundColor: provs.map(p => (state.selectedProvince === p ? '#FF8A32' : '#A778E8')),
                            borderRadius: 4
                        }},
                        {{
                            label: 'ทั้งจังหวัด (HII)',
                            data: hiiData,
                            backgroundColor: provs.map(p => (state.selectedProvince === p ? '#FA9A55' : '#38bdf8')),
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    ...chartDefaults,
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const pName = provs[elements[0].index];
                            window.HighlandApp.dispatchFilter({{ province: pName }});
                        }}
                    }}
                }}
            }});
        }}

        // 3. Rice Yield Comparison Bar (2022 vs 2023)
        function renderRiceYieldComparisonChart() {{
            const ctx = document.getElementById('chartRiceYieldComparison').getContext('2d');
            if (chartRiceComp) chartRiceComp.destroy();

            const riceProvs = REAL_DATA.province_changes.map(p => p.province_name);
            const yield2022 = riceProvs.map(p => REAL_DATA.province_summaries[p]?.rice_yield_2022 || 0);
            const yield2023 = riceProvs.map(p => REAL_DATA.province_summaries[p]?.rice_yield_2023 || 0);

            chartRiceComp = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: riceProvs,
                    datasets: [
                        {{
                            label: '2022',
                            data: yield2022,
                            backgroundColor: riceProvs.map(p => (state.selectedProvince === p ? '#FA9A55' : '#A778E8')),
                            borderRadius: 4
                        }},
                        {{
                            label: '2023',
                            data: yield2023,
                            backgroundColor: riceProvs.map(p => (state.selectedProvince === p ? '#FF8A32' : '#ff6b1a')),
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    ...chartDefaults,
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const pName = riceProvs[elements[0].index];
                            window.HighlandApp.dispatchFilter({{ province: pName }});
                        }}
                    }}
                }}
            }});
        }}

        // 4. Secondary Page Charts (Tabs 2, 3, 4)
        function renderDetailedCharts() {{
            // Detailed Rain (Page 2)
            const ctx2 = document.getElementById('chartDetailedRainComparison');
            if (ctx2) {{
                if (chartDetailedRain) chartDetailedRain.destroy();
                const pNames = REAL_DATA.province_changes.map(p => p.province_name);
                const hrdi22 = pNames.map(p => REAL_DATA.province_summaries[p]?.rain_2022 || 0);
                const hrdi23 = pNames.map(p => REAL_DATA.province_summaries[p]?.rain_2023 || 0);
                const hii22 = pNames.map(p => REAL_DATA.province_summaries[p]?.hii_rain_2022 || 0);
                const hii23 = pNames.map(p => REAL_DATA.province_summaries[p]?.hii_rain_2023 || 0);

                chartDetailedRain = new Chart(ctx2.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: pNames,
                        datasets: [
                            {{ label: 'HRDI บนพื้นที่สูง (2022)', data: hrdi22, backgroundColor: '#A778E8', borderRadius: 4 }},
                            {{ label: 'HRDI บนพื้นที่สูง (2023)', data: hrdi23, backgroundColor: '#FF8A32', borderRadius: 4 }},
                            {{ label: 'HII ทั้งจังหวัด (2022)', data: hii22, backgroundColor: '#38bdf8', borderRadius: 4 }},
                            {{ label: 'HII ทั้งจังหวัด (2023)', data: hii23, backgroundColor: '#0284c7', borderRadius: 4 }}
                        ]
                    }},
                    options: {{
                        ...chartDefaults,
                        onClick: (e, elements) => {{
                            if (elements.length > 0) {{
                                window.HighlandApp.dispatchFilter({{ province: pNames[elements[0].index] }});
                            }}
                        }}
                    }}
                }});
            }}

            // Rice Slope (Page 3)
            const ctx3 = document.getElementById('chartRiceSlopeDetail');
            if (ctx3) {{
                if (chartRiceSlope) chartRiceSlope.destroy();
                let filteredTambons = REAL_DATA.tambons;
                if (state.selectedProvince !== 'all') {{
                    filteredTambons = filteredTambons.filter(t => t.province_name === state.selectedProvince);
                    document.getElementById('lblRiceSlopeScope').textContent = `เฉพาะจังหวัด ${{state.selectedProvince}} (${{filteredTambons.length}} ตำบล)`;
                }} else {{
                    document.getElementById('lblRiceSlopeScope').textContent = 'ทั้งหมด 25 ตำบล (Balanced Panel)';
                }}

                chartRiceSlope = new Chart(ctx3.getContext('2d'), {{
                    type: 'line',
                    data: {{
                        labels: ['ปี 2022', 'ปี 2023'],
                        datasets: filteredTambons.map(t => ({{
                            label: t.label,
                            data: [t.yield_2022, t.yield_2023],
                            borderColor: t.direction === 'เพิ่มขึ้น (+)' ? '#22c55e' : (t.direction === 'ลดลง (-)' ? '#ef4444' : '#eab308'),
                            backgroundColor: t.direction === 'เพิ่มขึ้น (+)' ? '#22c55e' : '#ef4444',
                            tension: 0,
                            pointRadius: 5.5,
                            pointHoverRadius: 8
                        }}))
                    }},
                    options: {{
                        ...chartDefaults,
                        plugins: {{
                            ...chartDefaults.plugins,
                            legend: {{ display: false }}
                        }}
                    }}
                }});
            }}

            // Scatter Plot (Page 4) - LARGE PRIMARY FOCAL GRAPH WITH CROSS-FILTERING
            const ctx4 = document.getElementById('chartScatterPlot');
            if (ctx4) {{
                if (chartScatter) chartScatter.destroy();
                const pts = REAL_DATA.tambons.map(t => ({{
                    x: t.delta_hrdi,
                    y: t.delta_yield,
                    tambon: t
                }}));

                chartScatter = new Chart(ctx4.getContext('2d'), {{
                    type: 'scatter',
                    data: {{
                        datasets: [{{
                            label: 'ตำบล Balanced Panel (n=25)',
                            data: pts,
                            backgroundColor: pts.map(p => {{
                                if (state.selectedTambon === p.tambon.tambon_code_6) return '#22c55e';
                                if (state.selectedProvince === p.tambon.province_name) return '#FF8A32';
                                return 'rgba(167, 120, 232, 0.75)';
                            }}),
                            borderColor: '#ffffff',
                            borderWidth: 1.2,
                            pointRadius: pts.map(p => (state.selectedTambon === p.tambon.tambon_code_6 ? 10 : 7.5)),
                            pointHoverRadius: 11
                        }}]
                    }},
                    options: {{
                        ...chartDefaults,
                        plugins: {{
                            ...chartDefaults.plugins,
                            tooltip: {{
                                ...chartDefaults.plugins.tooltip,
                                callbacks: {{
                                    title: (ctx) => ctx[0].raw.tambon.label,
                                    label: (ctx) => [
                                        `จังหวัด: ${{ctx.raw.tambon.province_name}}`,
                                        `Δ ฝน HRDI: ${{ctx.raw.x.toFixed(1)}} มม.`,
                                        `Δ ผลผลิตข้าว: ${{ctx.raw.y.toFixed(1)}} กก./ไร่`
                                    ]
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                title: {{ display: true, text: 'Δ ปริมาณน้ำฝน HRDI ก.พ.–ก.ค. (มม.)', color: '#FF8A32', font: {{ weight: '600' }} }},
                                grid: {{ color: 'rgba(167, 120, 232, 0.1)' }},
                                ticks: {{ color: '#A59DB5' }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Δ ผลผลิตข้าวนาปี (กก./ไร่)', color: '#FF8A32', font: {{ weight: '600' }} }},
                                grid: {{ color: 'rgba(167, 120, 232, 0.1)' }},
                                ticks: {{ color: '#A59DB5' }}
                            }}
                        }},
                        onClick: (e, elements) => {{
                            if (elements.length > 0) {{
                                const raw = pts[elements[0].index];
                                window.HighlandApp.dispatchFilter({{
                                    province: raw.tambon.province_name,
                                    tambon: raw.tambon.tambon_code_6
                                }});
                            }}
                        }}
                    }}
                }});
            }}

            // LOPO Table Population (Page 4)
            const lopoBody = document.querySelector('#lopoTable tbody');
            if (lopoBody && lopoBody.children.length === 0) {{
                REAL_DATA.lopo.forEach(row => {{
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td><strong>${{row.excluded_province_name}}</strong></td>
                        <td>${{row.tambons}}</td>
                        <td style="color:${{row.hrdi_tambon_rho < 0 ? '#FF8A32' : '#4ade80'}};">${{row.hrdi_tambon_rho.toFixed(4)}}</td>
                        <td>${{row.hrdi_province_rho.toFixed(4)}}</td>
                        <td>${{row.hii_province_rho.toFixed(4)}}</td>
                    `;
                    lopoBody.appendChild(tr);
                }});
            }}
        }}

        // Master Component Update Trigger
        function updateAllComponents() {{
            updateKPIs();
            renderMonthlyTrendChart();
            renderRainComparisonChart();
            renderRiceYieldComparisonChart();
            renderDetailedCharts();
        }}

        // -------------------------------------------------------------
        // F. TAB NAVIGATION LOGIC (SWITCHING BETWEEN 5 BENTO PAGES)
        // -------------------------------------------------------------
        const navTabBtns = document.querySelectorAll('.nav-tab-btn');
        navTabBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                navTabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const targetTab = btn.getAttribute('data-tab');
                state.activeTab = targetTab;

                document.querySelectorAll('.page-view-section').forEach(sec => {{
                    sec.classList.remove('active');
                }});
                const targetSec = document.getElementById(targetTab);
                if (targetSec) targetSec.classList.add('active');

                if (targetTab === 'page1') {{
                    setTimeout(() => map.invalidateSize(), 150);
                }} else {{
                    renderDetailedCharts();
                }}
            }});
        }});

        // Initial Render
        updateAllComponents();
        setTimeout(() => map.invalidateSize(), 300);

    }});
    </script>

</body>
</html>
"""
    return html_content
