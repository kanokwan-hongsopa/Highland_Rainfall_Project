# -*- coding: utf-8 -*-
"""
Script to apply comprehensive data completeness and empty state upgrades to dashboard/halloween_app.py
"""

import sys
from pathlib import Path

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS: Add .chart-empty-state and badge styling
old_css = """        .chart-canvas-container {{
            position: relative;
            width: 100%;
        }}"""

new_css = """        .chart-canvas-container {{
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
        }}"""

assert old_css in content, "old_css not found"
content = content.replace(old_css, new_css, 1)

# 2. Update Tab 2 Filter HTML
old_tab2_filter = """                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab2_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (5 จังหวัดศึกษา)</option>
                            <option value="เชียงใหม่">เชียงใหม่</option>
                            <option value="น่าน">น่าน</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน</option>
                            <option value="ตาก">ตาก</option>
                            <option value="เชียงราย">เชียงราย</option>
                        </select>
                    </div>"""

new_tab2_filter = """                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab2_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (9 จังหวัด)</option>
                            <option value="เชียงใหม่">เชียงใหม่ (22 สถานี HRDI)</option>
                            <option value="น่าน">น่าน (12 สถานี HRDI)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (5 สถานี HRDI)</option>
                            <option value="ตาก">ตาก (4 สถานี HRDI)</option>
                            <option value="เชียงราย">เชียงราย (3 สถานี HRDI)</option>
                            <option value="กำแพงเพชร">กำแพงเพชร (เฉพาะฝน HII)</option>
                            <option value="พิษณุโลก">พิษณุโลก (เฉพาะฝน HII)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (เฉพาะฝน HII)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (เฉพาะฝน HII)</option>
                        </select>
                    </div>"""

assert old_tab2_filter in content, "old_tab2_filter not found"
content = content.replace(old_tab2_filter, new_tab2_filter, 1)

# 3. Update Tab 3 Filter HTML
old_tab3_filter = """                    <div class="filter-item">
                        <span class="filter-label">📍 จังหวัด</span>
                        <select id="tab3_filterProvince" class="filter-select">
                            <option value="all">ทั้งหมด (5 จังหวัดข้าวนาปี)</option>
                            <option value="เชียงใหม่">เชียงใหม่ (14 ตำบล)</option>
                            <option value="น่าน">น่าน (5 ตำบล)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (3 ตำบล)</option>
                            <option value="ตาก">ตาก (2 ตำบล)</option>
                            <option value="เชียงราย">เชียงราย (1 ตำบล)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">🌿 ตำบล</span>
                        <select id="tab3_filterTambon" class="filter-select">
                            <option value="all">ทั้งหมด (25 ตำบล Balanced Panel)</option>
                        </select>
                    </div>"""

new_tab3_filter = """                    <div class="filter-item">
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
                    </div>"""

assert old_tab3_filter in content, "old_tab3_filter not found"
content = content.replace(old_tab3_filter, new_tab3_filter, 1)

# 4. Update Tab 4 Filter HTML and KPIs
old_tab4_filter = """                    <div class="filter-item">
                        <span class="filter-label">📊 ระดับการวิเคราะห์</span>
                        <select id="tab4_filterLevel" class="filter-select">
                            <option value="tambon">ระดับตำบล Balanced Panel (n=25)</option>
                            <option value="province_hrdi">ระดับจังหวัด HRDI (n=5)</option>
                            <option value="province_hii">ระดับจังหวัด HII (n=5)</option>
                        </select>
                    </div>

                    <div class="filter-item">
                        <span class="filter-label">📍 กรองจังหวัด</span>
                        <select id="tab4_filterProvince" class="filter-select">
                            <option value="all">แสดงทั้งหมด 5 จังหวัด</option>
                            <option value="เชียงใหม่">เชียงใหม่ (14 ตำบล)</option>
                            <option value="น่าน">น่าน (5 ตำบล)</option>
                            <option value="แม่ฮ่องสอน">แม่ฮ่องสอน (3 ตำบล)</option>
                            <option value="ตาก">ตาก (2 ตำบล)</option>
                            <option value="เชียงราย">เชียงราย (1 ตำบล)</option>
                        </select>
                    </div>"""

new_tab4_filter = """                    <div class="filter-item">
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
                            <option value="กำแพงเพชร">กำแพงเพชร (ไม่มีสถานี HRDI)</option>
                            <option value="พิษณุโลก">พิษณุโลก (ไม่มีสถานี HRDI)</option>
                            <option value="เพชรบูรณ์">เพชรบูรณ์ (ไม่มีสถานี HRDI)</option>
                            <option value="กาญจนบุรี">กาญจนบุรี (ไม่มีสถานี HRDI)</option>
                        </select>
                    </div>"""

assert old_tab4_filter in content, "old_tab4_filter not found"
content = content.replace(old_tab4_filter, new_tab4_filter, 1)

# Tab 4 KPIs with dynamic element IDs
old_tab4_kpis = """            <!-- Tab 4 Context KPIs (Spearman Rho) -->
            <div class="kpi-row-grid" style="margin-bottom: 0.95rem;">
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🔗</span><span>Spearman ρ (ตำบล HRDI)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" style="color:var(--primary-orange);">-0.0270</div><span class="kpi-delta-pill" style="background:rgba(234,179,8,0.2); color:#facc15;">p = 0.8979</span></div>
                    <div class="kpi-subtext">n = 25 ตำบล | ไม่พบนัยสำคัญทางสถิติ (พ.ค.–ส.ค.)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🏔️</span><span>Spearman ρ (จังหวัด HRDI)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" style="color:var(--secondary-lavender);">-0.7000</div><span class="kpi-delta-pill" style="background:rgba(167,120,232,0.2); color:#A778E8;">p = 0.1881</span></div>
                    <div class="kpi-subtext">n = 5 จังหวัด | ขนาดตัวอย่างจำกัดมาก (พ.ค.–ส.ค.)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-header"><span class="kpi-icon">🌧️</span><span>Spearman ρ (จังหวัด HII)</span></div>
                    <div class="kpi-main-body"><div class="kpi-number" style="color:var(--accent-cyan);">+0.1000</div><span class="kpi-delta-pill" style="background:rgba(148,163,184,0.2); color:#94a3b8;">p = 0.8729</span></div>
                    <div class="kpi-subtext">n = 5 จังหวัด | ข้อมูลรวมระดับจังหวัด ไม่ใช่จุดเพาะปลูก</div>
                </div>
            </div>"""

new_tab4_kpis = """            <!-- Tab 4 Context KPIs (Spearman Rho) -->
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
            </div>"""

assert old_tab4_kpis in content, "old_tab4_kpis not found"
content = content.replace(old_tab4_kpis, new_tab4_kpis, 1)

# 5. Update JavaScript from Tab 1 cascading through Tab 4
old_js_block_start = """        function animateCountUp(element, endVal, duration = 900, decimals = 1, suffix = '') {{"""
old_js_block_end = """        // LOPO Table Population"""

assert old_js_block_start in content, "old_js_block_start not found"
assert old_js_block_end in content, "old_js_block_end not found"

new_js_block = """        // -------------------------------------------------------------
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
            animateCountUp(document.getElementById('tab1_kpiRain'), rainVal, 900, 1);
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

            if (sta !== 'all') {{
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
                    pointRadius: 4
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
                    pointRadius: 4
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

            // Provinces with HRDI Highland Stations
            const highlandProvs = ['เชียงใหม่', 'น่าน', 'แม่ฮ่องสอน', 'ตาก', 'เชียงราย'];

            if (p !== 'all' && !highlandProvs.includes(p)) {{
                showChartEmptyState('chartTab1RainCompare', 'ไม่มีสถานีตรวจวัด HRDI', `จังหวัด${{p}} ไม่มีสถานีตรวจวัดสภาพอากาศบนพื้นที่สูงของ HRDI (มีเฉพาะข้อมูลฝนระดับจังหวัด HII)`, 'HII Only');
                return;
            }}

            clearChartEmptyState('chartTab1RainCompare');

            const provNames = (p === 'all') ? highlandProvs : [p];
            const hrdiData = [];
            const hiiData = [];

            provNames.forEach(pr => {{
                const sum = REAL_DATA.province_summaries[pr] || {{}};
                const hrdi = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                const hii = (yr === '2022') ? (sum.hii_rain_2022 || 0) : (yr === '2023') ? (sum.hii_rain_2023 || 0) : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                hrdiData.push(Math.round(hrdi || 0));
                hiiData.push(Math.round(hii || 0));
            }});

            chartTab1RainComp = new Chart(canvas.getContext('2d'), {{
                type: 'bar',
                data: {{
                    labels: provNames,
                    datasets: [
                        {{ label: 'พื้นที่สูง (HRDI เฉลี่ยสถานี)', data: hrdiData, backgroundColor: '#A778E8', borderRadius: 4 }},
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

            const provs = Object.keys(REAL_DATA.centers);
            const yr = state.tab1.year;
            const sorted = provs.map(p => {{
                const sum = REAL_DATA.province_summaries[p] || {{}};
                const r = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                return {{ name: p, rain: r, sum: sum }};
            }}).sort((a, b) => b.rain - a.rain);

            const top4 = sorted.slice(0, 4);
            const rankColors = ['#FF8A32', '#FA9A55', '#B777CE', '#A778E8'];

            top4.forEach((item, idx) => {{
                const card = document.createElement('div');
                const isSelected = (state.tab1.province === item.name);
                card.className = `highlight-prov-card ${{isSelected ? 'active' : ''}}`;
                card.innerHTML = `
                    <div class="highlight-prov-top">
                        <span class="highlight-rank-badge" style="background: ${{rankColors[idx]}}22; color: ${{rankColors[idx]}}; border: 1px solid ${{rankColors[idx]}}55;">#${{idx + 1}}</span>
                        <span class="highlight-prov-name">${{item.name}}</span>
                        <span class="highlight-sta-count">${{item.sum.station_count}} สถานี</span>
                    </div>
                    <div class="highlight-prov-body">
                        <div class="highlight-rain-val">${{item.rain.toLocaleString()}} <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">มม.</span></div>
                        <div class="highlight-sub-stat">🌡️ ${{item.sum.temp}}°C | 💧 ${{item.sum.humidity}}%</div>
                    </div>
                    <div class="highlight-prov-footer">
                        <span>${{isSelected ? '✓ เลือกอยู่' : 'คลิกเพื่อเลือก 🔍'}}</span>
                    </div>
                `;
                card.addEventListener('click', () => {{
                    dispatchTab1Filter({{ province: item.name }});
                }});
                container.appendChild(card);
            }});
        }}

        const btnToggleAllRankings = document.getElementById('btnToggleAllRankings');
        const allRankingDrawer = document.getElementById('allRankingDrawer');
        const rankToggleIcon = document.getElementById('rankToggleIcon');
        if (btnToggleAllRankings && allRankingDrawer) {{
            btnToggleAllRankings.addEventListener('click', () => {{
                const isClosed = allRankingDrawer.classList.contains('closed');
                allRankingDrawer.classList.toggle('closed', !isClosed);
                if (rankToggleIcon) rankToggleIcon.textContent = isClosed ? '▲' : '▼';
            }});
        }}

        function renderTab1ProvinceRankChart() {{
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
            }}).sort((a, b) => b.rain - a.rain);

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

            const highlandProvs = ['เชียงใหม่', 'น่าน', 'แม่ฮ่องสอน', 'ตาก', 'เชียงราย'];
            if (p !== 'all' && !highlandProvs.includes(p)) {{
                if (hrdiEl) hrdiEl.textContent = 'ไม่มีสถานี';
                if (hiiEl) hiiEl.textContent = hiiMean.toFixed(1);
                if (diffEl) diffEl.textContent = 'N/A';
            }} else {{
                if (hrdiEl) hrdiEl.textContent = hrdiMean.toFixed(1);
                if (hiiEl) hiiEl.textContent = hiiMean.toFixed(1);
                const diff = hrdiMean - hiiMean;
                if (diffEl) diffEl.textContent = `${{diff > 0 ? '+' : ''}}${{diff.toFixed(1)}}`;
            }}

            renderTab2Charts();
        }}

        function renderTab2Charts() {{
            const canvas1 = document.getElementById('chartDetailedRainComparison');
            if (chartTab2RainComp) chartTab2RainComp.destroy();

            const p = state.tab2.province;
            const src = state.tab2.source;
            const yr = state.tab2.year;
            const highlandProvs = ['เชียงใหม่', 'น่าน', 'แม่ฮ่องสอน', 'ตาก', 'เชียงราย'];

            if (p !== 'all' && src === 'HRDI' && !highlandProvs.includes(p)) {{
                showChartEmptyState('chartDetailedRainComparison', 'ไม่มีสถานีตรวจวัด HRDI', `จังหวัด${{p}} ไม่มีสถานีตรวจวัดสภาพอากาศของ HRDI (มีเฉพาะข้อมูลฝนระดับจังหวัด HII)`, 'HRDI: ไม่มีข้อมูล');
            }} else {{
                clearChartEmptyState('chartDetailedRainComparison');
                const provList = (p === 'all') ? Object.keys(REAL_DATA.province_summaries) : [p];
                const hrdiVals = [];
                const hiiVals = [];

                provList.forEach(pr => {{
                    const s = REAL_DATA.province_summaries[pr] || {{}};
                    const hrdi = (yr === '2022') ? s.rain_2022 : (yr === '2023') ? s.rain_2023 : s.rain_all;
                    const hii = (yr === '2022') ? s.hii_rain_2022 : (yr === '2023') ? s.hii_rain_2023 : (((s.hii_rain_2022 || 0) + (s.hii_rain_2023 || 0)) / 2);
                    hrdiVals.push(highlandProvs.includes(pr) ? Math.round(hrdi || 0) : null);
                    hiiVals.push(Math.round(hii || 0));
                }});

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
            }}

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

            if (p === 'all' || highlandProvs.includes(p)) {{
                let hrdi22 = REAL_DATA.monthly_overall['2022'].map(v => Math.round(v * 0.95));
                let hrdi23 = REAL_DATA.monthly_overall['2023'].map(v => Math.round(v * 0.95));
                datasets2.unshift(
                    {{ label: 'HRDI บนพื้นที่สูง (2022)', data: hrdi22, borderColor: '#A778E8', tension: 0.3 }},
                    {{ label: 'HRDI บนพื้นที่สูง (2023)', data: hrdi23, borderColor: '#FF8A32', tension: 0.3 }}
                );
            }}

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

"""

# Slice out the old block and insert new_js_block
idx_start = content.index(old_js_block_start)
idx_end = content.index(old_js_block_end)

content = content[:idx_start] + new_js_block + content[idx_end:]

# Write back upgraded file
with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] halloween_app.py upgraded successfully!")
