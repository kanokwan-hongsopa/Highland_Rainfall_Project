# -*- coding: utf-8 -*-
"""
Script to apply Province Insights & Rain-Rice Relationship upgrades to dashboard/halloween_app.py
"""

from pathlib import Path
import re

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------------------
# 1. ADD CSS FOR INSIGHT CARDS & SCATTER PLOT
# -------------------------------------------------------------------------
insights_css = """
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
"""

if ".insight-cards-grid" not in content:
    target_css_end = "        .hrdi-mode-status-banner .banner-icon {{\n            font-size: 1.1rem;\n            flex-shrink: 0;\n        }}\n    </style>"
    if target_css_end in content:
        content = content.replace(target_css_end, "        .hrdi-mode-status-banner .banner-icon {{\n            font-size: 1.1rem;\n            flex-shrink: 0;\n        }}\n" + insights_css + "\n    </style>")
        print("[SUCCESS] Added Insight Cards and Scatter Plot CSS")
    else:
        print("[WARNING] Could not match target_css_end for insights_css")

# -------------------------------------------------------------------------
# 2. UPDATE HTML: REPLACE TOP 4 SECTION & ADD SCATTER PLOT
# -------------------------------------------------------------------------
old_highlights_html = """            <!-- PROVINCE HIGHLIGHTS SECTION (TOP 4 PROVINCES + FULL RANKING DRAWER) -->
            <div class="province-highlights-section">
                <div class="section-title-row">
                    <div class="section-title-left">
                        <span class="section-badge-icon">🏆</span>
                        <span class="section-title-text">จังหวัดฝนสะสมสูงสุด 4 อันดับแรก (พื้นที่สูง)</span>
                        <span class="section-subtitle-tag">💡 คลิกการ์ดเพื่อซูมแผนที่ & กรองข้อมูล</span>
                    </div>
                    <button class="btn-view-all-ranking" id="btnToggleAllRankings">
                        <span>📊</span> ดูอันดับทั้งหมด 9 จังหวัด <span id="rankToggleArrow">▼</span>
                    </button>
                </div>

                <!-- Top 4 Cards Grid -->
                <div class="top4-cards-grid" id="top4CardsContainer">
                    <!-- Populated dynamically -->
                </div>

                <!-- Collapsible Full 9 Provinces Ranking Panel -->
                <div class="all-ranking-drawer" id="allRankingDrawer" style="display:none; margin-top: 0.75rem; background: rgba(14, 7, 27, 0.6); padding: 1.15rem; border-radius: 12px; border: 1px solid rgba(167, 120, 232, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: #ffffff; font-size: 0.95rem;">📊 อันดับปริมาณฝนสะสมเฉลี่ยครบทั้ง 9 จังหวัดบนพื้นที่สูง</strong>
                        <span style="font-size: 0.76rem; color: var(--text-muted);">คลิกแท่งกราฟเพื่อเลือกจังหวัด</span>
                    </div>
                    <div class="chart-canvas-container" style="height: 220px;">
                        <canvas id="chartProvinceRank"></canvas>
                    </div>
                </div>
            </div>"""

new_highlights_html = """            <!-- PROVINCE INSIGHTS & RANKINGS (UNDER MAIN MAP) -->
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
            </div>"""

if old_highlights_html in content:
    content = content.replace(old_highlights_html, new_highlights_html, 1)
    print("[SUCCESS] Replaced Highlights HTML with 6 Insight Cards & Scatter Plot Section")
else:
    print("[WARNING] Could not match old_highlights_html")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] Step 1 & 2 saved.")
