# -*- coding: utf-8 -*-
"""
Script to apply Exploratory & Observed JS logic upgrades to dashboard/halloween_app.py
"""

from pathlib import Path
import re

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update state object: Add hrdiMode: 'observed'
old_state = """        const state = {{
            activeTab: 'page1',
            tab1: {{"""

new_state = """        const state = {{
            activeTab: 'page1',
            hrdiMode: 'observed', // 'observed' | 'exploratory'
            tab1: {{"""

if old_state in content:
    content = content.replace(old_state, new_state, 1)
    print("[SUCCESS] Added hrdiMode to state")

# 2. Add setHrdiMode and event listeners right after state declaration
target_after_state = """            selectedMarker: null,
            isDrawerOpen: false
        }};"""

mode_js_block = """            selectedMarker: null,
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
        if (btnModeExploratory) btnModeExploratory.addEventListener('click', () => window.setHrdiMode('exploratory'));"""

if "window.setHrdiMode" not in content and target_after_state in content:
    content = content.replace(target_after_state, mode_js_block, 1)
    print("[SUCCESS] Added setHrdiMode and event listeners")

# 3. Update updateTab1Components
old_update_tab1 = """        function updateTab1Components() {{
            const p = state.tab1.province;
            const yr = state.tab1.year;
            const sta = state.tab1.station;
            const tCode = state.tab1.tambon || 'all';

            // Compute KPIs
            let rainVal = REAL_DATA.overall_kpis.mean_rain;
            let tempVal = REAL_DATA.overall_kpis.mean_temp;
            let humVal = REAL_DATA.overall_kpis.mean_humidity;
            let windVal = REAL_DATA.overall_kpis.mean_wind;
            let yieldVal = REAL_DATA.overall_kpis.mean_yield;

            if (p !== 'all') {{
                const sum = REAL_DATA.province_summaries[p];
                if (sum) {{
                    rainVal = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                    tempVal = sum.temp;
                    humVal = sum.humidity;
                    windVal = sum.wind || 2.4;
                    yieldVal = (yr === '2022') ? (sum.rice_yield_2022 || yieldVal) : (yr === '2023') ? (sum.rice_yield_2023 || yieldVal) : (((sum.rice_yield_2022 || yieldVal) + (sum.rice_yield_2023 || yieldVal)) / 2);
                }}
            }}

            if (sta !== 'all') {{
                const s = REAL_DATA.stations.find(x => x.name === sta);
                if (s) {{
                    rainVal = s.mean_rain;
                    tempVal = s.mean_temp;
                    humVal = s.mean_humidity;
                    windVal = s.mean_wind || 2.5;
                }}
            }}"""

new_update_tab1 = """        function updateTab1Components() {{
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
                        rainSub = `⚠️ รวมค่าประมาณการวิจัย (${s.estimated_count_total + s.exploratory_count_total} ด.)`;
                    }} else {{
                        if (yr === '2022') {{
                            if (s.annual_obs_2022 !== null) {{
                                rainVal = s.annual_obs_2022;
                                rainBadge = '✓ 12/12 ด.';
                                rainSub = '✓ ข้อมูลตรวจวัดจริงครบ 12 เดือน';
                            }} else {{
                                rainVal = null;
                                rainBadge = '⚠️ ข้อมูลไม่ครบ';
                                rainSub = `ตรวจวัดได้ ${s.observed_count_2022}/12 ด. (ห้ามคำนวณผลรวมทั้งปี)`;
                            }}
                        }} else if (yr === '2023') {{
                            rainVal = null;
                            rainBadge = '⚠️ ข้อมูลไม่ครบ';
                            rainSub = `ตรวจวัดได้ ${s.observed_count_2023}/12 ด. (ห้ามคำนวณผลรวมทั้งปี)`;
                        }} else {{
                            rainVal = null;
                            rainBadge = '⚠️ 2023 ไม่ครบ';
                            rainSub = `ตรวจวัดจริง ${s.observed_count_total}/24 ด. (ห้ามรวมยอดปี 2023)`;
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
            }}"""

if old_update_tab1 in content:
    content = content.replace(old_update_tab1, new_update_tab1, 1)
    print("[SUCCESS] Updated updateTab1Components KPI calculation")

# Update count-up call for rain in updateTab1Components
old_rain_render = """            // Animate Count-up numbers (0.8–1.0s)
            animateCountUp(document.getElementById('tab1_kpiRain'), rainVal, 900, 1);"""

new_rain_render = """            // Animate Count-up numbers (0.8–1.0s)
            const rainEl = document.getElementById('tab1_kpiRain');
            const rainBadgeEl = document.getElementById('tab1_kpiRainBadge');
            const rainSubEl = document.getElementById('tab1_kpiRainSub');

            if (rainBadgeEl) rainBadgeEl.textContent = rainBadge;
            if (rainSubEl) rainSubEl.textContent = rainSub;

            if (rainVal === null || isNaN(rainVal)) {
                if (rainEl) rainEl.textContent = 'ไม่ครบ 12 ด.';
            } else {
                animateCountUp(rainEl, rainVal, 900, 1);
            }"""

if old_rain_render in content:
    content = content.replace(old_rain_render, new_rain_render, 1)
    print("[SUCCESS] Updated Tab 1 Rain KPI element rendering")

# 4. Update renderTab1MonthlyTrendChart
old_monthly_trend = """            if (sta !== 'all') {{
                const s = REAL_DATA.stations.find(x => x.name === sta);
                if (s) {{
                    scopeLabel = `สถานี: ${{s.name}} (${{s.province}}) [${{s.data_status_label}}]`;
                    d22 = s.monthly_rain_2022 || [];
                    d23 = s.monthly_rain_2023 || [];
                }} else {{
                    showChartEmptyState('chartMonthlyRainTrend', 'ไม่พบข้อมูลสถานี', 'ไม่พบประวัติข้อมูลน้ำฝนสำหรับสถานีที่เลือก', 'HRDI: ไม่มีข้อมูล');
                    return;
                }}
            }} else if (p !== 'all') {{
                scopeLabel = `จังหวัด: ${{p}} (HII ฝนเฉลี่ยพื้นที่)`;
                const pTrends = REAL_DATA.monthly_trends.filter(m => m.province === p);
                d22 = months.map((_, i) => {{
                    const ym = `2022-${{String(i + 1).padStart(2, '0')}}`;
                    const it = pTrends.find(m => m.year_month === ym);
                    return it ? it.mean_rain : 0;
                }});
                d23 = months.map((_, i) => {{
                    const ym = `2023-${{String(i + 1).padStart(2, '0')}}`;
                    const it = pTrends.find(m => m.year_month === ym);
                    return it ? it.mean_rain : 0;
                }});
            }}"""

new_monthly_trend = """            const isExp = (state.hrdiMode === 'exploratory');
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
            }}"""

if old_monthly_trend in content:
    content = content.replace(old_monthly_trend, new_monthly_trend, 1)
    print("[SUCCESS] Updated renderTab1MonthlyTrendChart data selection")

# Also add spanGaps: false to monthly trend chart options
old_span_gaps = """                    fill: true,
                    tension: 0.35,
                    pointRadius: 4
                }});"""

new_span_gaps = """                    fill: true,
                    tension: 0.35,
                    pointRadius: 4,
                    spanGaps: false
                }});"""

if old_span_gaps in content:
    content = content.replace(old_span_gaps, new_span_gaps)
    print("[SUCCESS] Added spanGaps: false to datasets")

# 5. Update renderTab1RainCompareChart
old_rain_compare = """            provNames.forEach(pr => {{
                const sum = REAL_DATA.province_summaries[pr] || {{}};
                const hrdi = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                const hii = (yr === '2022') ? (sum.hii_rain_2022 || 0) : (yr === '2023') ? (sum.hii_rain_2023 || 0) : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                hrdiData.push(Math.round(hrdi || 0));
                hiiData.push(Math.round(hii || 0));
            }});"""

new_rain_compare = """            const isExp = (state.hrdiMode === 'exploratory');
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
            }}"""

if old_rain_compare in content:
    content = content.replace(old_rain_compare, new_rain_compare, 1)
    print("[SUCCESS] Updated renderTab1RainCompareChart")

# Update label in renderTab1RainCompareChart datasets
old_hrdi_compare_label = "{{ label: 'พื้นที่สูง (HRDI เฉลี่ยสถานี)', data: hrdiData, backgroundColor: '#A778E8', borderRadius: 4 }}"
new_hrdi_compare_label = "{{ label: isExp ? 'พื้นที่สูง (HRDI เติมเต็ม Exploratory)' : 'พื้นที่สูง (HRDI ตรวจวัดจริง)', data: hrdiData, backgroundColor: '#A778E8', borderRadius: 4 }}"

if old_hrdi_compare_label in content:
    content = content.replace(old_hrdi_compare_label, new_hrdi_compare_label, 1)
    print("[SUCCESS] Updated HRDI bar label in comparison chart")

# 6. Update renderTop4HighlightCards and renderTab1ProvinceRankChart
old_top4 = """        function renderTop4HighlightCards() {{
            const container = document.getElementById('top4CardsContainer');
            if (!container) return;
            container.innerHTML = '';

            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;
            const sorted = provs.map(p => {{
                const sum = REAL_DATA.province_summaries[p] || {{}};
                const r = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                return {{ name: p, rain: r, sum: sum }};
            }}).sort((a, b) => b.rain - a.rain);"""

new_top4 = """        function renderTop4HighlightCards() {{
            const container = document.getElementById('top4CardsContainer');
            if (!container) return;
            container.innerHTML = '';

            const isExp = (state.hrdiMode === 'exploratory');
            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;

            if (!isExp && (yr === '2023' || yr === 'all')) {{
                container.innerHTML = `
                    <div style="grid-column: 1 / -1; background: rgba(33, 22, 49, 0.7); border: 1px dashed rgba(167, 120, 232, 0.4); border-radius: 8px; padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.82rem;">
                        <span>🧪 <strong>โหมดตรวจวัดจริง (Observed Only):</strong> ข้อมูลฝนสถานีปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน จึงไม่สามารถจัดอันดับผลรวมทั้งปีได้ <button type="button" onclick="window.setHrdiMode('exploratory')" style="background:var(--primary-orange); color:#fff; border:none; border-radius:4px; padding:2px 8px; cursor:pointer; margin-left:6px; font-size:0.75rem;">🔮 สลับเป็นโหมด Exploratory</button> หรือเลือกตัวกรองปี 2022</span>
                    </div>
                `;
                return;
            }}

            const sorted = provs.map(p => {{
                const sum = REAL_DATA.province_summaries[p] || {{}};
                const r = isExp ? ((yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all)
                               : sum.rain_obs_2022;
                return {{ name: p, rain: r, sum: sum }};
            }}).filter(x => x.rain !== null && !isNaN(x.rain)).sort((a, b) => b.rain - a.rain);"""

if old_top4 in content:
    content = content.replace(old_top4, new_top4, 1)
    print("[SUCCESS] Updated renderTop4HighlightCards")

old_prov_rank = """        function renderTab1ProvinceRankChart() {{
            const canvas = document.getElementById('chartProvinceRank');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (chartProvinceRank) chartProvinceRank.destroy();

            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;
            const provRainPairs = provs.map(p => {{
                const sum = REAL_DATA.province_summaries[p] || {{}};
                const r = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                return {{ name: p, rain: r }};
            }}).sort((a, b) => b.rain - a.rain);"""

new_prov_rank = """        function renderTab1ProvinceRankChart() {{
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
            }}).filter(x => x.rain !== null && !isNaN(x.rain)).sort((a, b) => b.rain - a.rain);"""

if old_prov_rank in content:
    content = content.replace(old_prov_rank, new_prov_rank, 1)
    print("[SUCCESS] Updated renderTab1ProvinceRankChart")

# 7. Update updateTab2Components and renderTab2Charts
old_update_tab2 = """        function updateTab2Components() {{
            const yr = state.tab2.year;
            const p = state.tab2.province;

            let hrdiMean = 1440.4;
            let hiiMean = 1358.5;

            if (p !== 'all') {{
                const sum = REAL_DATA.province_summaries[p];
                if (sum) {{
                    hrdiMean = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                    hiiMean = (yr === '2022') ? sum.hii_rain_2022 : (yr === '2023') ? sum.hii_rain_2023 : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                }}
            }}

            const hrdiEl = document.getElementById('tab2_kpiHrdi');
            const hiiEl = document.getElementById('tab2_kpiHii');
            const diffEl = document.getElementById('tab2_kpiDiff');

            if (hrdiEl) hrdiEl.textContent = (hrdiMean !== null && !isNaN(hrdiMean)) ? hrdiMean.toFixed(1) : 'ไม่มีรายงาน';
            if (hiiEl) hiiEl.textContent = (hiiMean !== null && !isNaN(hiiMean)) ? hiiMean.toFixed(1) : 'ไม่มีรายงาน';
            if (diffEl) {{
                const diff = hrdiMean - hiiMean;
                diffEl.textContent = `${{diff > 0 ? '+' : ''}}${{diff.toFixed(1)}}`;
            }}

            renderTab2Charts();
        }}"""

new_update_tab2 = """        function updateTab2Components() {{
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
        }}"""

if old_update_tab2 in content:
    content = content.replace(old_update_tab2, new_update_tab2, 1)
    print("[SUCCESS] Updated updateTab2Components")

# Update renderTab2Charts
old_tab2_charts_bar = """            provList.forEach(pr => {{
                const s = REAL_DATA.province_summaries[pr] || {{}};
                const hrdi = (yr === '2022') ? s.rain_2022 : (yr === '2023') ? s.rain_2023 : sum.rain_all;
                const hii = (yr === '2022') ? s.hii_rain_2022 : (yr === '2023') ? s.hii_rain_2023 : (((s.hii_rain_2022 || 0) + (s.hii_rain_2023 || 0)) / 2);
                hrdiVals.push(Math.round(hrdi || 0));
                hiiVals.push(Math.round(hii || 0));
            }});"""

new_tab2_charts_bar = """            const isExp = (state.hrdiMode === 'exploratory');
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
            }}"""

if old_tab2_charts_bar in content:
    content = content.replace(old_tab2_charts_bar, new_tab2_charts_bar, 1)
    print("[SUCCESS] Updated Tab 2 Detailed Comparison bar chart")

# Update monthly curves in renderTab2Charts
old_tab2_monthly = """            let hrdi22 = months.map((_, i) => {{
                const vals = pStas.map(s => (s.monthly_rain_2022 && s.monthly_rain_2022[i] !== null && !isNaN(s.monthly_rain_2022[i])) ? s.monthly_rain_2022[i] : null).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
            }});
            let hrdi23 = months.map((_, i) => {{
                const vals = pStas.map(s => (s.monthly_rain_2023 && s.monthly_rain_2023[i] !== null && !isNaN(s.monthly_rain_2023[i])) ? s.monthly_rain_2023[i] : null).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
            }});"""

new_tab2_monthly = """            let hrdi22 = months.map((_, i) => {{
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
            }});"""

if old_tab2_monthly in content:
    content = content.replace(old_tab2_monthly, new_tab2_monthly, 1)
    print("[SUCCESS] Updated Tab 2 Monthly trend curves")

# 8. Update Station Drawer details and Mini Chart
old_drawer_subpanel = """        function openStationDetailSubpanel(s) {{
            document.getElementById('subStaName').textContent = s.name;
            const codeBadge = s.code_ref || s.code_sta || 'HRDI';
            document.getElementById('subStaMeta').textContent = `อ.${{s.amphoe || '-'}} ต.${{s.tambon || '-'}} | รหัส: ${{codeBadge}} (${{s.source}})`;
            document.getElementById('subStaCoords').textContent = `พิกัดจริง: ${{s.lat}}, ${{s.lng}} (WGS84)`;
            document.getElementById('subStaCompleteness').textContent = `ความครบถ้วน: 2022 (${{s.months_2022}}/12 ด.) | 2023 (${{s.months_2023}}/12 ด.) | รวม ${{s.total_months}}/24 เดือน`;

            drawerProvinceView.style.display = 'none';
            drawerStationView.style.display = 'flex';

            renderStationMiniChart(s);
        }}

        function renderStationMiniChart(s) {{
            const ctx = document.getElementById('stationMiniChart').getContext('2d');
            if (miniStationChart) miniStationChart.destroy();

            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            miniStationChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: months,
                    datasets: [
                        {{ label: '2022', data: s.monthly_rain_2022, backgroundColor: '#A778E8', borderRadius: 2 }},
                        {{ label: '2023', data: s.monthly_rain_2023, backgroundColor: '#FF8A32', borderRadius: 2 }}
                    ]
                }},"""

new_drawer_subpanel = """        function openStationDetailSubpanel(s) {{
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
            const d22 = isExp ? s.monthly_exp_2022 : s.monthly_obs_2022;
            const d23 = isExp ? s.monthly_exp_2023 : s.monthly_obs_2023;

            miniStationChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: months,
                    datasets: [
                        {{ label: isExp ? '2022 (Exploratory)' : '2022 (Observed)', data: d22, backgroundColor: '#A778E8', borderRadius: 2 }},
                        {{ label: isExp ? '2023 (Exploratory)' : '2023 (Observed)', data: d23, backgroundColor: '#FF8A32', borderRadius: 2 }}
                    ]
                }},"""

if old_drawer_subpanel in content:
    content = content.replace(old_drawer_subpanel, new_drawer_subpanel, 1)
    print("[SUCCESS] Updated Station Drawer Subpanel and Mini Chart")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] JS logic upgrade saved successfully.")
