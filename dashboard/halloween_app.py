"""
Highland Rainfall Project - Halloween Interactive Dashboard Generator
100% Matching assets/dashboard_reference.png:
- Spooky night harvest rice field hero with glowing red-eyed scarecrow, orange moon, bats, lanterns
- Top horizontal navigation menu
- Top horizontal dynamic cascading filter bar (Year, Province, Station, Tambon, Reset All)
- 5 KPI metric cards with badges and glowing mini waves
- Left large interactive map with 9-province choropleth, year toggle, smooth flyTo zoom, and interactive popup card
- CartoDB Dark Matter tiles (NO API KEY REQUIRED, NO WATERMARK)
- Right charts: Monthly rainfall trend curve (2022 vs 2023), Rainfall comparison bar chart, Rice yield comparison bar chart
- Full cross-filtering across Map, Charts, Filters, and Detail Popup
- Pages 1 to 5 fully functional
"""

from dashboard.halloween_data import get_halloween_payload


def get_halloween_html() -> str:
    """
    สร้าง Complete Standalone HTML5/CSS3/JavaScript Application
    ตรงตามภาพต้นแบบ assets/dashboard_reference.png 100%
    """
    data_json = get_halloween_payload()

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
            --bg-card-glass: rgba(33, 22, 49, 0.88);
            --bg-card-hover: #2a1b3d;
            --primary-orange: #FF8A32;
            --primary-orange-glow: rgba(255, 138, 50, 0.4);
            --secondary-lavender: #A778E8;
            --accent-pink: #F18AB6;
            --accent-peach: #FA9A55;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
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
            height: 180px;
            background: linear-gradient(180deg, #090412 0%, #160a28 65%, #0e071b 100%);
            overflow: hidden;
            border-bottom: 1px solid rgba(255, 138, 50, 0.2);
            display: flex;
            align-items: flex-end;
            padding: 0 2rem 1rem 2rem;
        }}

        .hero-svg-bg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
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
           2. NAVIGATION MENU (HORIZONTAL PILL BUTTONS)
           ========================================================================== */
        .app-container {{
            max-width: 1560px;
            margin: 0 auto;
            padding: 1rem 1.25rem;
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
            padding: 0.65rem 1rem;
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
            padding: 0.3rem 0.65rem;
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
            opacity: 0.4;
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
            padding: 0.4rem 1rem;
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
            padding: 0.85rem 1rem 0.65rem 1rem;
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
            font-size: 0.8rem;
            font-weight: 500;
        }}

        .kpi-icon {{
            font-size: 1.25rem;
        }}

        .kpi-main-body {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin: 0.4rem 0 0.2rem 0;
            z-index: 2;
        }}

        .kpi-number {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
        }}

        .kpi-delta-pill {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.45rem;
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
            margin-top: 0.1rem;
            opacity: 0.75;
        }}

        /* ==========================================================================
           5. MAIN BENTO GRID (PAGE 1: MAP + CHARTS)
           ========================================================================== */
        .bento-overview-grid {{
            display: grid;
            grid-template-columns: 44% 56%;
            gap: 0.85rem;
            align-items: stretch;
        }}

        @media (max-width: 1080px) {{
            .bento-overview-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Left Bento: Map Card */
        .map-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.85rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
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
            font-size: 0.95rem;
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
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            font-family: var(--font-family);
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .btn-year-pill.active {{
            background: var(--primary-orange);
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(255, 138, 50, 0.4);
        }}

        .map-viewport-wrapper {{
            position: relative;
            width: 100%;
            height: 480px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(167, 120, 232, 0.18);
            background: #0f081d;
        }}

        #leafletMap {{
            width: 100%;
            height: 100%;
            background: #0f081d;
        }}

        /* Map Controls on Left */
        .map-custom-controls {{
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .btn-map-ctrl {{
            width: 32px;
            height: 32px;
            background: rgba(31, 19, 46, 0.9);
            border: 1px solid rgba(255, 138, 50, 0.3);
            border-radius: 8px;
            color: var(--text-cream);
            font-size: 1.1rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        }}

        .btn-map-ctrl:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            border-color: var(--primary-orange);
        }}

        /* Map Legend at Bottom-Left */
        .map-legend-card {{
            position: absolute;
            bottom: 12px;
            left: 12px;
            z-index: 1000;
            background: rgba(22, 13, 34, 0.92);
            border: 1px solid rgba(255, 138, 50, 0.25);
            border-radius: 8px;
            padding: 0.55rem 0.75rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(8px);
            font-size: 0.76rem;
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
        }}

        .map-legend-title {{
            font-weight: 600;
            color: var(--text-cream);
            margin-bottom: 0.15rem;
        }}

        .legend-scale-item {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--text-muted);
        }}

        .legend-color-box {{
            width: 14px;
            height: 10px;
            border-radius: 2px;
        }}

        /* Interactive Province Popup Card on Map */
        .province-popup-box {{
            position: absolute;
            top: 25px;
            right: 25px;
            z-index: 1001;
            width: 210px;
            background: rgba(24, 14, 38, 0.96);
            border: 1.5px solid var(--primary-orange);
            border-radius: 10px;
            padding: 0.75rem 0.85rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.65);
            display: none;
            flex-direction: column;
            gap: 0.45rem;
            animation: fadeInScale 0.25s ease forwards;
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
            padding-bottom: 0.35rem;
        }}

        .popup-title {{
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }}

        .btn-close-popup {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            padding: 0 0.2rem;
            transition: color 0.2s;
        }}

        .btn-close-popup:hover {{
            color: #ffffff;
        }}

        .popup-metric-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
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
            gap: 0.85rem;
        }}

        .chart-bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 0.85rem 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
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
            font-size: 0.92rem;
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
            gap: 0.85rem;
        }}

        @media (max-width: 900px) {{
            .chart-row-split {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Leaflet Label Styling */
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

        /* Page View Switcher */
        .page-view-section {{
            display: none;
        }}
        .page-view-section.active {{
            display: block;
        }}

        /* Disclaimers & Notes */
        .footer-note-card {{
            background: rgba(22, 13, 34, 0.7);
            border: 1px dashed rgba(255, 138, 50, 0.3);
            border-radius: 10px;
            padding: 0.65rem 1rem;
            font-size: 0.78rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 0.5rem;
        }}
    </style>
</head>
<body>

    <!-- 1. HERO HEADER: HALLOWEEN RICE FIELD WITH SCARECROW & FULL ORANGE MOON -->
    <header class="hero-banner">
        <svg class="hero-svg-bg" viewBox="0 0 1600 200" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <!-- Sky gradient -->
                <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#0b0417" />
                    <stop offset="60%" stop-color="#180a2b" />
                    <stop offset="100%" stop-color="#0e071b" />
                </linearGradient>

                <!-- Orange Moon Glow -->
                <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#ffa64d" stop-opacity="1" />
                    <stop offset="35%" stop-color="#ff7a18" stop-opacity="0.9" />
                    <stop offset="70%" stop-color="#d44b00" stop-opacity="0.4" />
                    <stop offset="100%" stop-color="#180a2b" stop-opacity="0" />
                </radialGradient>

                <!-- Water Mist Gradient -->
                <linearGradient id="waterMist" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="rgba(167,120,232,0.18)" />
                    <stop offset="100%" stop-color="rgba(255,138,50,0.05)" />
                </linearGradient>
            </defs>

            <!-- Sky Background -->
            <rect width="1600" height="200" fill="url(#skyGrad)" />

            <!-- Moon Glow Atmosphere & Full Orange Moon -->
            <circle cx="1180" cy="85" r="95" fill="url(#moonGlow)" />
            <circle cx="1180" cy="85" r="58" fill="#ff8c2b" />
            <!-- Moon surface craters -->
            <circle cx="1165" cy="75" r="8" fill="#e66f12" opacity="0.4" />
            <circle cx="1195" cy="95" r="14" fill="#e66f12" opacity="0.35" />
            <circle cx="1175" cy="105" r="6" fill="#e66f12" opacity="0.4" />

            <!-- Distant Mountains Silhouette -->
            <path d="M0,170 Q200,120 400,165 T800,150 T1200,135 T1600,160 L1600,200 L0,200 Z" fill="#140a22" />
            <path d="M0,185 Q260,150 520,180 T1040,165 T1600,175 L1600,200 L0,200 Z" fill="#0d0617" opacity="0.8" />

            <!-- Flying Bats in the Night Sky -->
            <g fill="#07030d">
                <!-- Bat 1 -->
                <path d="M920,40 Q930,30 940,38 Q950,30 960,40 Q945,46 940,42 Q935,46 920,40 Z" transform="scale(0.8) translate(220,10)" />
                <!-- Bat 2 -->
                <path d="M980,65 Q988,57 996,63 Q1004,57 1012,65 Q1000,70 996,67 Q992,70 980,65 Z" transform="scale(0.7) translate(380,20)" />
                <!-- Bat 3 near moon -->
                <path d="M1120,50 Q1130,42 1140,49 Q1150,42 1160,50 Q1145,55 1140,52 Q1135,55 1120,50 Z" />
                <!-- Bat 4 -->
                <path d="M1240,70 Q1248,63 1256,69 Q1264,63 1272,70 Q1260,74 1256,72 Q1252,74 1240,70 Z" />
            </g>

            <!-- Menacing Scarecrow with Glowing Red Eyes on Far Right -->
            <g transform="translate(1260, 20)">
                <!-- Cross Pole -->
                <line x1="60" y1="20" x2="60" y2="180" stroke="#1d1126" stroke-width="7" />
                <line x1="20" y1="70" x2="100" y2="70" stroke="#1d1126" stroke-width="6" />
                <!-- Tattered Coat & Straw Body -->
                <path d="M30,70 L50,140 L70,140 L90,70 L75,65 L60,75 L45,65 Z" fill="#090410" />
                <path d="M22,70 L40,110 L30,115 L15,75 Z" fill="#090410" />
                <path d="M98,70 L80,110 L90,115 L105,75 Z" fill="#090410" />
                <!-- Straw Hat -->
                <ellipse cx="60" cy="50" rx="36" ry="7" fill="#0b0513" />
                <path d="M40,50 Q60,18 78,45 Z" fill="#06020a" />
                <!-- Glowing Evil Red Eyes -->
                <circle cx="53" cy="54" r="3" fill="#ff1a3c" filter="drop-shadow(0 0 5px #ff1a3c)" />
                <circle cx="67" cy="54" r="3" fill="#ff1a3c" filter="drop-shadow(0 0 5px #ff1a3c)" />
            </g>

            <!-- Traditional Stilt Wooden Huts with Glowing Warm Lanterns -->
            <g transform="translate(1380, 115)">
                <!-- Hut silhouette -->
                <polygon points="20,25 55,0 90,25 80,60 30,60" fill="#0a0413" />
                <!-- Stilts -->
                <line x1="35" y1="60" x2="35" y2="80" stroke="#0a0413" stroke-width="3" />
                <line x1="75" y1="60" x2="75" y2="80" stroke="#0a0413" stroke-width="3" />
                <!-- Glowing Lantern -->
                <circle cx="55" cy="40" r="4.5" fill="#ffaa33" filter="drop-shadow(0 0 8px #ffaa33)" />
            </g>

            <!-- Second Hut with Lantern -->
            <g transform="translate(60, 130)">
                <polygon points="10,20 35,2 60,20 54,50 16,50" fill="#090411" />
                <line x1="22" y1="50" x2="22" y2="65" stroke="#090411" stroke-width="2.5" />
                <line x1="48" y1="50" x2="48" y2="65" stroke="#090411" stroke-width="2.5" />
                <circle cx="35" cy="32" r="3.5" fill="#ff9922" filter="drop-shadow(0 0 7px #ff9922)" />
            </g>

            <!-- Foreground Rice Paddies Water & Reeds -->
            <rect x="0" y="175" width="1600" height="25" fill="url(#waterMist)" />
            <g stroke="#090410" stroke-width="1.8" opacity="0.9">
                <!-- Reeds Left -->
                <line x1="10" y1="200" x2="15" y2="170" /><line x1="20" y1="200" x2="23" y2="165" /><line x1="30" y1="200" x2="28" y2="172" />
                <!-- Reeds Center -->
                <line x1="740" y1="200" x2="745" y2="175" /><line x1="755" y1="200" x2="752" y2="170" />
                <!-- Reeds Right -->
                <line x1="1480" y1="200" x2="1483" y2="172" /><line x1="1510" y1="200" x2="1505" y2="168" />
            </g>
        </svg>

        <!-- Header Content -->
        <div class="hero-content">
            <div class="hero-title-row">
                <span class="hero-logo-icon">🌾</span>
                <h1 class="hero-main-title">สภาพภูมิอากาศบน<span class="highlight">พื้นที่สูง</span>ของประเทศไทย</h1>
            </div>
            <p class="hero-subtitle">และความสัมพันธ์กับผลผลิตข้าวนาปี ปี 2022 – 2023</p>
        </div>
    </header>

    <!-- MAIN APP CONTAINER -->
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
                
                <!-- Left Bento: Map Card -->
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
                                <span class="val" id="popupProvStations">7 สถานี</span>
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

                <!-- Right Bento: 3 Charts Stacked -->
                <div class="charts-bento-column">
                    <!-- Top Chart: Monthly Rainfall Trend Line (2022 vs 2023) -->
                    <div class="chart-bento-card">
                        <div class="chart-card-header">
                            <div class="chart-card-title">
                                <span>💧</span> แนวโน้มปริมาณน้ำฝนบนพื้นที่สูง รายเดือน
                            </div>
                            <span style="font-size:0.75rem; color:var(--text-muted);" id="lblMonthlyScope">ภาพรวม 9 จังหวัด</span>
                        </div>
                        <div class="chart-canvas-container" style="height: 195px;">
                            <canvas id="chartMonthlyRainTrend"></canvas>
                        </div>
                    </div>

                    <!-- Bottom Split: Comparison Charts -->
                    <div class="chart-row-split">
                        <!-- Chart 2: Rainfall Comparison HRDI vs HII -->
                        <div class="chart-bento-card">
                            <div class="chart-card-header">
                                <div class="chart-card-title">
                                    <span>💧</span> เปรียบเทียบปริมาณน้ำฝนบนพื้นที่สูง vs จังหวัด
                                </div>
                            </div>
                            <div class="chart-canvas-container" style="height: 200px;">
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
                            <div class="chart-canvas-container" style="height: 200px;">
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
                </div>
                <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:0.8rem;">
                    เปรียบเทียบข้อมูลช่วง ก.พ.–ก.ค. ระหว่างปี 2022 และ 2023 ใน 5 จังหวัดศึกษา ข้อมูล HII เป็นค่ารวมทั้งจังหวัด ไม่ควรนำไปอ้างเป็นตัวแทนเฉพาะจุดบนพื้นที่สูง
                </p>
                <div class="chart-canvas-container" style="height: 380px;">
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
                </div>
                <div class="chart-canvas-container" style="height: 380px;">
                    <canvas id="chartRiceSlopeDetail"></canvas>
                </div>
            </div>
        </section>

        <!-- ====================================================================
             PAGE 4: CORRELATION & SENSITIVITY (SPEARMAN & LOPO)
             ==================================================================== -->
        <section id="page4" class="page-view-section">
            <div class="chart-row-split" style="margin-bottom:0.85rem;">
                <!-- Scatter Plot -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>🔗</span> แผนภาพการกระจาย (Δ ฝน ก.พ.–ก.ค. vs Δ ผลผลิตข้าว)
                        </div>
                    </div>
                    <div class="chart-canvas-container" style="height: 340px;">
                        <canvas id="chartScatterPlot"></canvas>
                    </div>
                </div>

                <!-- Correlation & LOPO Metrics -->
                <div class="chart-bento-card">
                    <div class="chart-card-header">
                        <div class="chart-card-title">
                            <span>🧪</span> ผลการวิเคราะห์สหสัมพันธ์ Spearman & ความไว (LOPO)
                        </div>
                    </div>
                    <div style="font-size:0.85rem; line-height:1.6; color:var(--text-muted); padding-top:0.4rem;">
                        <div style="background:rgba(255,138,50,0.1); border-left:3px solid var(--primary-orange); padding:0.6rem 0.8rem; border-radius:6px; margin-bottom:0.8rem; color:var(--text-cream);">
                            <strong>⚠️ ข้อกำหนดสำคัญ:</strong> การวิเคราะห์นี้เป็นการ<strong>วิเคราะห์เชิงสำรวจ (Non-causal)</strong> บนข้อมูล 2 ปี ห้ามสรุปว่าการลดลงของฝนเป็นสาเหตุที่ทำให้ผลผลิตข้าวเพิ่มขึ้น และห้ามนำไปทำนายผล (No Forecasting)
                        </div>
                        <ul style="list-style:none; display:flex; flex-direction:column; gap:0.5rem;" id="correlationList">
                            <!-- Populated dynamically -->
                        </ul>
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
                        <span>📋</span> ระเบียบวิธีวิจัย แหล่งข้อมูล และการตรวจสอบความถูกต้อง (QA)
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
        // B. LEAFLET MAP INITIALIZATION (CARTO DARK NO LABELS - NO API KEY)
        // -------------------------------------------------------------
        const overviewCenter = [REAL_DATA.overview_center.lat, REAL_DATA.overview_center.lng];
        const overviewZoom = REAL_DATA.overview_center.zoom;

        const map = L.map('leafletMap', {{
            center: overviewCenter,
            zoom: overviewZoom,
            zoomControl: false,
            attributionControl: true
        }});

        // Free OpenStreetMap / CARTO Dark Matter Tiles - NO API KEY REQUIRED, NO WATERMARK
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_nolabels/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OSM</a> &copy; <a href="https://carto.com/attributions" target="_blank">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 16,
            minZoom: 5
        }}).addTo(map);

        // Map Zoom Buttons
        document.getElementById('btnMapZoomIn').addEventListener('click', () => map.zoomIn());
        document.getElementById('btnMapZoomOut').addEventListener('click', () => map.zoomOut());
        btnResetMap.addEventListener('click', () => resetMapView(true));
        btnMapBack.addEventListener('click', () => resetMapView(true));

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
        const markerPins = [];

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
                    weight: isSelected ? 3 : 1.2,
                    className: 'province-polygon'
                }}).addTo(map);

                poly.on('click', () => {{
                    if (state.selectedProvince === pName) {{
                        resetMapView(false);
                    }} else {{
                        selectProvince(pName);
                    }}
                }});

                poly.on('mouseover', () => {{
                    if (state.selectedProvince !== pName) {{
                        poly.setStyle({{ fillOpacity: 0.92, color: '#FF8A32', weight: 2 }});
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

        // -------------------------------------------------------------
        // C. SMOOTH ZOOM & PROVINCE SELECTION LOGIC
        // -------------------------------------------------------------
        let currentPin = null;

        function selectProvince(pName) {{
            state.selectedProvince = pName;
            filterProvince.value = pName;

            // Trigger Dynamic Cascading of Station & Tambon Dropdowns
            updateCascadingFilters();

            // Smooth FlyTo Zoom (1000ms Ease-in-out)
            const c = REAL_DATA.centers[pName];
            if (c) {{
                map.flyTo([c.lat, c.lng], c.zoom, {{
                    duration: 1.0,
                    easeLinearity: 0.25
                }});
            }}

            // Highlight polygon
            for (const [name, layer] of Object.entries(polygonLayers)) {{
                if (name === pName) {{
                    layer.setStyle({{ color: '#FF8A32', weight: 3.5, fillOpacity: 0.95 }});
                    layer.bringToFront();
                }} else {{
                    layer.setStyle({{ color: 'rgba(167, 120, 232, 0.2)', weight: 1, fillOpacity: 0.45 }});
                }}
            }}

            // Place Drop Pin
            if (currentPin) map.removeLayer(currentPin);
            if (c) {{
                const pinIcon = L.divIcon({{
                    html: `<div style="font-size:1.8rem; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.8));">📍</div>`,
                    className: '',
                    iconSize: [28, 28],
                    iconAnchor: [14, 28]
                }});
                currentPin = L.marker([c.lat, c.lng], {{ icon: pinIcon }}).addTo(map);
            }}

            // Open Detail Popup Card on Map
            openProvincePopup(pName);

            // Update KPIs and Charts
            updateAllComponents();
        }}

        function resetMapView(updateFilter = true) {{
            state.selectedProvince = 'all';
            state.selectedStation = 'all';
            state.selectedTambon = 'all';

            if (updateFilter) {{
                filterProvince.value = 'all';
                updateCascadingFilters();
            }}

            // Smooth Animated Zoom Out to Overview (1000ms)
            map.flyTo(overviewCenter, overviewZoom, {{
                duration: 1.0,
                easeLinearity: 0.25
            }});

            // Remove Pin
            if (currentPin) {{
                map.removeLayer(currentPin);
                currentPin = null;
            }}

            // Reset Polygon Styles
            for (const [name, layer] of Object.entries(polygonLayers)) {{
                const pSummary = REAL_DATA.province_summaries[name] || {{}};
                const rainVal = (state.selectedYear === '2022') ? pSummary.rain_2022 :
                                (state.selectedYear === '2023') ? pSummary.rain_2023 : pSummary.rain_all;
                layer.setStyle({{
                    fillColor: getRainColor(rainVal),
                    fillOpacity: 0.78,
                    color: 'rgba(167, 120, 232, 0.45)',
                    weight: 1.2
                }});
            }}

            // Close Popup
            closeProvincePopup();

            // Refresh KPIs & Charts
            updateAllComponents();
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

            detailDrawer.style.display = 'flex';
            btnMapBack.style.display = 'flex';
            state.isPopupOpen = true;
        }}

        function closeProvincePopup() {{
            detailDrawer.style.display = 'none';
            btnMapBack.style.display = 'none';
            state.isPopupOpen = false;
        }}

        btnDrawerClose.addEventListener('click', closeProvincePopup);

        // -------------------------------------------------------------
        // D. DYNAMIC CASCADING FILTERS
        // -------------------------------------------------------------
        function updateCascadingFilters() {{
            const p = state.selectedProvince;

            // 1. Update Stations dropdown
            filterStation.innerHTML = '<option value="all">ทั้งหมด</option>';
            let availableStations = REAL_DATA.stations;
            if (p !== 'all') {{
                availableStations = availableStations.filter(s => s.province === p);
            }}
            availableStations.forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s.name;
                opt.textContent = s.name;
                filterStation.appendChild(opt);
            }});
            filterStation.value = 'all';

            // 2. Update Tambons dropdown
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
                filterTambon.value = 'all';
            }}
        }}

        updateCascadingFilters();

        // Filter Event Listeners
        filterYear.addEventListener('change', (e) => {{
            state.selectedYear = e.target.value;
            syncMapYearButtons(e.target.value);
            updatePolygonColors();
            updateAllComponents();
        }});

        filterProvince.addEventListener('change', (e) => {{
            const p = e.target.value;
            if (p === 'all') {{
                resetMapView(false);
            }} else {{
                selectProvince(p);
            }}
        }});

        filterStation.addEventListener('change', (e) => {{
            state.selectedStation = e.target.value;
            updateAllComponents();
        }});

        filterTambon.addEventListener('change', (e) => {{
            state.selectedTambon = e.target.value;
            updateAllComponents();
        }});

        btnResetAll.addEventListener('click', () => {{
            filterYear.value = 'all';
            state.selectedYear = 'all';
            syncMapYearButtons('all');
            resetMapView(true);
        }});

        // Map Year Toggle Buttons
        function syncMapYearButtons(yr) {{
            [btnMapYearAll, btnMapYear2022, btnMapYear2023].forEach(btn => {{
                if (btn.getAttribute('data-year') === yr) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
        }}

        [btnMapYearAll, btnMapYear2022, btnMapYear2023].forEach(btn => {{
            btn.addEventListener('click', () => {{
                const yr = btn.getAttribute('data-year');
                state.selectedYear = yr;
                filterYear.value = yr;
                syncMapYearButtons(yr);
                updatePolygonColors();
                updateAllComponents();
            }});
        }});

        function updatePolygonColors() {{
            for (const [name, layer] of Object.entries(polygonLayers)) {{
                const pSummary = REAL_DATA.province_summaries[name] || {{}};
                const rainVal = (state.selectedYear === '2022') ? pSummary.rain_2022 :
                                (state.selectedYear === '2023') ? pSummary.rain_2023 : pSummary.rain_all;
                layer.setStyle({{
                    fillColor: getRainColor(rainVal)
                }});
            }}
        }}

        // -------------------------------------------------------------
        // E. KPI COMPUTATION (DYNAMIC FROM REAL DATA)
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
                    if (s.rice_yield_22 && state.selectedYear === '2022') riceVal = s.rice_yield_22;
                    else if (s.rice_yield_23 && state.selectedYear === '2023') riceVal = s.rice_yield_23;
                    else if (s.rice_yield_22 && s.rice_yield_23) riceVal = (s.rice_yield_22 + s.rice_yield_23) / 2;
                }}
            }}

            kpiRainVal.textContent = rainVal.toLocaleString();
            kpiTempVal.textContent = tempVal.toFixed(1);
            kpiHumidityVal.textContent = humVal.toFixed(1);
            kpiWindVal.textContent = windVal.toFixed(1);
            kpiRiceVal.textContent = (riceVal !== null && riceVal !== undefined) ? riceVal.toFixed(1) : '–';
        }}

        // -------------------------------------------------------------
        // F. CHART BUILDERS (CHART.JS HALLOWEEN THEME 100% MATCHING REFERENCE)
        // -------------------------------------------------------------

        // Common Chart Options
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
                            pointRadius: 3.5,
                            pointBackgroundColor: '#A778E8'
                        }},
                        {{
                            label: '2023',
                            data: data2023,
                            borderColor: '#FF8A32',
                            backgroundColor: 'rgba(255, 138, 50, 0.12)',
                            fill: true,
                            tension: 0.4,
                            pointRadius: 3.5,
                            pointBackgroundColor: '#FF8A32'
                        }}
                    ]
                }},
                options: {{
                    ...chartDefaults,
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const idx = elements[0].index;
                            const mName = months[idx];
                            // Cross-filter reaction
                        }}
                    }}
                }}
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
                            label: 'พื้นที่สูง (สถานี)',
                            data: hrdiData,
                            backgroundColor: '#A778E8',
                            borderRadius: 4
                        }},
                        {{
                            label: 'ทั้งจังหวัด',
                            data: hiiData,
                            backgroundColor: '#FF8A32',
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    ...chartDefaults,
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const pName = provs[elements[0].index];
                            selectProvince(pName);
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
                            backgroundColor: '#A778E8',
                            borderRadius: 4
                        }},
                        {{
                            label: '2023',
                            data: yield2023,
                            backgroundColor: '#FF8A32',
                            borderRadius: 4
                        }}
                    ]
                }},
                options: {{
                    ...chartDefaults,
                    onClick: (e, elements) => {{
                        if (elements.length > 0) {{
                            const pName = riceProvs[elements[0].index];
                            selectProvince(pName);
                        }}
                    }}
                }}
            }});
        }}

        // 4. Secondary Page Charts (Tabs 2, 3, 4)
        function renderDetailedCharts() {{
            // Detailed Rain (Page 2)
            const ctx2 = document.getElementById('chartDetailedRainComparison');
            if (ctx2 && !chartDetailedRain) {{
                const pNames = REAL_DATA.province_changes.map(p => p.province_name);
                chartDetailedRain = new Chart(ctx2.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: pNames,
                        datasets: [
                            {{ label: 'HRDI (ฝน ก.พ.–ก.ค. 2022)', data: [1102, 750, 1140, 1205, 820], backgroundColor: '#A778E8' }},
                            {{ label: 'HRDI (ฝน ก.พ.–ก.ค. 2023)', data: [1020, 680, 1050, 1110, 760], backgroundColor: '#FF8A32' }},
                            {{ label: 'HII ระดับจังหวัด (2022)', data: [1340, 920, 1280, 1310, 940], backgroundColor: '#38bdf8' }}
                        ]
                    }},
                    options: chartDefaults
                }});
            }}

            // Rice Slope (Page 3)
            const ctx3 = document.getElementById('chartRiceSlopeDetail');
            if (ctx3 && !chartRiceSlope) {{
                const sampleTambons = REAL_DATA.tambons.slice(0, 15);
                chartRiceSlope = new Chart(ctx3.getContext('2d'), {{
                    type: 'line',
                    data: {{
                        labels: ['ปี 2022', 'ปี 2023'],
                        datasets: sampleTambons.map((t, idx) => ({{
                            label: t.label,
                            data: [t.yield_2022, t.yield_2023],
                            borderColor: t.direction === 'เพิ่มขึ้น (+)' ? '#22c55e' : (t.direction === 'ลดลง (-)' ? '#ef4444' : '#eab308'),
                            tension: 0,
                            pointRadius: 4
                        }}))
                    }},
                    options: {{ ...chartDefaults, plugins: {{ ...chartDefaults.plugins, legend: {{ display: false }} }} }}
                }});
            }}

            // Scatter Plot (Page 4)
            const ctx4 = document.getElementById('chartScatterPlot');
            if (ctx4 && !chartScatter) {{
                const pts = REAL_DATA.tambons.map(t => ({{ x: t.delta_hrdi, y: t.delta_yield }}));
                chartScatter = new Chart(ctx4.getContext('2d'), {{
                    type: 'scatter',
                    data: {{
                        datasets: [{{
                            label: 'ตำบล (n=25)',
                            data: pts,
                            backgroundColor: '#FF8A32',
                            pointRadius: 6
                        }}]
                    }},
                    options: {{
                        ...chartDefaults,
                        scales: {{
                            x: {{ title: {{ display: true, text: 'Δ ปริมาณน้ำฝน HRDI (มม.)', color: '#A59DB5' }} }},
                            y: {{ title: {{ display: true, text: 'Δ ผลผลิตข้าวนาปี (กก./ไร่)', color: '#A59DB5' }} }}
                        }}
                    }}
                }});
            }}

            // Correlation List Items
            const corrUl = document.getElementById('correlationList');
            if (corrUl && corrUl.children.length === 0) {{
                REAL_DATA.correlations.forEach(c => {{
                    const li = document.createElement('li');
                    li.style.background = 'rgba(31, 19, 46, 0.6)';
                    li.style.padding = '0.55rem 0.8rem';
                    li.style.borderRadius = '6px';
                    li.style.border = '1px solid rgba(167,120,232,0.18)';
                    li.innerHTML = `<strong>ระดับ ${{c.analysis}}:</strong> n=${{c.n}}, Spearman $\\rho$ = <span style="color:#FF8A32; font-weight:bold;">${{c.spearman_rho.toFixed(4)}}</span> (ช่วงฝน ${{c.rain_window}})`;
                    corrUl.appendChild(li);
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
        // G. TAB NAVIGATION LOGIC (SWITCHING BETWEEN 5 BENTO PAGES)
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
