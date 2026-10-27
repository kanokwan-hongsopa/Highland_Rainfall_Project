"""
Highland Rainfall Project - Halloween Interactive Dashboard Generator
สร้าง Complete Standalone Interactive Single-Page Application (HTML5/CSS3/JS + Leaflet + Chart.js)
"""

from dashboard.halloween_data import get_halloween_payload


def get_halloween_html() -> str:
    """
    สร้างเอกสาร HTML แบบสมบูรณ์ที่มีระบบ Client-Side Centralized State,
    Smooth Camera Fly-To Zoom (800-1200ms), Real-time Cross-Filtering,
    Bento Grid Layout, Detail Drawer และ Halloween Theme
    """
    data_json = get_halloween_payload()

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Highland Rainfall & Rice Analytics — Halloween Edition 🎃</title>
    <!-- Fonts: Prompt & Sarabun -->
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
            --bg-dark: #130D22;
            --bg-card: #211631;
            --bg-card-hover: #291b3e;
            --primary-orange: #FF8A32;
            --primary-orange-glow: rgba(255, 138, 50, 0.35);
            --secondary-lavender: #A778E8;
            --accent-pink: #F18AB6;
            --accent-cyan: #38bdf8;
            --text-cream: #F7F0E8;
            --text-muted: #A59DB5;
            --border-card: rgba(255, 138, 50, 0.22);
            --border-card-active: #FF8A32;
            --radius-card: 16px;
            --font-main: 'Prompt', 'Sarabun', sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-dark);
            color: var(--text-cream);
            font-family: var(--font-main);
            font-size: 14px;
            line-height: 1.5;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(167, 120, 232, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 70%, rgba(255, 138, 50, 0.07) 0%, transparent 40%);
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #181028;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #392854;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--primary-orange);
        }}

        /* Container */
        .app-container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 1rem 1.5rem 3rem 1.5rem;
        }}

        /* Hero Header */
        .hero-header {{
            position: relative;
            background: linear-gradient(180deg, #180F2A 0%, #211631 100%);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.5rem 2rem;
            margin-bottom: 1.25rem;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        }}

        .hero-svg-bg {{
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            width: 55%;
            pointer-events: none;
            opacity: 0.95;
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            max-width: 65%;
        }}

        .hero-badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.6rem;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            background: rgba(255, 138, 50, 0.15);
            border: 1px solid rgba(255, 138, 50, 0.4);
            color: var(--primary-orange);
            font-size: 0.76rem;
            font-weight: 600;
            padding: 0.2rem 0.65rem;
            border-radius: 9999px;
            letter-spacing: 0.02em;
        }}

        .hero-badge-purple {{
            background: rgba(167, 120, 232, 0.15);
            border-color: rgba(167, 120, 232, 0.4);
            color: var(--secondary-lavender);
        }}

        .hero-title {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.3rem;
            letter-spacing: -0.01em;
            text-shadow: 0 2px 10px rgba(255, 138, 50, 0.25);
        }}

        .hero-subtitle {{
            font-size: 0.88rem;
            color: var(--text-muted);
            line-height: 1.45;
        }}

        /* Navigation Bar */
        .nav-tabs {{
            display: flex;
            gap: 0.6rem;
            background: #1a112c;
            padding: 0.4rem;
            border-radius: 14px;
            border: 1px solid var(--border-card);
            margin-bottom: 1.25rem;
            overflow-x: auto;
        }}

        .nav-tab-btn {{
            flex: 1;
            min-width: 170px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            font-family: var(--font-main);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s ease;
            white-space: nowrap;
        }}

        .nav-tab-btn:hover {{
            color: #ffffff;
            background: rgba(255, 138, 50, 0.1);
        }}

        .nav-tab-btn.active {{
            background: linear-gradient(135deg, var(--primary-orange) 0%, #e06c19 100%);
            color: #ffffff;
            font-weight: 600;
            box-shadow: 0 4px 16px var(--primary-orange-glow);
        }}

        /* Main Layout Grid (Sidebar + Content) */
        .layout-wrapper {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1.25rem;
            align-items: start;
        }}

        @media (max-width: 1024px) {{
            .layout-wrapper {{
                grid-template-columns: 1fr;
            }}
            .hero-content {{
                max-width: 100%;
            }}
            .hero-svg-bg {{
                opacity: 0.25;
            }}
        }}

        /* Sidebar */
        .sidebar-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.25rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            position: sticky;
            top: 1rem;
        }}

        .sidebar-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid rgba(255, 138, 50, 0.15);
        }}

        .filter-group {{
            margin-bottom: 1rem;
        }}

        .filter-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.35rem;
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .filter-select, .filter-input {{
            width: 100%;
            background: #170E26;
            border: 1px solid rgba(255, 138, 50, 0.3);
            border-radius: 8px;
            color: #ffffff;
            padding: 0.5rem 0.75rem;
            font-family: var(--font-main);
            font-size: 0.82rem;
            outline: none;
            transition: all 0.2s ease;
        }}

        .filter-select:focus, .filter-input:focus {{
            border-color: var(--primary-orange);
            box-shadow: 0 0 10px var(--primary-orange-glow);
        }}

        .btn-action {{
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            padding: 0.55rem;
            border-radius: 8px;
            font-family: var(--font-main);
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 0.6rem;
            border: none;
        }}

        .btn-reset-all {{
            background: rgba(255, 138, 50, 0.15);
            border: 1px solid var(--primary-orange);
            color: var(--primary-orange);
        }}
        .btn-reset-all:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            box-shadow: 0 0 15px var(--primary-orange-glow);
        }}

        .btn-reset-map {{
            background: rgba(167, 120, 232, 0.15);
            border: 1px solid var(--secondary-lavender);
            color: var(--secondary-lavender);
        }}
        .btn-reset-map:hover {{
            background: var(--secondary-lavender);
            color: #ffffff;
            box-shadow: 0 0 15px rgba(167, 120, 232, 0.4);
        }}

        .sidebar-active-status {{
            margin-top: 1.25rem;
            padding: 0.85rem;
            background: #170E26;
            border-radius: 10px;
            border-left: 3px solid var(--primary-orange);
            font-size: 0.76rem;
            color: var(--text-muted);
            line-height: 1.5;
        }}

        .active-filter-badge {{
            display: inline-block;
            background: rgba(255, 138, 50, 0.25);
            color: #ffb37a;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
            margin-top: 0.25rem;
        }}

        /* Content Area & Bento Grid */
        .content-area {{
            min-width: 0;
        }}

        .page-view {{
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }}

        .page-view.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* KPI Bento Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.15rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease;
            cursor: pointer;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--primary-orange);
            box-shadow: 0 6px 20px var(--primary-orange-glow);
        }}

        .kpi-card::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 40px;
            height: 40px;
            background: radial-gradient(circle, rgba(255, 138, 50, 0.15) 0%, transparent 70%);
            border-radius: 0 var(--radius-card) 0 40px;
        }}

        .kpi-icon-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }}

        .kpi-title {{
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .kpi-icon {{
            font-size: 1.25rem;
        }}

        .kpi-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }}

        .kpi-subtext {{
            font-size: 0.75rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .kpi-delta {{
            font-weight: 600;
        }}

        .delta-orange {{ color: var(--primary-orange); }}
        .delta-purple {{ color: var(--secondary-lavender); }}
        .delta-pink {{ color: var(--accent-pink); }}
        .delta-cyan {{ color: var(--accent-cyan); }}

        /* Standard Bento Card */
        .bento-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-card);
            padding: 1.25rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.25rem;
            transition: border-color 0.25s ease;
            position: relative;
        }}

        .bento-card:hover {{
            border-color: rgba(255, 138, 50, 0.4);
        }}

        .card-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid rgba(255, 138, 50, 0.12);
        }}

        .card-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }}

        .card-subtitle {{
            font-size: 0.76rem;
            color: var(--text-muted);
        }}

        /* Map Container */
        #map-container {{
            width: 100%;
            height: 480px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 138, 50, 0.3);
            position: relative;
        }}

        .map-breadcrumb {{
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(19, 13, 34, 0.9);
            border: 1px solid var(--primary-orange);
            border-radius: 8px;
            padding: 0.4rem 0.8rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.78rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
        }}

        .btn-map-back {{
            background: var(--primary-orange);
            color: #ffffff;
            border: none;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            font-size: 0.74rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: none;
        }}

        .btn-map-back:hover {{
            background: #ff9d54;
        }}

        /* Two-Column Grid */
        .two-col-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.25rem;
        }}

        @media (max-width: 900px) {{
            .two-col-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Charts Canvas Container */
        .chart-box {{
            position: relative;
            width: 100%;
            height: 320px;
        }}

        /* Notice & Disclaimer Callout */
        .halloween-notice {{
            background: rgba(255, 138, 50, 0.08);
            border-left: 4px solid var(--primary-orange);
            border-radius: 8px;
            padding: 0.85rem 1.15rem;
            margin-bottom: 1.25rem;
            font-size: 0.82rem;
            color: #f7e6d7;
            line-height: 1.5;
        }}

        .halloween-notice-purple {{
            background: rgba(167, 120, 232, 0.08);
            border-left-color: var(--secondary-lavender);
            color: #f0e6fc;
        }}

        /* Table Styling */
        .custom-table-wrapper {{
            overflow-x: auto;
            border-radius: 10px;
            border: 1px solid rgba(255, 138, 50, 0.2);
        }}

        .custom-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            text-align: left;
        }}

        .custom-table th {{
            background: #170E26;
            color: var(--primary-orange);
            padding: 0.75rem 0.9rem;
            font-weight: 600;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
            white-space: nowrap;
        }}

        .custom-table td {{
            padding: 0.7rem 0.9rem;
            border-bottom: 1px solid rgba(255, 138, 50, 0.1);
            color: var(--text-cream);
            white-space: nowrap;
        }}

        .custom-table tr:hover td {{
            background: rgba(255, 138, 50, 0.08);
            cursor: pointer;
        }}

        /* Detail Drawer / Side Modal */
        .detail-drawer {{
            position: fixed;
            top: 0;
            right: -420px;
            width: 400px;
            height: 100vh;
            background: #1a102c;
            border-left: 2px solid var(--primary-orange);
            box-shadow: -10px 0 35px rgba(0, 0, 0, 0.7);
            z-index: 9999;
            transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            padding: 1.5rem;
            overflow-y: auto;
            backdrop-filter: blur(8px);
        }}

        .detail-drawer.open {{
            right: 0;
        }}

        .drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(255, 138, 50, 0.25);
        }}

        .drawer-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .btn-drawer-close {{
            background: rgba(255, 138, 50, 0.15);
            border: 1px solid var(--primary-orange);
            color: var(--primary-orange);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.2s;
        }}

        .btn-drawer-close:hover {{
            background: var(--primary-orange);
            color: #ffffff;
            transform: scale(1.08);
        }}

        .drawer-body {{
            font-size: 0.85rem;
            color: var(--text-cream);
        }}

        .drawer-metric-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .drawer-metric-label {{
            color: var(--text-muted);
        }}

        .drawer-metric-val {{
            font-weight: 600;
            color: #ffffff;
        }}

        /* Leaflet Custom Marker Glow */
        .station-glow-marker {{
            background: var(--primary-orange);
            border: 2px solid #ffffff;
            border-radius: 50%;
            box-shadow: 0 0 12px #ff8a32, 0 0 20px #ff8a32;
            cursor: pointer;
            transition: transform 0.2s ease;
        }}

        .station-glow-marker:hover {{
            transform: scale(1.4);
        }}

        .station-glow-marker.selected {{
            background: #ffffff;
            border-color: var(--primary-orange);
            box-shadow: 0 0 25px #ff8a32, 0 0 40px #ff8a32;
            transform: scale(1.6);
        }}

        /* Footer */
        .app-footer {{
            margin-top: 2rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(255, 138, 50, 0.2);
            font-size: 0.78rem;
            color: var(--text-muted);
            line-height: 1.6;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
        }}
    </style>
</head>
<body>

<div class="app-container">

    <!-- Hero Header with Full Halloween Landscape SVG -->
    <header class="hero-header">
        <svg class="hero-svg-bg" viewBox="0 0 800 240" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#FFB37A" stop-opacity="1" />
                    <stop offset="60%" stop-color="#FF8A32" stop-opacity="0.85" />
                    <stop offset="100%" stop-color="#FF8A32" stop-opacity="0" />
                </radialGradient>
                <linearGradient id="mntGrad1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#341f53" />
                    <stop offset="100%" stop-color="#180f2a" />
                </linearGradient>
                <linearGradient id="mntGrad2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#211438" />
                    <stop offset="100%" stop-color="#130d22" />
                </linearGradient>
            </defs>
            <!-- Glowing Moon -->
            <circle cx="560" cy="85" r="55" fill="url(#moonGlow)" filter="drop-shadow(0 0 35px rgba(255,138,50,0.8))" />
            <circle cx="560" cy="85" r="42" fill="#FFA55C" />
            <circle cx="545" cy="75" r="9" fill="#E88235" opacity="0.4" />
            <circle cx="575" cy="90" r="14" fill="#E88235" opacity="0.35" />
            <circle cx="560" cy="105" r="6" fill="#E88235" opacity="0.3" />

            <!-- Flying Bats -->
            <path d="M410,50 Q418,42 426,50 Q434,42 442,50 Q426,58 410,50 Z" fill="#FF8A32" opacity="0.75" />
            <path d="M450,30 Q456,24 462,30 Q468,24 474,30 Q462,36 450,30 Z" fill="#FF8A32" opacity="0.6" />
            <path d="M490,65 Q495,60 500,65 Q505,60 510,65 Q500,70 490,65 Z" fill="#FF8A32" opacity="0.8" />
            <path d="M640,40 Q647,33 654,40 Q661,33 668,40 Q654,47 640,40 Z" fill="#FF8A32" opacity="0.65" />

            <!-- Mountains Background -->
            <path d="M260,240 L380,120 L480,190 L600,100 L720,200 L800,150 L800,240 Z" fill="url(#mntGrad1)" opacity="0.75" />
            <!-- Mountains Foreground -->
            <path d="M320,240 L440,150 L540,210 L680,140 L800,220 L800,240 Z" fill="url(#mntGrad2)" />

            <!-- Haunted House Silhouette -->
            <g transform="translate(680, 140)">
                <rect x="0" y="25" width="45" height="35" fill="#0C0817" />
                <polygon points="22.5,0 -5,25 50,25" fill="#0C0817" />
                <rect x="30" y="8" width="10" height="15" fill="#0C0817" />
                <!-- Glowing Windows -->
                <rect x="15" y="32" width="7" height="9" fill="#FF8A32" />
                <rect x="26" y="32" width="7" height="9" fill="#FF8A32" />
                <rect x="19" y="12" width="6" height="7" fill="#FFA55C" />
            </g>

            <!-- Spooky Pine Trees -->
            <polygon points="360,190 350,215 370,215" fill="#0D0719" />
            <polygon points="360,180 353,198 367,198" fill="#0D0719" />
            <polygon points="385,185 375,220 395,220" fill="#0D0719" />
            <polygon points="410,200 402,228 418,228" fill="#0D0719" />
            <polygon points="630,175 620,215 640,215" fill="#0D0719" />
            <polygon points="650,185 642,225 658,225" fill="#0D0719" />

            <!-- Jack-o'-Lantern Pumpkins on Hill -->
            <g transform="translate(610, 205)">
                <ellipse cx="12" cy="10" rx="12" ry="9" fill="#FF8A32" />
                <polygon points="12,1 10,4 14,4" fill="#388E3C" />
                <!-- Eyes & Spooky Smile -->
                <polygon points="7,8 9,6 9,10" fill="#130D22" />
                <polygon points="17,8 15,6 15,10" fill="#130D22" />
                <path d="M7,13 Q12,17 17,13 Z" fill="#130D22" />
            </g>
            <g transform="translate(585, 212) scale(0.75)">
                <ellipse cx="12" cy="10" rx="12" ry="9" fill="#FF8A32" />
                <polygon points="12,1 10,4 14,4" fill="#388E3C" />
                <polygon points="7,8 9,6 9,10" fill="#130D22" />
                <polygon points="17,8 15,6 15,10" fill="#130D22" />
                <path d="M7,13 Q12,17 17,13 Z" fill="#130D22" />
            </g>
        </svg>

        <div class="hero-content">
            <div class="hero-badge-row">
                <span class="hero-badge">🎃 HALLOWEEN EDITION</span>
                <span class="hero-badge hero-badge-purple">📅 ข้อมูลจริงปี 2022–2023</span>
                <span class="hero-badge">🏔️ 9 จังหวัดพื้นที่สูง (50 สถานี)</span>
                <span class="hero-badge hero-badge-purple">🌾 ข้าวนาปี 25 ตำบล (5 จังหวัด)</span>
                <span class="hero-badge">⚠️ วิเคราะห์เชิงสำรวจ (Non-causal)</span>
            </div>
            <h1 class="hero-title">ระบบวิเคราะห์สภาพภูมิอากาศบนพื้นที่สูงและผลผลิตข้าวนาปี</h1>
            <p class="hero-subtitle">
                สำรวจข้อมูลเปิดสภาพภูมิอากาศรายเดือนจากสถานีตรวจวัดบนพื้นที่สูง (HRDI & OWM) และความสัมพันธ์กับการเปลี่ยนแปลงผลผลิตข้าวนาปี
                พร้อมระบบ Interactive Cross-Filtering และแผนที่ซูมกล้องแบบ Smooth Animation
            </p>
        </div>
    </header>

    <!-- Top Navigation Tabs -->
    <nav class="nav-tabs" id="navTabs">
        <button class="nav-tab-btn active" data-tab="page1">
            <span>🛰️</span> ภาพรวมภูมิอากาศ 9 จังหวัด
        </button>
        <button class="nav-tab-btn" data-tab="page2">
            <span>🌧️</span> เปรียบเทียบฝน HRDI vs HII
        </button>
        <button class="nav-tab-btn" data-tab="page3">
            <span>🌾</span> ผลผลิตข้าวนาปีระดับตำบล
        </button>
        <button class="nav-tab-btn" data-tab="page4">
            <span>📈</span> วิเคราะห์ความสัมพันธ์ฝน-ข้าว
        </button>
        <button class="nav-tab-btn" data-tab="page5">
            <span>ℹ️</span> ข้อมูลและระเบียบวิธีวิจัย
        </button>
    </nav>

    <!-- Main Layout: Sidebar Filters + Pages -->
    <div class="layout-wrapper">
        
        <!-- Left Sidebar Controls -->
        <aside class="sidebar-card">
            <div class="sidebar-title">
                <span>🎃</span> ตัวกรองอัจฉริยะ (Filters)
            </div>

            <!-- Filter: Year -->
            <div class="filter-group">
                <label class="filter-label">เลือกปี (Year):</label>
                <select id="filterYear" class="filter-select">
                    <option value="all">ทั้งหมด (2022–2023)</option>
                    <option value="2022">ปี 2022</option>
                    <option value="2023">ปี 2023</option>
                </select>
            </div>

            <!-- Filter: Province -->
            <div class="filter-group">
                <label class="filter-label">เลือกจังหวัด (Province):</label>
                <select id="filterProvince" class="filter-select">
                    <option value="all">ทุกจังหวัด (ภาพรวม 9 จังหวัด)</option>
                    <option value="เชียงใหม่">เชียงใหม่ (14 ตำบล / 17 สถานี)</option>
                    <option value="น่าน">น่าน (5 ตำบล / 7 สถานี)</option>
                    <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (3 ตำบล / 4 สถานี)</option>
                    <option value="ตาก">ตาก (2 ตำบล / 6 สถานี)</option>
                    <option value="เชียงราย">เชียงราย (1 ตำบล / 7 สถานี)</option>
                    <option value="กำแพงเพชร">กำแพงเพชร (2 สถานี)</option>
                    <option value="พิษณุโลก">พิษณุโลก (3 สถานี)</option>
                    <option value="เพชรบูรณ์">เพชรบูรณ์ (2 สถานี)</option>
                    <option value="กาญจนบุรี">กาญจนบุรี (2 สถานี)</option>
                </select>
            </div>

            <!-- Filter: Weather Variable -->
            <div class="filter-group">
                <label class="filter-label">ตัวแปรสภาพอากาศ:</label>
                <select id="filterVariable" class="filter-select">
                    <option value="rain">ปริมาณน้ำฝน (หน่วยรอยืนยัน mm)</option>
                    <option value="temp">อุณหภูมิเฉลี่ย (°C)</option>
                    <option value="humidity">ความชื้นสัมพัทธ์ (%)</option>
                    <option value="wind">ความเร็วลม (m/s)</option>
                </select>
            </div>

            <!-- Action Buttons -->
            <button class="btn-action btn-reset-map" id="btnResetMap">
                <span>🗺️</span> รีเซ็ตแผนที่สู่ภาพรวม
            </button>
            <button class="btn-action btn-reset-all" id="btnResetAll">
                <span>🔄</span> ล้างตัวกรองทั้งหมด
            </button>

            <!-- Status Indicator -->
            <div class="sidebar-active-status">
                <strong>📍 สถานะการเลือกปัจจุบัน:</strong><br/>
                พื้นที่: <span id="statusProvinceBadge" class="active-filter-badge">ภาพรวม 9 จังหวัด</span><br/>
                สถานี: <span id="statusStationBadge" class="active-filter-badge">ทุกสถานี (50)</span><br/>
                ช่วงปี: <span id="statusYearBadge" class="active-filter-badge">2022–2023</span>
            </div>
        </aside>

        <!-- Right Content Area -->
        <main class="content-area">

            <!-- ======================================================== -->
            <!-- PAGE 1: CLIMATE OVERVIEW (9 PROVINCES, 50 STATIONS)      -->
            <!-- ======================================================== -->
            <section id="page1" class="page-view active">
                
                <!-- Notice Callout -->
                <div class="halloween-notice">
                    <strong>⚠️ คำเตือนการแปลผลสภาพภูมิอากาศ:</strong> ข้อมูลรวบรวมจากสถานีตรวจวัดเฉพาะจุดบนพื้นที่สูงของโครงการหลวง (HRDI) 
                    และแบบจำลอง OWM <strong>ไม่ใช่ตัวแทนค่าเฉลี่ยของทั้งจังหวัด</strong> และมี Missing Rows 217 แถวเนื่องจากเปิดบันทึกไม่พร้อมกัน 
                    ห้ามนำยอดรวมทั้งปีของสถานีที่ไม่ครบไปเทียบกับสถานีที่ครบ 12 เดือน
                </div>

                <!-- KPI Cards Grid -->
                <div class="kpi-grid">
                    <div class="kpi-card" data-action="focus-rain">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ปริมาณฝนเฉลี่ย/เดือน</span>
                            <span class="kpi-icon">🌧️</span>
                        </div>
                        <div class="kpi-value delta-orange" id="kpiRainVal">118.4</div>
                        <div class="kpi-subtext">
                            <span class="kpi-delta delta-orange">หน่วยรอยืนยัน (mm)</span> • 976 ค่าสมบูรณ์
                        </div>
                    </div>

                    <div class="kpi-card" data-action="focus-temp">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">อุณหภูมิเฉลี่ย</span>
                            <span class="kpi-icon">🌡️</span>
                        </div>
                        <div class="kpi-value delta-purple" id="kpiTempVal">21.8 °C</div>
                        <div class="kpi-subtext">
                            <span class="kpi-delta delta-purple">ครบ 100%</span> • 983 สถานี-เดือน
                        </div>
                    </div>

                    <div class="kpi-card" data-action="focus-humidity">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ความชื้นสัมพัทธ์เฉลี่ย</span>
                            <span class="kpi-icon">💧</span>
                        </div>
                        <div class="kpi-value delta-cyan" id="kpiHumidityVal">78.2 %</div>
                        <div class="kpi-subtext">
                            <span class="kpi-delta delta-cyan">ครบ 100%</span> • สภาพอากาศชื้นสูง
                        </div>
                    </div>

                    <div class="kpi-card" data-action="focus-wind">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ความเร็วลมเฉลี่ย</span>
                            <span class="kpi-icon">🍃</span>
                        </div>
                        <div class="kpi-value delta-pink" id="kpiWindVal">1.48 m/s</div>
                        <div class="kpi-subtext">
                            <span class="kpi-delta delta-pink">ครบ 100%</span> • ลมสงบ-ปานกลาง
                        </div>
                    </div>
                </div>

                <!-- Interactive Map Bento Card -->
                <div class="bento-card">
                    <div class="card-header-row">
                        <div>
                            <div class="card-title">
                                <span>🗺️</span> แผนที่สถานีตรวจวัดบนพื้นที่สูง 50 สถานี (Smooth Animated Map)
                            </div>
                            <div class="card-subtitle">
                                คลิกที่หมุดสถานีหรือเลือกจังหวัดเพื่อซูมกล้องเข้าสู่นุ่มนวล (800–1,200ms) พร้อมเปิดแผงข้อมูลรายละเอียด
                            </div>
                        </div>
                        <span id="mapSelectedIndicator" class="hero-badge">มุมมอง: ภาพรวม 9 จังหวัด</span>
                    </div>

                    <div id="map-container">
                        <div class="map-breadcrumb">
                            <span id="mapBreadcrumbText">📍 ภาพรวม 9 จังหวัด (50 สถานี)</span>
                            <button id="btnMapBack" class="btn-map-back">⬅️ ย้อนกลับสู่ภาพรวม</button>
                        </div>
                        <div id="leafletMap" style="width:100%; height:100%;"></div>
                    </div>
                </div>

                <!-- Two Charts Bento Row -->
                <div class="two-col-grid">
                    <!-- Chart 1: Monthly Trend -->
                    <div class="bento-card">
                        <div class="card-header-row">
                            <div class="card-title">
                                <span>📈</span> แนวโน้มสภาพภูมิอากาศรายเดือน (2022–2023)
                            </div>
                            <span class="card-subtitle" id="trendChartSubtitle">9 จังหวัด</span>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartMonthlyTrend"></canvas>
                        </div>
                    </div>

                    <!-- Chart 2: Station Comparison -->
                    <div class="bento-card">
                        <div class="card-header-row">
                            <div class="card-title">
                                <span>📊</span> เปรียบเทียบสถานีตรวจวัดในจังหวัดที่เลือก
                            </div>
                            <span class="card-subtitle" id="stationChartSubtitle">คลิกแท่งเพื่อซูมสถานี</span>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartStationCompare"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Completeness Breakdown Card -->
                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>🔍</span> รายงานความครบถ้วนของข้อมูลสถานี–เดือน (Data Completeness Audit)
                        </div>
                        <span class="hero-badge hero-badge-purple">ความครบถ้วน 81.9%</span>
                    </div>
                    <p style="font-size:0.83rem; color:var(--text-muted); margin-bottom:0.75rem;">
                        ข้อมูลตามเมทริกซ์ 50 สถานี × 24 เดือน (1,200 ระเบียน): มีข้อมูลจริง 983 แถว (ค่าฝนสมบูรณ์ 976 แถว, Missing Values 7 แถว), 
                        และ <strong>Missing Rows 217 แถว</strong> (18.1%) เนื่องจากบางสถานียังไม่ติดตั้งหรือปิดการบันทึก
                    </p>
                    <div class="two-col-grid">
                        <div style="background:#170E26; padding:0.85rem; border-radius:10px; border-left:3px solid var(--primary-orange);">
                            <strong style="color:var(--primary-orange);">🟢 สถานะค่าฝน (Rainfall):</strong>
                            <div style="margin-top:0.35rem; font-size:0.8rem; color:#f0e6fc;">
                                • ข้อมูลสมบูรณ์: <strong>976 แถว</strong><br/>
                                • ค่าว่าง (Missing Values): <strong>7 แถว</strong><br/>
                                • ค่าฝนเป็น 0.0 มม.: <strong>73 แถว</strong>
                            </div>
                        </div>
                        <div style="background:#170E26; padding:0.85rem; border-radius:10px; border-left:3px solid var(--secondary-lavender);">
                            <strong style="color:var(--secondary-lavender);">🟣 สถานะตัวแปรอื่น:</strong>
                            <div style="margin-top:0.35rem; font-size:0.8rem; color:#f0e6fc;">
                                • อุณหภูมิ, ความชื้น, ลม: <strong>ครบ 983 แถว (100%)</strong><br/>
                                • Temp Min/Max, ความกดอากาศ: <strong>883 แถว (เฉพาะ OWM)</strong><br/>
                                • PM2.5: <strong>99 แถว (ไม่สมบูรณ์)</strong>
                            </div>
                        </div>
                    </div>
                </div>

            </section>

            <!-- ======================================================== -->
            <!-- PAGE 2: RAINFALL COMPARISON (HRDI vs HII)                -->
            <!-- ======================================================== -->
            <section id="page2" class="page-view">
                
                <div class="halloween-notice halloween-notice-purple">
                    <strong>⚠️ คำอธิบายความแตกต่างของระดับพื้นที่ (Spatial Granularity):</strong><br/>
                    • <strong>ฝน HRDI:</strong> วัดจากสถานีตรวจวัดเฉพาะจุดบนพื้นที่สูงในตำบล (Point Measurements)<br/>
                    • <strong>ฝน HII:</strong> ค่าเฉลี่ยฝนสะสมระดับจังหวัดของ สสน. (Provincial Aggregate)<br/>
                    • <strong>ข้อควรระวัง:</strong> ห้ามนับค่า HII ที่ซ้ำกันในหลายตำบลเป็นตัวอย่างอิสระ และนิยาม/หน่วย <code>AvgRain</code> ของ HII ยังรอยืนยันจากเอกสารต้นทาง
                </div>

                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>🌧️</span> เปรียบเทียบฝน HRDI (สถานีพื้นที่สูง) กับ HII (ฝนจังหวัด) ช่วง ก.พ.–ก.ค.
                        </div>
                        <span class="hero-badge">เปรียบเทียบปี 2022 vs 2023</span>
                    </div>
                    <div class="chart-box" style="height: 380px;">
                        <canvas id="chartRainCompare"></canvas>
                    </div>
                </div>

                <div class="two-col-grid">
                    <div class="bento-card">
                        <div class="card-header-row">
                            <div class="card-title">
                                <span>📉</span> การเปลี่ยนแปลงฝน HRDI รายจังหวัด (2023 ลบ 2022)
                            </div>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartHrdiDeltaProv"></canvas>
                        </div>
                    </div>

                    <div class="bento-card">
                        <div class="card-header-row">
                            <div class="card-title">
                                <span>📉</span> การเปลี่ยนแปลงฝน HII รายจังหวัด (2023 ลบ 2022)
                            </div>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartHiiDeltaProv"></canvas>
                        </div>
                    </div>
                </div>

            </section>

            <!-- ======================================================== -->
            <!-- PAGE 3: RICE YIELD (25 TAMBONS BALANCED PANEL)           -->
            <!-- ======================================================== -->
            <section id="page3" class="page-view">
                
                <div class="halloween-notice">
                    <strong>🌾 ขอบเขตกลุ่มตัวอย่างข้าวนาปี (Balanced Panel):</strong> 25 ตำบลใน 5 จังหวัดที่มีข้อมูลครบทั้งปี 2022 และ 2023 
                    (รวม 50 ระเบียนตำบล–ปี) โดย <strong>เชียงใหม่คิดเป็น 56% (14 ตำบล)</strong>, น่าน 5, แม่ฮ่องสอน 3, ตาก 2, เชียงราย 1 
                    กลุ่มตัวอย่างนี้ไม่ใช่ตัวแทนของพื้นที่สูง 9 จังหวัด
                </div>

                <!-- KPI Rice -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">จำนวนตำบลวิเคราะห์</span>
                            <span class="kpi-icon">🌾</span>
                        </div>
                        <div class="kpi-value delta-orange">25</div>
                        <div class="kpi-subtext"><span class="kpi-delta delta-orange">Balanced Panel</span> • 5 จังหวัด</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ผลผลิตเฉลี่ยปี 2022</span>
                            <span class="kpi-icon">📊</span>
                        </div>
                        <div class="kpi-value delta-purple" id="kpiYield2022">478.6</div>
                        <div class="kpi-subtext">หน่วยรอยืนยันต่อพื้นที่เก็บเกี่ยว</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ผลผลิตเฉลี่ยปี 2023</span>
                            <span class="kpi-icon">📈</span>
                        </div>
                        <div class="kpi-value delta-pink" id="kpiYield2023">474.3</div>
                        <div class="kpi-subtext">หน่วยรอยืนยันต่อพื้นที่เก็บเกี่ยว</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">ทิศทางผลผลิตรายตำบล</span>
                            <span class="kpi-icon">⚖️</span>
                        </div>
                        <div class="kpi-value delta-cyan">+10 | -10</div>
                        <div class="kpi-subtext">เพิ่ม 10, ลด 10, เท่าเดิม 5 ตำบล</div>
                    </div>
                </div>

                <!-- Slope Chart / Paired Bar -->
                <div class="bento-card">
                    <div class="card-header-row">
                        <div>
                            <div class="card-title">
                                <span>🌾</span> ผลผลิตข้าวนาปีต่อพื้นที่เก็บเกี่ยวรายตำบล (2022 vs 2023)
                            </div>
                            <div class="card-subtitle">คลิกที่ตำบลในกราฟหรือตารางเพื่อดูประวัติและข้อมูลฝนเฉพาะตำบล</div>
                        </div>
                        <span class="hero-badge">25 ตำบลเดิม</span>
                    </div>
                    <div class="chart-box" style="height: 380px;">
                        <canvas id="chartRiceSlope"></canvas>
                    </div>
                </div>

                <!-- Tambon Searchable Table -->
                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>📋</span> ทะเบียนข้อมูลข้าวนาปีและฝน 25 ตำบล (คลิกแถวเพื่อดูรายละเอียด)
                        </div>
                        <input type="text" id="searchTambonInput" class="filter-input" placeholder="🔍 ค้นหาตำบล, อำเภอ หรือรหัส..." style="width: 220px;">
                    </div>
                    <div class="custom-table-wrapper">
                        <table class="custom-table" id="tambonTable">
                            <thead>
                                <tr>
                                    <th>รหัสตำบล</th>
                                    <th>ตำบล</th>
                                    <th>อำเภอ</th>
                                    <th>จังหวัด</th>
                                    <th>ผลผลิต 2022</th>
                                    <th>ผลผลิต 2023</th>
                                    <th>Δ ผลผลิต</th>
                                    <th>ฝน HRDI 2022</th>
                                    <th>ฝน HRDI 2023</th>
                                    <th>Δ ฝน HRDI</th>
                                </tr>
                            </thead>
                            <tbody id="tambonTableBody">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>

            </section>

            <!-- ======================================================== -->
            <!-- PAGE 4: CORRELATION ANALYSIS                             -->
            <!-- ======================================================== -->
            <section id="page4" class="page-view">
                
                <div class="halloween-notice" style="border-left-color: #ef4444; background: rgba(239, 68, 68, 0.1);">
                    <strong>🛑 ข้อกำหนดจริยธรรมข้อมูล (Non-Causal & No Forecasting):</strong><br/>
                    • ค่าสหสัมพันธ์อันดับ Spearman ที่ติดลบเป็นการสำรวจทิศทางข้อมูลของ 2 ปี <strong>ห้ามสรุปว่าการลดลงของฝนเป็นสาเหตุให้ผลผลิตเพิ่มขึ้น</strong><br/>
                    • ห้ามนำโมเดลนี้ไปใช้ทำนายหรือพยากรณ์ผลผลิตในอนาคต (No Forecasting Allowed)<br/>
                    • ขนาดตัวอย่างระดับจังหวัดมีเพียง $n = 5$ จังหวัด ซึ่งมีความอ่อนไหวสูงมากต่อการเลือกตัวอย่าง ไม่สามารถสรุปว่า HII เหนือกว่า HRDI ได้
                </div>

                <!-- Spearman Summary Metrics -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">Spearman rho (ตำบล)</span>
                            <span class="kpi-icon">📍</span>
                        </div>
                        <div class="kpi-value delta-orange">-0.1734</div>
                        <div class="kpi-subtext">ขนาดตัวอย่าง n = 25 ตำบล (Weak Negative)</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">Spearman rho (HRDI จังหวัด)</span>
                            <span class="kpi-icon">🏔️</span>
                        </div>
                        <div class="kpi-value delta-purple">-0.7000</div>
                        <div class="kpi-subtext">ขนาดตัวอย่าง n = 5 จังหวัด (ค่าเฉลี่ยสถานี)</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">Spearman rho (HII จังหวัด)</span>
                            <span class="kpi-icon">🌧️</span>
                        </div>
                        <div class="kpi-value delta-cyan">-0.9000</div>
                        <div class="kpi-subtext">ขนาดตัวอย่าง n = 5 จังหวัด (ฝนรวมจังหวัด)</div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-icon-row">
                            <span class="kpi-title">Leave-One-Province-Out</span>
                            <span class="kpi-icon">🎯</span>
                        </div>
                        <div class="kpi-value delta-pink">-0.52 ถึง +0.03</div>
                        <div class="kpi-subtext">ช่วง rho ระดับตำบลเมื่อตัดจังหวัดออก</div>
                    </div>
                </div>

                <!-- Scatter Plots Row -->
                <div class="two-col-grid">
                    <!-- Scatter Tambon -->
                    <div class="bento-card">
                        <div class="card-header-row">
                            <div>
                                <div class="card-title">
                                    <span>🔍</span> Scatter Plot ระดับตำบล (n = 25 จุด)
                                </div>
                                <div class="card-subtitle">Δ ฝน HRDI ก.พ.–ก.ค. vs Δ ผลผลิตข้าวนาปี (คลิกจุดเพื่อดูข้อมูล)</div>
                            </div>
                            <span class="hero-badge">rho = -0.1734</span>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartScatterTambon"></canvas>
                        </div>
                    </div>

                    <!-- Scatter Province -->
                    <div class="bento-card">
                        <div class="card-header-row">
                            <div>
                                <div class="card-title">
                                    <span>🗺️</span> Scatter Plot ระดับจังหวัด (n = 5 จุด)
                                </div>
                                <div class="card-subtitle">Δ ฝน (HRDI / HII) vs Δ ผลผลิตเฉลี่ยของตำบลในจังหวัด</div>
                            </div>
                            <span class="hero-badge hero-badge-purple">5 จังหวัด</span>
                        </div>
                        <div class="chart-box">
                            <canvas id="chartScatterProvince"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Sensitivity Table Card -->
                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>🧪</span> ผลการทดสอบความไว: ตัดจังหวัดออกทีละแห่ง (Leave-One-Province-Out)
                        </div>
                    </div>
                    <div class="custom-table-wrapper">
                        <table class="custom-table">
                            <thead>
                                <tr>
                                    <th>จังหวัดที่ตัดออก</th>
                                    <th>จำนวนตำบลที่เหลือ</th>
                                    <th>rho HRDI ตำบล</th>
                                    <th>rho HRDI จังหวัด</th>
                                    <th>rho HII จังหวัด</th>
                                    <th>ข้อสังเกต</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>เชียงใหม่ (รหัส 50)</td>
                                    <td>11 ตำบล</td>
                                    <td style="color:#4ade80; font-weight:600;">+0.0303</td>
                                    <td>-0.8000</td>
                                    <td>-0.8000</td>
                                    <td>เมื่อตัดเชียงใหม่ออก ค่า rho ตำบลเปลี่ยนเป็นบวก สะท้อนอิทธิพลของเชียงใหม่ (56%)</td>
                                </tr>
                                <tr>
                                    <td>น่าน (รหัส 55)</td>
                                    <td>20 ตำบล</td>
                                    <td>-0.1245</td>
                                    <td>-0.8000</td>
                                    <td>-0.8000</td>
                                    <td>ค่า rho ใกล้เคียงเดิม</td>
                                </tr>
                                <tr>
                                    <td>เชียงราย (รหัส 57)</td>
                                    <td>24 ตำบล</td>
                                    <td>-0.1989</td>
                                    <td>-0.4000</td>
                                    <td>-1.0000</td>
                                    <td>rho HRDI จังหวัดลดลงเหลือ -0.4</td>
                                </tr>
                                <tr>
                                    <td>แม่ฮ่องสอน (รหัส 58)</td>
                                    <td>22 ตำบล</td>
                                    <td>-0.0988</td>
                                    <td>-1.0000</td>
                                    <td>-0.8000</td>
                                    <td>rho HRDI จังหวัดเปลี่ยนเป็น -1.0</td>
                                </tr>
                                <tr>
                                    <td>ตาก (รหัส 63)</td>
                                    <td>23 ตำบล</td>
                                    <td>-0.5285</td>
                                    <td>-0.8000</td>
                                    <td>-1.0000</td>
                                    <td>rho HRDI ตำบลติดลบเพิ่มขึ้นเป็น -0.5285</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </section>

            <!-- ======================================================== -->
            <!-- PAGE 5: ABOUT & METHODOLOGY                              -->
            <!-- ======================================================== -->
            <section id="page5" class="page-view">
                
                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>📖</span> แหล่งที่มาของข้อมูลและการประมวลผล (Data Pipeline)
                        </div>
                    </div>
                    <div style="line-height:1.7; font-size:0.85rem; color:#f0e6fc;">
                        <p><strong>1. ข้อมูลสภาพภูมิอากาศ (สถาบันวิจัยและพัฒนาพื้นที่สูง - HRDI):</strong> ข้อมูลจากสถานีตรวจวัดสภาพอากาศภาคพื้นดิน 100 แถว และแบบจำลอง OpenWeatherMap (OWM) 883 แถว รวม 983 ระเบียนสถานี–เดือน ครอบคลุม 50 สถานีใน 9 จังหวัด</p>
                        <p><strong>2. ข้อมูลผลผลิตข้าวนาปี (กรมส่งเสริมการเกษตร - DOA):</strong> ข้อมูลปี 2565 (2022) และปี 2566 (2023) ที่ผ่านการจับคู่รหัสตำบล 6 หลักสมบูรณ์ 25 ตำบลใน 5 จังหวัด</p>
                        <p><strong>3. ข้อมูลฝนระดับจังหวัด (สถาบันสารสนเทศทรัพยากรน้ำ - HII):</strong> ปริมาณฝนสะสมรายเดือนระดับจังหวัดจากไฟล์ <code>spatial-rain-hii.csv</code> คอลัมน์ <code>AvgRain</code></p>
                    </div>
                </div>

                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>🗺️</span> ตรวจสอบการจับคู่รหัสตำบล 25 ตำบล (Area Matching Validation)
                        </div>
                        <span class="hero-badge">ผ่านการรับรอง 100%</span>
                    </div>
                    <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:0.75rem;">
                        ข้อมูลปี 2022 ที่เก็บรหัสแยกส่วน (จังหวัด/อำเภอ/ตำบล) ได้ถูกประกอบเป็นรหัส 6 หลัก และเทียบกับข้อมูลปี 2023 
                        ผลการตรวจสอบกับฐานข้อมูลทางการของไทย (<code>geo.json</code>) พบว่าถูกต้องครบทั้ง 25 ตำบล:
                    </p>
                    <div style="font-size:0.82rem; color:#f0e6fc; line-height:1.6;">
                        • <strong>เชียงใหม่ (14 ตำบล):</strong> สบเตี๊ยะ, แม่นาจร, เชียงดาว, แม่นะ, เมืองคอง, ป่าแป๋, กึ้ดช้าง, เมืองก๋าย, สะเมิงใต้, สะเมิงเหนือ, แม่แดด, แม่ตื่น, ม่อนจอง, แสนไห<br/>
                        • <strong>น่าน (5 ตำบล):</strong> บ่อสวก, น้ำพาง, สกาด, ดงพญา, ผาช้างน้อย<br/>
                        • <strong>แม่ฮ่องสอน (3 ตำบล):</strong> ขุนยวม, สบเมย, แม่คะตวน<br/>
                        • <strong>ตาก (2 ตำบล):</strong> แม่ตื่น, ท่าสองยาง<br/>
                        • <strong>เชียงราย (1 ตำบล):</strong> ปอ
                    </div>
                </div>

                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>⚠️</span> ข้อจำกัดทางสถิติและข้อกำหนดทางธุรกิจ 11 ข้อ (BRD Limitations)
                        </div>
                    </div>
                    <ul style="padding-left:1.25rem; font-size:0.82rem; color:#f0e6fc; line-height:1.7;">
                        <li>1. มีข้อมูลเพียง 2 ปี (2022–2023) ไม่เพียงพอสำหรับการวิเคราะห์แนวโน้มระยะยาว</li>
                        <li>2. 5 จังหวัดที่มีข้อมูลข้าวนาปีไม่ใช่ตัวแทนของพื้นที่สูง 9 จังหวัด</li>
                        <li>3. เชียงใหม่คิดเป็น 56% ของตำบลที่ศึกษา อาจทำให้ผลสะท้อนลักษณะเฉพาะของเชียงใหม่เป็นหลัก</li>
                        <li>4. HII เป็นข้อมูลระดับจังหวัด ห้ามนับค่า HII ที่ซ้ำในระดับตำบลเป็นตัวอย่างอิสระ</li>
                        <li>5. หน่วยและนิยาม AvgRain ของ HII ยังรอยืนยันจากเอกสารต้นทาง</li>
                        <li>6. หน่วยผลผลิตและพื้นที่เก็บเกี่ยวยังรอยืนยันจากเอกสารต้นทาง (แสดงเป็น "หน่วยรอยืนยัน")</li>
                        <li>7. ช่วง ก.พ.–ก.ค. เลือกจากความครบถ้วนของข้อมูลสถานี ยังไม่ยืนยันว่าเป็นฤดูปลูกข้าวนาปีจริง</li>
                        <li>8. ผลรวมฝน HRDI และ HII ไม่อาจเทียบกันตรง ๆ เนื่องจากวิธีตรวจวัดและระดับพื้นที่ต่างกัน</li>
                        <li>9. ห้ามสรุปว่า HII ดีกว่า HRDI จากค่า rho เพียงอย่างเดียวเนื่องจาก n=5 มีความอ่อนไหวสูงมาก</li>
                        <li>10. ห้ามสรุปว่าฝนเป็นสาเหตุให้ผลผลิตเพิ่มหรือลด (Non-causal interpretation)</li>
                        <li>11. ห้ามนำผลการศึกษานี้ไปใช้เป็นโมเดลพยากรณ์หรือทำนาย (No Forecasting)</li>
                    </ul>
                </div>

                <div class="bento-card">
                    <div class="card-header-row">
                        <div class="card-title">
                            <span>🎮</span> คู่มือการใช้งานระบบโต้ตอบ (Interactive Features Guide)
                        </div>
                    </div>
                    <div style="font-size:0.82rem; color:#f0e6fc; line-height:1.6;">
                        • <strong>คลิกจังหวัดบนแผนที่:</strong> แผนที่จะเลื่อนกล้องและซูมเข้าสู่จังหวัดนั้นอย่างนุ่มนวล (Smooth Ease-in-out Zoom 1,000ms) พร้อมกรอง KPI กราฟ และเปิด Detail Drawer ด้านขวา<br/>
                        • <strong>คลิกแท่งกราฟ หรือจุด Scatter:</strong> แสดงรายละเอียดเฉพาะจุดทันทีและไฮไลต์ตำแหน่งบนแผนที่<br/>
                        • <strong>คลิกซ้ำ:</strong> ยกเลิกการเลือกและคืนค่ามุมมอง<br/>
                        • <strong>ปุ่ม [✕]:</strong> ปิดแผงรายละเอียดด้านขวาโดยไม่ล้างตัวกรองอื่น<br/>
                        • <strong>ปุ่ม ⬅️ ย้อนกลับ:</strong> ซูมแผนที่กลับสู่ภาพรวม 9 จังหวัดอย่างนุ่มนวล<br/>
                        • <strong>ปุ่ม 🔄 ล้างตัวกรองทั้งหมด:</strong> คืนค่าทุกองค์ประกอบสู่ค่าเริ่มต้น
                    </div>
                </div>

            </section>

        </main>
    </div>

    <!-- Halloween Detail Drawer -->
    <div class="detail-drawer" id="detailDrawer">
        <div class="drawer-header">
            <div class="drawer-title">
                <span>🎃</span> <span id="drawerTitleText">รายละเอียดข้อมูล</span>
            </div>
            <button class="btn-drawer-close" id="btnDrawerClose" title="ปิดแผงนี้ [X]">✕</button>
        </div>
        <div class="drawer-body" id="drawerBodyContent">
            <!-- Dynamic Content -->
        </div>
    </div>

    <!-- Footer -->
    <footer class="app-footer">
        <div>
            <strong>Highland Rainfall Project — Halloween Edition 🎃</strong><br/>
            ข้อมูลจริงปี 2022–2023 • แหล่งข้อมูล: HRDI, DOA, HII, OWM • ออกแบบเพื่อการวิเคราะห์ข้อมูลเปิดอย่างโปร่งใส
        </div>
        <div style="text-align: right;">
            สถานะ QA: ผ่านเกณฑ์ BRD Section 8 ครบ 100%<br/>
            Branch: <code>dashboard-dev</code> • Streamlit & Plotly/Chart.js Architecture
        </div>
    </footer>

</div>

<!-- Injected Real Data Payload -->
<script>
    const REAL_DATA = {data_json};
</script>

<!-- Halloween App Controller & Smooth Zoom Engine -->
<script>
document.addEventListener('DOMContentLoaded', () => {{

    // State Management
    const state = {{
        activeTab: 'page1',
        selectedYear: 'all',
        selectedProvince: 'all',
        selectedVariable: 'rain',
        selectedStation: null,
        selectedTambon: null,
        isDrawerOpen: false
    }};

    // DOM Elements
    const navTabs = document.querySelectorAll('.nav-tab-btn');
    const pageViews = document.querySelectorAll('.page-view');
    const filterYear = document.getElementById('filterYear');
    const filterProvince = document.getElementById('filterProvince');
    const filterVariable = document.getElementById('filterVariable');
    const btnResetAll = document.getElementById('btnResetAll');
    const btnResetMap = document.getElementById('btnResetMap');
    const btnMapBack = document.getElementById('btnMapBack');
    const mapBreadcrumbText = document.getElementById('mapBreadcrumbText');
    const mapSelectedIndicator = document.getElementById('mapSelectedIndicator');
    const statusProvinceBadge = document.getElementById('statusProvinceBadge');
    const statusStationBadge = document.getElementById('statusStationBadge');
    const statusYearBadge = document.getElementById('statusYearBadge');
    const detailDrawer = document.getElementById('detailDrawer');
    const btnDrawerClose = document.getElementById('btnDrawerClose');
    const drawerTitleText = document.getElementById('drawerTitleText');
    const drawerBodyContent = document.getElementById('drawerBodyContent');

    // Chart instances store
    let chartTrend = null;
    let chartStation = null;
    let chartRainComp = null;
    let chartHrdiDelta = null;
    let chartHiiDelta = null;
    let chartRiceSlope = null;
    let chartScatterTambon = null;
    let chartScatterProvince = null;

    // -------------------------------------------------------------
    // 1. LEAFLET MAP INITIALIZATION WITH SMOOTH ANIMATED ZOOM
    // -------------------------------------------------------------
    const overviewCenter = [REAL_DATA.overview_center.lat, REAL_DATA.overview_center.lng];
    const overviewZoom = REAL_DATA.overview_center.zoom;

    const map = L.map('leafletMap', {{
        center: overviewCenter,
        zoom: overviewZoom,
        minZoom: 5.5,
        maxZoom: 14,
        zoomControl: true
    }});

    // Dark Matter Tiles (Night Theme)
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 19
    }}).addTo(map);

    // Marker Layer Group
    const stationMarkersGroup = L.layerGroup().addTo(map);
    const provinceCirclesGroup = L.layerGroup().addTo(map);
    const stationMarkersMap = {{}};

    // Render Province Ambient Circles
    Object.entries(REAL_DATA.centers).forEach(([pName, pData]) => {{
        const circle = L.circle([pData.lat, pData.lng], {{
            color: '#FF8A32',
            fillColor: '#FF8A32',
            fillOpacity: 0.08,
            weight: 1.5,
            radius: 35000,
            dashArray: '4, 8'
        }}).addTo(provinceCirclesGroup);

        circle.bindTooltip(`<b>จังหวัด${{pName}}</b><br><span style="color:#FF8A32">คลิกเพื่อซูมเข้าสู่จังหวัด</span>`, {{
            className: 'custom-tooltip',
            direction: 'top'
        }});

        circle.on('click', () => {{
            selectProvince(pName);
        }});
    }});

    // Render 50 Stations Markers
    REAL_DATA.stations.forEach(sta => {{
        const marker = L.circleMarker([sta.lat, sta.lng], {{
            radius: 6,
            fillColor: '#FF8A32',
            color: '#ffffff',
            weight: 1.5,
            opacity: 0.95,
            fillOpacity: 0.85
        }});

        marker.bindTooltip(`
            <div style="font-family:'Prompt',sans-serif; font-size:12px; color:#130D22;">
                <strong style="color:#d9650b;">🎃 ${{sta.name}}</strong><br>
                จังหวัด: ${{sta.province}} (${{sta.amphoe}})<br>
                ฝนเฉลี่ย: ${{sta.mean_rain}} mm (รอยืนยัน)<br>
                อุณหภูมิ: ${{sta.mean_temp}} °C<br>
                แหล่งข้อมูล: ${{sta.source}}
            </div>
        `, {{ direction: 'top' }});

        marker.on('click', (e) => {{
            L.DomEvent.stopPropagation(e);
            selectStation(sta);
        }});

        stationMarkersGroup.addLayer(marker);
        stationMarkersMap[sta.name] = marker;
    }});

    // Smooth FlyTo Function
    function smoothFlyTo(lat, lng, zoom) {{
        map.flyTo([lat, lng], zoom, {{
            duration: 1.0,           // 1,000ms duration
            easeLinearity: 0.25,     // Smooth ease-in-out
            essential: true
        }});
    }}

    // -------------------------------------------------------------
    // 2. CENTRALIZED STATE ACTIONS
    // -------------------------------------------------------------
    function selectProvince(provName) {{
        if (state.selectedProvince === provName) {{
            // Toggle off
            resetProvinceView();
            return;
        }}

        state.selectedProvince = provName;
        state.selectedStation = null;
        filterProvince.value = provName;

        // UI Updates
        mapBreadcrumbText.textContent = `📍 ภาพรวม > จังหวัด${{provName}}`;
        mapSelectedIndicator.textContent = `จังหวัด${{provName}}`;
        btnMapBack.style.display = 'inline-block';
        statusProvinceBadge.textContent = `จังหวัด${{provName}}`;
        statusStationBadge.textContent = `ทุกสถานีใน${{provName}}`;

        // Smooth Camera Animation
        const pGeo = REAL_DATA.centers[provName];
        if (pGeo) {{
            smoothFlyTo(pGeo.lat, pGeo.lng, pGeo.zoom);
        }}

        // Highlight Station Markers
        highlightMarkersForProvince(provName);

        // Update Charts & KPIs
        updateAllComponents();

        // Open Detail Drawer for Province
        openProvinceDrawer(provName);
    }}

    function selectStation(sta) {{
        state.selectedStation = sta.name;
        state.selectedProvince = sta.province;
        filterProvince.value = sta.province;

        // UI Updates
        mapBreadcrumbText.textContent = `📍 ${{sta.province}} > ${{sta.name}}`;
        mapSelectedIndicator.textContent = sta.name;
        btnMapBack.style.display = 'inline-block';
        statusProvinceBadge.textContent = `จังหวัด${{sta.province}}`;
        statusStationBadge.textContent = sta.name;

        // Smooth Camera Animation to Station
        smoothFlyTo(sta.lat, sta.lng, 11.5);

        // Highlight this marker
        Object.values(stationMarkersMap).forEach(m => {{
            m.setStyle({{ fillColor: '#A778E8', color: '#ffffff', radius: 5, fillOpacity: 0.5 }});
        }});
        if (stationMarkersMap[sta.name]) {{
            stationMarkersMap[sta.name].setStyle({{ fillColor: '#ffffff', color: '#FF8A32', radius: 10, fillOpacity: 1.0 }});
            stationMarkersMap[sta.name].bringToFront();
        }}

        // Update Charts & Drawer
        updateAllComponents();
        openStationDrawer(sta);
    }}

    function resetProvinceView() {{
        state.selectedProvince = 'all';
        state.selectedStation = null;
        filterProvince.value = 'all';

        mapBreadcrumbText.textContent = '📍 ภาพรวม 9 จังหวัด (50 สถานี)';
        mapSelectedIndicator.textContent = 'มุมมอง: ภาพรวม 9 จังหวัด';
        btnMapBack.style.display = 'none';
        statusProvinceBadge.textContent = 'ภาพรวม 9 จังหวัด';
        statusStationBadge.textContent = 'ทุกสถานี (50)';

        // Smooth FlyTo Overview
        smoothFlyTo(overviewCenter[0], overviewCenter[1], overviewZoom);

        // Reset all marker styles
        Object.values(stationMarkersMap).forEach(m => {{
            m.setStyle({{ fillColor: '#FF8A32', color: '#ffffff', radius: 6, fillOpacity: 0.85 }});
        }});

        updateAllComponents();
        closeDrawer();
    }}

    function highlightMarkersForProvince(provName) {{
        Object.entries(stationMarkersMap).forEach(([name, marker]) => {{
            const sta = REAL_DATA.stations.find(s => s.name === name);
            if (sta && sta.province === provName) {{
                marker.setStyle({{ fillColor: '#FF8A32', color: '#ffffff', radius: 8, fillOpacity: 1.0 }});
                marker.bringToFront();
            }} else {{
                marker.setStyle({{ fillColor: '#4a3b63', color: '#6d5a8c', radius: 4, fillOpacity: 0.3 }});
            }}
        }});
    }}

    // -------------------------------------------------------------
    // 3. DETAIL DRAWER CONTROLLER
    // -------------------------------------------------------------
    function openProvinceDrawer(provName) {{
        drawerTitleText.textContent = `ข้อมูลจังหวัด${{provName}}`;
        const stationsInProv = REAL_DATA.stations.filter(s => s.province === provName);
        const tambonsInProv = REAL_DATA.tambons.filter(t => t.province_name === provName);
        const provChange = REAL_DATA.province_changes.find(p => p.province_name === provName);

        let html = `
            <div style="background:rgba(255,138,50,0.12); border-left:3px solid var(--primary-orange); padding:0.8rem; border-radius:6px; margin-bottom:1rem;">
                <strong style="color:var(--primary-orange);">🏔️ สรุปข้อมูลภูมิอากาศในจังหวัด${{provName}}</strong>
                <div style="font-size:0.78rem; margin-top:0.3rem; color:#f0e6fc;">
                    ค่าเฉลี่ยสถานีบนพื้นที่สูง (ไม่ใช่ค่าเฉลี่ยทั้งจังหวัด)
                </div>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">จำนวนสถานีตรวจวัด:</span>
                <span class="drawer-metric-val">${{stationsInProv.length}} สถานี</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ตำบลในกลุ่มตัวอย่างข้าว:</span>
                <span class="drawer-metric-val">${{tambonsInProv.length > 0 ? tambonsInProv.length + ' ตำบล' : 'ไม่มีข้อมูลในกลุ่ม 5 จังหวัด'}}</span>
            </div>
        `;

        if (provChange) {{
            html += `
                <div class="drawer-metric-row">
                    <span class="drawer-metric-label">Δ ผลผลิตเฉลี่ย (2023-2022):</span>
                    <span class="drawer-metric-val" style="color:${{provChange.mean_yield_change >= 0 ? '#4ade80' : '#f87171'}};">
                        ${{provChange.mean_yield_change >= 0 ? '+' : ''}}${{provChange.mean_yield_change}}
                    </span>
                </div>
                <div class="drawer-metric-row">
                    <span class="drawer-metric-label">Δ ฝน HRDI เฉลี่ย:</span>
                    <span class="drawer-metric-val" style="color:#f87171;">${{provChange.mean_hrdi_change}} mm</span>
                </div>
                <div class="drawer-metric-row">
                    <span class="drawer-metric-label">Δ ฝน HII จังหวัด:</span>
                    <span class="drawer-metric-val" style="color:#f87171;">${{provChange.hii_change}} mm</span>
                </div>
            `;
        }}

        html += `
            <div style="margin-top:1.25rem;">
                <strong style="font-size:0.85rem; color:var(--primary-orange);">📍 รายชื่อสถานีตรวจวัดในจังหวัด:</strong>
                <ul style="padding-left:1.2rem; margin-top:0.4rem; font-size:0.8rem; line-height:1.6;">
                    ${{stationsInProv.map(s => `<li><a href="javascript:void(0)" onclick="selectStationByName('${{s.name}}')" style="color:#FFA55C; text-decoration:none;">${{s.name}}</a> (${{s.amphoe}})</li>`).join('')}}
                </ul>
            </div>
        `;

        drawerBodyContent.innerHTML = html;
        detailDrawer.classList.add('open');
        state.isDrawerOpen = true;
    }}

    function openStationDrawer(sta) {{
        drawerTitleText.textContent = sta.name;
        drawerBodyContent.innerHTML = `
            <div style="background:rgba(167,120,232,0.12); border-left:3px solid var(--secondary-lavender); padding:0.8rem; border-radius:6px; margin-bottom:1rem;">
                <strong style="color:var(--secondary-lavender);">🛰️ สถานีตรวจวัดสภาพอากาศ</strong>
                <div style="font-size:0.78rem; margin-top:0.3rem; color:#f0e6fc;">
                    พิกัดจริง: Lat ${{sta.lat}}, Long ${{sta.lng}}
                </div>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">จังหวัด / อำเภอ / ตำบล:</span>
                <span class="drawer-metric-val">${{sta.province}} / ${{sta.amphoe}} / ${{sta.tambon}}</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ประเภทแหล่งข้อมูล:</span>
                <span class="drawer-metric-val">${{sta.source === 'HRDI' ? 'สถานีโครงการหลวง (HRDI)' : 'แบบจำลอง OpenWeatherMap (OWM)'}}</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">จำนวนเดือนที่มีข้อมูล:</span>
                <span class="drawer-metric-val">${{sta.records}} / 24 เดือน</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ปริมาณฝนเฉลี่ยรายเดือน:</span>
                <span class="drawer-metric-val" style="color:var(--primary-orange);">${{sta.mean_rain}} mm (รอยืนยัน)</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">อุณหภูมิเฉลี่ย:</span>
                <span class="drawer-metric-val">${{sta.mean_temp}} °C</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ความชื้นสัมพัทธ์:</span>
                <span class="drawer-metric-val">${{sta.mean_humidity}} %</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ความเร็วลมเฉลี่ย:</span>
                <span class="drawer-metric-val">${{sta.mean_wind}} m/s</span>
            </div>
        `;
        detailDrawer.classList.add('open');
        state.isDrawerOpen = true;
    }}

    function openTambonDrawer(tambon) {{
        drawerTitleText.textContent = `ตำบล${{tambon.tambon_name}}`;
        drawerBodyContent.innerHTML = `
            <div style="background:rgba(56,189,248,0.12); border-left:3px solid var(--accent-cyan); padding:0.8rem; border-radius:6px; margin-bottom:1rem;">
                <strong style="color:var(--accent-cyan);">🌾 กลุ่มตัวอย่างข้าวนาปี (Balanced Panel)</strong>
                <div style="font-size:0.78rem; margin-top:0.3rem; color:#f0e6fc;">
                    รหัส 6 หลัก: <strong>${{tambon.tambon_code_6}}</strong> • ผ่านเกณฑ์จับคู่ 100%
                </div>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">อำเภอ / จังหวัด:</span>
                <span class="drawer-metric-val">${{tambon.amphoe_name}} / ${{tambon.province_name}}</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ผลผลิตข้าวปี 2022:</span>
                <span class="drawer-metric-val">${{tambon.yield_2022}} (รอยืนยัน)</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ผลผลิตข้าวปี 2023:</span>
                <span class="drawer-metric-val">${{tambon.yield_2023}} (รอยืนยัน)</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">การเปลี่ยนแปลงผลผลิต:</span>
                <span class="drawer-metric-val" style="color:${{tambon.delta_yield >= 0 ? '#4ade80' : '#f87171'}};">
                    ${{tambon.delta_yield >= 0 ? '+' : ''}}${{tambon.delta_yield}} (${{tambon.direction}})
                </span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ฝน HRDI (ก.พ.–ก.ค. 2022):</span>
                <span class="drawer-metric-val">${{tambon.hrdi_2022}} mm</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">ฝน HRDI (ก.พ.–ก.ค. 2023):</span>
                <span class="drawer-metric-val">${{tambon.hrdi_2023}} mm</span>
            </div>
            <div class="drawer-metric-row">
                <span class="drawer-metric-label">Δ ฝน HRDI (2023 - 2022):</span>
                <span class="drawer-metric-val" style="color:#f87171;">${{tambon.delta_hrdi}} mm (ลดลง)</span>
            </div>
        `;
        detailDrawer.classList.add('open');
        state.isDrawerOpen = true;
    }}

    function closeDrawer() {{
        detailDrawer.classList.remove('open');
        state.isDrawerOpen = false;
    }}

    btnDrawerClose.addEventListener('click', closeDrawer);
    btnMapBack.addEventListener('click', resetProvinceView);
    btnResetMap.addEventListener('click', resetProvinceView);

    window.selectStationByName = function(name) {{
        const sta = REAL_DATA.stations.find(s => s.name === name);
        if (sta) selectStation(sta);
    }};

    window.selectTambonByCode = function(code) {{
        const t = REAL_DATA.tambons.find(item => item.tambon_code_6 === code);
        if (t) openTambonDrawer(t);
    }};

    // -------------------------------------------------------------
    // 4. CHART BUILDERS (CHART.JS HALLOWEEN THEME)
    // -------------------------------------------------------------
    const chartDefaults = {{
        color: '#A59DB5',
        borderColor: 'rgba(255, 138, 50, 0.15)',
        font: {{ family: "'Prompt', sans-serif", size: 11 }}
    }};
    Chart.defaults.color = chartDefaults.color;
    Chart.defaults.borderColor = chartDefaults.borderColor;
    Chart.defaults.font.family = chartDefaults.font.family;

    function renderMonthlyTrendChart() {{
        const ctx = document.getElementById('chartMonthlyTrend').getContext('2d');
        if (chartTrend) chartTrend.destroy();

        // กรองข้อมูลตามจังหวัดและปี
        let filteredTrends = REAL_DATA.monthly_trends;
        if (state.selectedProvince !== 'all') {{
            filteredTrends = filteredTrends.filter(t => t.province === state.selectedProvince);
        }}
        if (state.selectedYear !== 'all') {{
            filteredTrends = filteredTrends.filter(t => t.year_month.startsWith(state.selectedYear));
        }}

        // กรุ๊ปตาม year_month
        const months = [...new Set(filteredTrends.map(t => t.year_month))].sort();
        const rainData = [];
        const tempData = [];

        months.forEach(m => {{
            const items = filteredTrends.filter(t => t.year_month === m);
            const rains = items.map(i => i.mean_rain).filter(v => v !== null);
            const temps = items.map(i => i.mean_temp).filter(v => v !== null);
            rainData.push(rains.length ? (rains.reduce((a,b)=>a+b,0)/rains.length).toFixed(1) : null);
            tempData.push(temps.length ? (temps.reduce((a,b)=>a+b,0)/temps.length).toFixed(1) : null);
        }});

        chartTrend = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'ปริมาณฝนเฉลี่ย (mm รอยืนยัน)',
                        data: rainData,
                        borderColor: '#FF8A32',
                        backgroundColor: 'rgba(255, 138, 50, 0.15)',
                        fill: true,
                        tension: 0.35,
                        yAxisID: 'yRain',
                        pointBackgroundColor: '#FF8A32',
                        pointHoverRadius: 6
                    }},
                    {{
                        label: 'อุณหภูมิเฉลี่ย (°C)',
                        data: tempData,
                        borderColor: '#A778E8',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5],
                        tension: 0.3,
                        yAxisID: 'yTemp',
                        pointBackgroundColor: '#A778E8',
                        pointHoverRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{ mode: 'index', intersect: false }},
                scales: {{
                    x: {{ ticks: {{ maxRotation: 45 }} }},
                    yRain: {{
                        type: 'linear',
                        position: 'left',
                        title: {{ display: true, text: 'ฝน (mm)', color: '#FF8A32' }},
                        grid: {{ color: 'rgba(255, 138, 50, 0.08)' }}
                    }},
                    yTemp: {{
                        type: 'linear',
                        position: 'right',
                        title: {{ display: true, text: 'อุณหภูมิ (°C)', color: '#A778E8' }},
                        grid: {{ drawOnChartArea: false }}
                    }}
                }},
                plugins: {{
                    legend: {{ position: 'top', labels: {{ usePointStyle: true }} }}
                }}
            }}
        }});
    }}

    function renderStationCompareChart() {{
        const ctx = document.getElementById('chartStationCompare').getContext('2d');
        if (chartStation) chartStation.destroy();

        let filteredStations = REAL_DATA.stations;
        if (state.selectedProvince !== 'all') {{
            filteredStations = filteredStations.filter(s => s.province === state.selectedProvince);
        }}
        // แสดงสูงสุด 15 สถานี
        filteredStations = filteredStations.slice(0, 15);

        const labels = filteredStations.map(s => s.name.replace('สถานีตรวจวัดสภาพอากาศ', ''));
        const rainVals = filteredStations.map(s => s.mean_rain);
        const tempVals = filteredStations.map(s => s.mean_temp);

        chartStation = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [{{
                    label: 'ปริมาณฝนเฉลี่ยรายสถานี (mm)',
                    data: rainVals,
                    backgroundColor: filteredStations.map(s => s.name === state.selectedStation ? '#ffffff' : '#FF8A32'),
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                onClick: (evt, elements) => {{
                    if (elements.length > 0) {{
                        const idx = elements[0].index;
                        selectStation(filteredStations[idx]);
                    }}
                }},
                scales: {{
                    x: {{ title: {{ display: true, text: 'ฝนเฉลี่ย (mm)' }} }}
                }},
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            afterBody: (context) => {{
                                const s = filteredStations[context[0].dataIndex];
                                return `จังหวัด: ${{s.province}}\\nอุณหภูมิ: ${{s.mean_temp}} °C\\nคลิกเพื่อซูมแผนที่`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
    }}

    function renderRainComparePageCharts() {{
        // Chart Rain Compare (HRDI vs HII)
        const ctx1 = document.getElementById('chartRainCompare').getContext('2d');
        if (chartRainComp) chartRainComp.destroy();

        const provNames = REAL_DATA.province_changes.map(p => p.province_name);
        const hrdiDeltas = REAL_DATA.province_changes.map(p => p.mean_hrdi_change);
        const hiiDeltas = REAL_DATA.province_changes.map(p => p.hii_change);

        chartRainComp = new Chart(ctx1, {{
            type: 'bar',
            data: {{
                labels: provNames,
                datasets: [
                    {{
                        label: 'Δ ฝน HRDI (สถานีในตำบล) [mm]',
                        data: hrdiDeltas,
                        backgroundColor: '#FF8A32',
                        borderRadius: 6
                    }},
                    {{
                        label: 'Δ ฝน HII (สสน. ระดับจังหวัด) [mm]',
                        data: hiiDeltas,
                        backgroundColor: '#A778E8',
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{ title: {{ display: true, text: 'การเปลี่ยนแปลงฝน ก.พ.–ก.ค. (2023 ลบ 2022)' }} }}
                }},
                plugins: {{
                    legend: {{ position: 'top' }}
                }}
            }}
        }});

        // HRDI Delta
        const ctx2 = document.getElementById('chartHrdiDeltaProv').getContext('2d');
        if (chartHrdiDelta) chartHrdiDelta.destroy();
        chartHrdiDelta = new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: provNames,
                datasets: [{{
                    label: 'Δ ฝน HRDI เฉลี่ย (mm)',
                    data: hrdiDeltas,
                    backgroundColor: '#FF8A32',
                    borderRadius: 6
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        // HII Delta
        const ctx3 = document.getElementById('chartHiiDeltaProv').getContext('2d');
        if (chartHiiDelta) chartHiiDelta.destroy();
        chartHiiDelta = new Chart(ctx3, {{
            type: 'bar',
            data: {{
                labels: provNames,
                datasets: [{{
                    label: 'Δ ฝน HII จังหวัด (mm)',
                    data: hiiDeltas,
                    backgroundColor: '#A778E8',
                    borderRadius: 6
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});
    }}

    function renderRiceYieldPageCharts() {{
        const ctx = document.getElementById('chartRiceSlope').getContext('2d');
        if (chartRiceSlope) chartRiceSlope.destroy();

        let filteredTambons = REAL_DATA.tambons;
        if (state.selectedProvince !== 'all') {{
            filteredTambons = filteredTambons.filter(t => t.province_name === state.selectedProvince);
        }}

        const labels = filteredTambons.map(t => t.tambon_name);
        const y22 = filteredTambons.map(t => t.yield_2022);
        const y23 = filteredTambons.map(t => t.yield_2023);

        chartRiceSlope = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'ผลผลิตปี 2022',
                        data: y22,
                        backgroundColor: 'rgba(167, 120, 232, 0.7)',
                        borderRadius: 4
                    }},
                    {{
                        label: 'ผลผลิตปี 2023',
                        data: y23,
                        backgroundColor: 'rgba(255, 138, 50, 0.85)',
                        borderRadius: 4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                onClick: (evt, elements) => {{
                    if (elements.length > 0) {{
                        const idx = elements[0].index;
                        openTambonDrawer(filteredTambons[idx]);
                    }}
                }},
                scales: {{
                    y: {{ title: {{ display: true, text: 'ผลผลิตต่อพื้นที่เก็บเกี่ยว (หน่วยรอยืนยัน)' }} }}
                }},
                plugins: {{
                    legend: {{ position: 'top' }}
                }}
            }}
        }});

        populateTambonTable(filteredTambons);
    }}

    function populateTambonTable(tambons) {{
        const tbody = document.getElementById('tambonTableBody');
        tbody.innerHTML = '';
        tambons.forEach(t => {{
            const tr = document.createElement('tr');
            const dColor = t.delta_yield > 0 ? '#4ade80' : (t.delta_yield < 0 ? '#f87171' : '#A59DB5');
            tr.innerHTML = `
                <td><code>${{t.tambon_code_6}}</code></td>
                <td><strong>${{t.tambon_name}}</strong></td>
                <td>${{t.amphoe_name}}</td>
                <td>${{t.province_name}}</td>
                <td>${{t.yield_2022}}</td>
                <td>${{t.yield_2023}}</td>
                <td style="color:${{dColor}}; font-weight:600;">${{t.delta_yield > 0 ? '+' : ''}}${{t.delta_yield}}</td>
                <td>${{t.hrdi_2022}}</td>
                <td>${{t.hrdi_2023}}</td>
                <td style="color:#f87171;">${{t.delta_hrdi}}</td>
            `;
            tr.addEventListener('click', () => openTambonDrawer(t));
            tbody.appendChild(tr);
        }});
    }}

    function renderCorrelationPageCharts() {{
        // Scatter Tambon (n=25)
        const ctx1 = document.getElementById('chartScatterTambon').getContext('2d');
        if (chartScatterTambon) chartScatterTambon.destroy();

        const scatterData = REAL_DATA.tambons.map(t => ({{
            x: t.delta_hrdi,
            y: t.delta_yield,
            tambon: t
        }}));

        chartScatterTambon = new Chart(ctx1, {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'ตำบลใน Balanced Panel (n=25)',
                    data: scatterData,
                    backgroundColor: '#FF8A32',
                    borderColor: '#ffffff',
                    borderWidth: 1.5,
                    pointRadius: 6,
                    pointHoverRadius: 9
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                onClick: (evt, elements) => {{
                    if (elements.length > 0) {{
                        const idx = elements[0].index;
                        openTambonDrawer(scatterData[idx].tambon);
                    }}
                }},
                scales: {{
                    x: {{ title: {{ display: true, text: 'Δ ฝน HRDI (2023 ลบ 2022) [mm]' }} }},
                    y: {{ title: {{ display: true, text: 'Δ ผลผลิตข้าวนาปี (2023 ลบ 2022)' }} }}
                }},
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: (context) => {{
                                const t = context.raw.tambon;
                                return `${{t.label}}: Δฝน=${{t.delta_hrdi}}, Δผลผลิต=${{t.delta_yield}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Scatter Province (n=5)
        const ctx2 = document.getElementById('chartScatterProvince').getContext('2d');
        if (chartScatterProvince) chartScatterProvince.destroy();

        const provScatterData = REAL_DATA.province_changes.map(p => ({{
            x: p.mean_hrdi_change,
            y: p.mean_yield_change,
            prov: p
        }}));

        chartScatterProvince = new Chart(ctx2, {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'ระดับจังหวัด (n=5)',
                    data: provScatterData,
                    backgroundColor: '#A778E8',
                    borderColor: '#ffffff',
                    borderWidth: 2,
                    pointRadius: 9,
                    pointHoverRadius: 12
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Δ ฝน HRDI เฉลี่ยระดับจังหวัด (mm)' }} }},
                    y: {{ title: {{ display: true, text: 'Δ ผลผลิตเฉลี่ยของตำบลในจังหวัด' }} }}
                }},
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: (context) => {{
                                const p = context.raw.prov;
                                return `จังหวัด${{p.province_name}}: Δฝน=${{p.mean_hrdi_change}}, Δผลผลิต=${{p.mean_yield_change}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
    }}

    // -------------------------------------------------------------
    // 5. UPDATE ALL COMPONENTS (KPIs + CHARTS)
    // -------------------------------------------------------------
    function updateAllComponents() {{
        // Filter stations
        let fStations = REAL_DATA.stations;
        if (state.selectedProvince !== 'all') {{
            fStations = fStations.filter(s => s.province === state.selectedProvince);
        }}

        // Update KPIs
        if (fStations.length > 0) {{
            const avgRain = (fStations.reduce((a,s)=>a+s.mean_rain,0)/fStations.length).toFixed(1);
            const avgTemp = (fStations.reduce((a,s)=>a+s.mean_temp,0)/fStations.length).toFixed(1);
            const avgHum = (fStations.reduce((a,s)=>a+s.mean_humidity,0)/fStations.length).toFixed(1);
            const avgWind = (fStations.reduce((a,s)=>a+s.mean_wind,0)/fStations.length).toFixed(2);

            document.getElementById('kpiRainVal').textContent = avgRain;
            document.getElementById('kpiTempVal').textContent = avgTemp + ' °C';
            document.getElementById('kpiHumidityVal').textContent = avgHum + ' %';
            document.getElementById('kpiWindVal').textContent = avgWind + ' m/s';
        }}

        renderMonthlyTrendChart();
        renderStationCompareChart();
        renderRainComparePageCharts();
        renderRiceYieldPageCharts();
        renderCorrelationPageCharts();
    }}

    // -------------------------------------------------------------
    // 6. EVENT LISTENERS
    // -------------------------------------------------------------
    navTabs.forEach(tab => {{
        tab.addEventListener('click', () => {{
            navTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const targetPageId = tab.getAttribute('data-tab');
            pageViews.forEach(pv => pv.classList.remove('active'));
            const targetPage = document.getElementById(targetPageId);
            if (targetPage) targetPage.classList.add('active');

            state.activeTab = targetPageId;

            // Trigger map resize if page 1
            if (targetPageId === 'page1') {{
                setTimeout(() => map.invalidateSize(), 150);
            }}
        }});
    }});

    filterProvince.addEventListener('change', (e) => {{
        if (e.target.value === 'all') {{
            resetProvinceView();
        }} else {{
            selectProvince(e.target.value);
        }}
    }});

    filterYear.addEventListener('change', (e) => {{
        state.selectedYear = e.target.value;
        statusYearBadge.textContent = e.target.value === 'all' ? '2022–2023' : 'ปี ' + e.target.value;
        updateAllComponents();
    }});

    btnResetAll.addEventListener('click', () => {{
        filterYear.value = 'all';
        state.selectedYear = 'all';
        statusYearBadge.textContent = '2022–2023';
        resetProvinceView();
    }});

    // Table search
    const searchTambonInput = document.getElementById('searchTambonInput');
    searchTambonInput.addEventListener('input', (e) => {{
        const q = e.target.value.toLowerCase().trim();
        let list = REAL_DATA.tambons;
        if (state.selectedProvince !== 'all') {{
            list = list.filter(t => t.province_name === state.selectedProvince);
        }}
        if (q) {{
            list = list.filter(t => 
                t.tambon_name.toLowerCase().includes(q) ||
                t.amphoe_name.toLowerCase().includes(q) ||
                t.province_name.toLowerCase().includes(q) ||
                t.tambon_code_6.includes(q)
            );
        }}
        populateTambonTable(list);
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
