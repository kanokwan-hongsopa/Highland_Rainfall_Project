# -*- coding: utf-8 -*-
"""
Script to apply JavaScript for Province Insights & Rain-Rice Relationship in dashboard/halloween_app.py
"""

from pathlib import Path
import re

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update renderTop4HighlightCards and add renderRainRiceScatterPlot
# Let's locate the existing renderTop4HighlightCards function
old_render_top4 = """        function renderTop4HighlightCards() {
            const container = document.getElementById('top4CardsContainer');
            if (!container) return;
            container.innerHTML = '';

            const isExp = (state.hrdiMode === 'exploratory');
            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;

            if (!isExp && (yr === '2023' || yr === 'all')) {
                container.innerHTML = `
                    <div style="grid-column: 1 / -1; background: rgba(33, 22, 49, 0.7); border: 1px dashed rgba(167, 120, 232, 0.4); border-radius: 8px; padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.82rem;">
                        <span>🧪 <strong>โหมดตรวจวัดจริง (Observed Only):</strong> ข้อมูลฝนสถานีปี 2023 ตรวจวัดจริงไม่ครบ 12 เดือน จึงไม่สามารถจัดอันดับผลรวมทั้งปีได้ <button type="button" onclick="window.setHrdiMode('exploratory')" style="background:var(--primary-orange); color:#fff; border:none; border-radius:4px; padding:2px 8px; cursor:pointer; margin-left:6px; font-size:0.75rem;">🔮 สลับเป็นโหมด Exploratory</button> หรือเลือกตัวกรองปี 2022</span>
                    </div>
                `;
                return;
            }

            const sorted = provs.map(p => {
                const sum = REAL_DATA.province_summaries[p] || {};
                const r = isExp ? ((yr === '2022') ? sum.rain_exp_2022 : (yr === '2023') ? sum.rain_exp_2023 : sum.rain_exp_all)
                               : sum.rain_obs_2022;
                return { name: p, rain: r, sum: sum };
            }).filter(x => x.rain !== null && !isNaN(x.rain)).sort((a, b) => b.rain - a.rain);

            const top4 = sorted.slice(0, 4);
            const rankColors = ['#FF8A32', '#FA9A55', '#B777CE', '#A778E8'];

            top4.forEach((item, idx) => {
                const card = document.createElement('div');
                const isSelected = (state.tab1.province === item.name);
                card.className = `highlight-prov-card ${isSelected ? 'active' : ''}`;
                card.innerHTML = `
                    <div class="highlight-prov-top">
                        <span class="highlight-rank-badge" style="background: ${rankColors[idx]}22; color: ${rankColors[idx]}; border: 1px solid ${rankColors[idx]}55;">#${idx + 1}</span>
                        <span class="highlight-prov-name">${item.name}</span>
                        <span class="highlight-sta-count">${item.sum.station_count} สถานี</span>
                    </div>
                    <div class="highlight-prov-body">
                        <div class="highlight-rain-val">${item.rain.toLocaleString()} <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">มม.</span></div>
                        <div class="highlight-sub-stat">🌡️ ${item.sum.temp}°C | 💧 ${item.sum.humidity}%</div>
                    </div>
                    <div class="highlight-prov-footer">
                        <span>${isSelected ? '✓ เลือกอยู่' : 'คลิกเพื่อเลือก 🔍'}</span>
                    </div>
                `;
                card.addEventListener('click', () => {
                    dispatchTab1Filter({ province: item.name });
                });
                container.appendChild(card);
            });
        }"""

# New 6 Insight Cards function with full adherence to requirements
new_insights_and_scatter = """        function renderTop4HighlightCards() {{
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
        }}"""

# Check if old_render_top4 is in content
# Let's use regex or search for function renderTop4HighlightCards
pattern_top4 = r"        function renderTop4HighlightCards\(\) \{.*?\n        \}"
# Find the start of function renderTop4HighlightCards
start_idx = content.find("function renderTop4HighlightCards()")
if start_idx != -1:
    # Find matching closing brace of renderTop4HighlightCards
    # Count braces
    b_count = 0
    end_idx = start_idx
    found_open = False
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            b_count += 1
            found_open = True
        elif content[i] == '}':
            b_count -= 1
            if found_open and b_count == 0:
                end_idx = i + 1
                break
    
    print(f"Found renderTop4HighlightCards from {start_idx} to {end_idx}")
    content = content[:start_idx - 8] + new_insights_and_scatter + content[end_idx:]
    print("[SUCCESS] Replaced renderTop4HighlightCards and added renderRainRiceScatterPlot")
else:
    print("[WARNING] Could not find function renderTop4HighlightCards")

# 2. Add scatterMetricSelect event listener
old_binds = "const btnToggleAllRankings = document.getElementById('btnToggleAllRankings');"
new_binds = """const scatterMetricSelect = document.getElementById('scatterMetricSelect');
        if (scatterMetricSelect) {
            scatterMetricSelect.addEventListener('change', () => renderRainRiceScatterPlot());
        }

        const btnToggleAllRankings = document.getElementById('btnToggleAllRankings');"""

if old_binds in content and "scatterMetricSelect.addEventListener" not in content:
    content = content.replace(old_binds, new_binds, 1)
    print("[SUCCESS] Bound scatterMetricSelect event listener")

# 3. Call renderRainRiceScatterPlot() inside updateTab1Components
old_update_calls = "renderTop4HighlightCards();\n            renderTab1ProvinceRankChart();"
new_update_calls = "renderTop4HighlightCards();\n            renderRainRiceScatterPlot();\n            renderTab1ProvinceRankChart();"

if old_update_calls in content:
    content = content.replace(old_update_calls, new_update_calls, 1)
    print("[SUCCESS] Added renderRainRiceScatterPlot() call to updateTab1Components")

# 4. Enhance renderStationMiniChart to separate Observed, Estimated DEMO, and Estimated Exploratory
old_station_mini = """        function renderStationMiniChart(s) {
            const ctx = document.getElementById('stationMiniChart').getContext('2d');
            if (miniStationChart) miniStationChart.destroy();

            const isExp = (state.hrdiMode === 'exploratory');
            const months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
            const d22 = isExp ? s.monthly_exp_2022 : s.monthly_obs_2022;
            const d23 = isExp ? s.monthly_exp_2023 : s.monthly_obs_2023;

            miniStationChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [
                        { label: isExp ? '2022 (Exploratory)' : '2022 (Observed)', data: d22, backgroundColor: '#A778E8', borderRadius: 2 },
                        { label: isExp ? '2023 (Exploratory)' : '2023 (Observed)', data: d23, backgroundColor: '#FF8A32', borderRadius: 2 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: '#F7F0E8', font: { size: 10 } } },
                        tooltip: { padding: 6 }
                    },
                    scales: {
                        x: { ticks: { color: '#A59DB5', font: { size: 9 } } },
                        y: { ticks: { color: '#A59DB5', font: { size: 9 } } }
                    }
                }
            });
        }"""

new_station_mini = """        function renderStationMiniChart(s) {{
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
        }}"""

start_mini = content.find("function renderStationMiniChart(s)")
if start_mini != -1:
    b_count = 0
    end_mini = start_mini
    found_open = False
    for i in range(start_mini, len(content)):
        if content[i] == '{':
            b_count += 1
            found_open = True
        elif content[i] == '}':
            b_count -= 1
            if found_open and b_count == 0:
                end_mini = i + 1
                break
    print(f"Found renderStationMiniChart from {start_mini} to {end_mini}")
    content = content[:start_mini - 8] + new_station_mini + content[end_mini:]
    print("[SUCCESS] Replaced renderStationMiniChart with color-coded status bar chart")
else:
    print("[WARNING] Could not find function renderStationMiniChart")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] JS upgrades applied successfully.")
