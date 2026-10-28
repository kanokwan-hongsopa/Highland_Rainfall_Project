# -*- coding: utf-8 -*-
"""
Fix HRDI stations matching across all 9 provinces in dashboard/halloween_app.py
Ensure all 9 provinces show their real HRDI station data without being filtered out.
"""

from pathlib import Path

APP_PATH = Path("dashboard/halloween_app.py")

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Tab 2 Filter HTML
old_tab2_html = """                        <select id="tab2_filterProvince" class="filter-select">
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
                        </select>"""

new_tab2_html = """                        <select id="tab2_filterProvince" class="filter-select">
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
                        </select>"""

assert old_tab2_html in content, "old_tab2_html not found"
content = content.replace(old_tab2_html, new_tab2_html, 1)

# 2. Update Tab 4 Filter HTML
old_tab4_html = """                        <select id="tab4_filterProvince" class="filter-select">
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
                        </select>"""

new_tab4_html = """                        <select id="tab4_filterProvince" class="filter-select">
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
                        </select>"""

assert old_tab4_html in content, "old_tab4_html not found"
content = content.replace(old_tab4_html, new_tab4_html, 1)

# 3. Update renderTab1RainCompareChart
old_tab1_rain_comp = """        function renderTab1RainCompareChart() {{
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
            }});"""

new_tab1_rain_comp = """        function renderTab1RainCompareChart() {{
            const canvas = document.getElementById('chartTab1RainCompare');
            if (!canvas) return;
            if (chartTab1RainComp) chartTab1RainComp.destroy();

            const p = state.tab1.province;
            const yr = state.tab1.year;

            clearChartEmptyState('chartTab1RainCompare');

            const provNames = (p === 'all') ? Object.keys(REAL_DATA.province_summaries) : [p];
            const hrdiData = [];
            const hiiData = [];

            provNames.forEach(pr => {{
                const sum = REAL_DATA.province_summaries[pr] || {{}};
                const hrdi = (yr === '2022') ? sum.rain_2022 : (yr === '2023') ? sum.rain_2023 : sum.rain_all;
                const hii = (yr === '2022') ? (sum.hii_rain_2022 || 0) : (yr === '2023') ? (sum.hii_rain_2023 || 0) : (((sum.hii_rain_2022 || 0) + (sum.hii_rain_2023 || 0)) / 2);
                hrdiData.push(Math.round(hrdi || 0));
                hiiData.push(Math.round(hii || 0));
            }});"""

assert old_tab1_rain_comp in content, "old_tab1_rain_comp not found"
content = content.replace(old_tab1_rain_comp, new_tab1_rain_comp, 1)

# 4. Update Tab 2 Components & Charts
old_tab2_js = """        function updateTab2Components() {{
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
            }}"""

new_tab2_js = """        function updateTab2Components() {{
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

            provList.forEach(pr => {{
                const s = REAL_DATA.province_summaries[pr] || {{}};
                const hrdi = (yr === '2022') ? s.rain_2022 : (yr === '2023') ? s.rain_2023 : sum.rain_all;
                const hii = (yr === '2022') ? s.hii_rain_2022 : (yr === '2023') ? s.hii_rain_2023 : (((s.hii_rain_2022 || 0) + (s.hii_rain_2023 || 0)) / 2);
                hrdiVals.push(Math.round(hrdi || 0));
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
                const vals = pStas.map(s => (s.monthly_rain_2022 && s.monthly_rain_2022[i] !== null && !isNaN(s.monthly_rain_2022[i])) ? s.monthly_rain_2022[i] : null).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
            }});
            let hrdi23 = months.map((_, i) => {{
                const vals = pStas.map(s => (s.monthly_rain_2023 && s.monthly_rain_2023[i] !== null && !isNaN(s.monthly_rain_2023[i])) ? s.monthly_rain_2023[i] : null).filter(v => v !== null);
                return vals.length > 0 ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
            }});

            datasets2.unshift(
                {{ label: `HRDI บนพื้นที่สูง (2022) [${{pStas.length}} สถานี]`, data: hrdi22, borderColor: '#A778E8', tension: 0.3 }},
                {{ label: `HRDI บนพื้นที่สูง (2023) [${{pStas.length}} สถานี]`, data: hrdi23, borderColor: '#FF8A32', tension: 0.3 }}
            );"""

assert old_tab2_js in content, "old_tab2_js not found"
content = content.replace(old_tab2_js, new_tab2_js, 1)

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] All 9 provinces HRDI matching updated successfully!")
