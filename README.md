# Highland Rainfall & Rice Analysis Interactive Dashboard
### ระบบแดชบอร์ดวิเคราะห์สภาพภูมิอากาศบนพื้นที่สูงและความสัมพันธ์กับผลผลิตข้าวนาปี (2022–2023)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75.svg)](https://plotly.com)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Branch](https://img.shields.io/badge/Git%20Branch-dashboard--dev-green.svg)]()

Interactive Dashboard ภาษาไทยสำหรับสำรวจและวิเคราะห์ข้อมูลสภาพภูมิอากาศบนพื้นที่สูง 9 จังหวัด และสำรวจความสัมพันธ์ระหว่างปริมาณน้ำฝนช่วงกุมภาพันธ์–กรกฎาคมกับผลผลิตข้าวนาปีต่อพื้นที่เก็บเกี่ยวในกลุ่มตัวอย่าง Balanced Panel 25 ตำบล (5 จังหวัด) ระหว่างปี 2022 และ 2023

---

## 📌 ขอบเขตและโครงสร้างการวิเคราะห์

| ส่วนแสดงผล | ขอบเขตพื้นที่ | จำนวนหน่วย | ช่วงเวลา | วัตถุประสงค์หลัก |
| :--- | :--- | :--- | :--- | :--- |
| **แท็บ A: ภาพรวมภูมิอากาศ** | 9 จังหวัดพื้นที่สูง | 50 สถานีตรวจวัด | 2022–2023 (รายเดือน) | สำรวจแนวโน้มรายเดือน, ตรวจสอบความครบถ้วนของข้อมูล, Heatmap แสดง Missing Rows vs Missing Values |
| **แท็บ B: ข้าวนาปีและฝน** | 5 จังหวัด | 25 ตำบล Balanced Panel | 2022–2023 (ฝน ก.พ.–ก.ค.) | เปรียบเทียบผลผลิตและฝนระหว่างปี, Scatter Plot ระดับตำบล ($n=25$) และระดับจังหวัด ($n=5$), สหสัมพันธ์ Spearman |
| **แท็บ C: ระเบียบวิธีและ QA** | - | 25 ตำบลที่จับคู่ได้ | - | บันทึก Data Pipeline, ตารางจับคู่รหัสตำบล 100%, พจนานุกรมข้อมูล, ผลการทดสอบความไว (Sensitivity) |

---

## ⚠️ ข้อกำหนดจริยธรรมข้อมูลและข้อจำกัดการวิเคราะห์

1. **การวิเคราะห์เชิงสำรวจเท่านั้น (Non-causal):** ค่าสหสัมพันธ์ Spearman ที่ติดลบเป็นการสังเกตทิศทางข้อมูล 2 ปี ห้ามตีความว่าฝนลดเป็นสาเหตุให้ผลผลิตเพิ่มขึ้น
2. **ห้ามทำนายหรือพยากรณ์ (No Forecasting):** แสดงผลเฉพาะข้อมูลจริงที่มีอยู่ ไม่มีการใส่แบบจำลองพยากรณ์ใด ๆ
3. **การเป็นตัวแทนพื้นที่:** ข้อมูลสถานี 50 แห่งไม่ใช่ตัวแทนค่าเฉลี่ยของทั้งจังหวัด และกลุ่มตัวอย่างข้าว 5 จังหวัด (เชียงใหม่คิดเป็น 56%) ไม่ใช่ตัวแทนของพื้นที่สูงทั้ง 9 จังหวัด
4. **ระดับข้อมูล HII:** ฝน HII เป็นข้อมูลระดับจังหวัด จึงแสดงในระดับจังหวัด ($n=5$) เท่านั้น ห้ามนับค่าซ้ำในระดับตำบลเป็นตัวอย่างอิสระ
5. **สถานะหน่วยวัดและฤดูปลูก:** หน่วยวัดของฝนและผลผลิตระบุเป็น **"หน่วยรอยืนยัน"** และช่วง ก.พ.–ก.ค. ยังไม่ได้รับการยืนยันว่าเป็นฤดูปลูกข้าวนาปีจริง

---

## 🛠️ โครงสร้างโปรเจกต์

```text
Highland_Rainfall_Project/
├── app.py                     # จุดเริ่มต้นหลักของ Streamlit Application (สลับระหว่าง Halloween และ Classic ได้)
├── requirements.txt           # รายการ Libraries และ Dependencies
├── README.md                  # เอกสารแนะนำและคู่มือการใช้งาน
├── BRD.md                     # ข้อกำหนดทางธุรกิจและการวิเคราะห์
├── HANDOFF.md                 # บันทึกข้อกำหนดส่งต่องาน
├── dashboard/                 # โมดูลระบบแดชบอร์ด
│   ├── __init__.py
│   ├── halloween_app.py       # Halloween Edition: Standalone SPA (Leaflet.js + Chart.js + Smooth Zoom + Detail Drawer)
│   ├── halloween_data.py      # Serializer แปลงข้อมูลจริงเป็น JSON สำหรับ Frontend Engine
│   ├── data_loader.py         # โมดูลอ่านและตรวจสอบข้อมูลจริงพร้อม Caching
│   ├── components.py          # UI Styling, Metric Cards, Alert Banners, Empty State
│   ├── tab_climate.py         # Classic แท็บ A: ภาพรวมสภาพภูมิอากาศ 9 จังหวัด (50 สถานี)
│   ├── tab_rice_rain.py       # Classic แท็บ B: วิเคราะห์ข้าวนาปีและฝน 5 จังหวัด (25 ตำบล)
│   └── tab_methodology.py     # Classic แท็บ C: ระเบียบวิธีวิจัย การจับคู่พื้นที่ และ QA
├── tests/                     # ชุดทดสอบอัตโนมัติ (Automated Unit Tests)
│   ├── test_halloween_app.py  # ทดสอบ Halloween Edition (JSON payload, Theme, Leaflet, Tabs, Disclaimers)
│   ├── test_data_loader.py    # ทดสอบ Data Engine & QA Invariants
│   ├── test_tab_climate.py    # ทดสอบตรรกะและตัวกรองแท็บ A
│   ├── test_tab_rice_rain.py  # ทดสอบตรรกะและ Invariants แท็บ B
│   └── test_tab_methodology.py# ทดสอบความสมบูรณ์แท็บ C
├── data/                      # ข้อมูลที่ผ่านการประมวลผลและไฟล์อ้างอิง
│   ├── processed/             # hrdi_clean_2022_2023.csv
│   ├── dashboard/             # dashboard_rice_tambon.csv, dashboard_province_changes.csv, dashboard_correlations.csv
│   └── reference/             # geo.json, postal_lookup.json
└── reports/                   # รายงานการทดสอบความไวในเครื่อง
```

---

## 🚀 วิธีติดตั้งและรันในเครื่อง (Local Setup)

เปิด PowerShell หรือ Terminal ที่โฟลเดอร์หลักของโปรเจกต์:

### 1. ติดตั้ง Dependencies
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. รันแอปพลิเคชัน Streamlit
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
เมื่อรันคำสั่ง ระบบจะเปิดหน้าต่างเบราว์เซอร์อัตโนมัติที่ `http://localhost:8501`

---

## 🧪 การรันชุดทดสอบ (Automated Unit Tests)

สามารถตรวจสอบความถูกต้องของข้อมูลตามเกณฑ์ QA Metrics ทุกข้อได้ผ่านคำสั่ง:

```powershell
# ทดสอบ Halloween Interactive Dashboard (UI/UX, FlyTo Animation, JSON Integrity, Disclaimers)
$env:PYTHONIOENCODING="utf-8"; .\.venv\Scripts\python.exe tests/test_halloween_app.py

# ทดสอบโมดูลโหลดข้อมูลและเกณฑ์ QA Metrics 8 ข้อ
$env:PYTHONIOENCODING="utf-8"; .\.venv\Scripts\python.exe tests/test_data_loader.py

# ทดสอบตรรกะและตัวกรองแท็บ A (ภาพรวมภูมิอากาศ)
$env:PYTHONIOENCODING="utf-8"; .\.venv\Scripts\python.exe tests/test_tab_climate.py

# ทดสอบตรรกะและ Invariants แท็บ B (ข้าวนาปีและฝน)
$env:PYTHONIOENCODING="utf-8"; .\.venv\Scripts\python.exe tests/test_tab_rice_rain.py

# ทดสอบทะเบียนจับคู่ตำบลและแท็บ C (ระเบียบวิธีวิจัย)
$env:PYTHONIOENCODING="utf-8"; .\.venv\Scripts\python.exe tests/test_tab_methodology.py
```

---

## 📊 ค่าสถิติตรวจรับคุณภาพ (QA Metrics Checklist)

- [x] Balanced Panel: 25 ตำบล × 2 ปี = **50 แถว ไม่มีค่าว่าง**
- [x] การกระจายตัวตำบลรายจังหวัด: `50 (เชียงใหม่): 14`, `55 (น่าน): 5`, `58 (แม่ฮ่องสอน): 3`, `63 (ตาก): 2`, `57 (เชียงราย): 1`
- [x] การจับคู่รหัสตำบลปี 2022–2023 กับ `geo.json`: **ตรงกันสมบูรณ์ 25/25 ตำบล (100%)**
- [x] ทิศทางฝน ก.พ.–ก.ค.: **ลดลงทั้ง 25 ตำบล** ทั้งฝน HRDI และ HII
- [x] ทิศทางผลผลิตข้าวนาปี: **เพิ่มขึ้น 10 ตำบล, ลดลง 10 ตำบล, คงที่ 5 ตำบล**
- [x] ค่า Spearman Rank Correlation ($\rho$):
  - HRDI ระดับตำบล ($n=25$): $\rho = -0.173427$
  - HRDI ระดับจังหวัด ($n=5$): $\rho = -0.7000$
  - HII ระดับจังหวัด ($n=5$): $\rho = -0.9000$
- [x] ช่วงผลการทดสอบความไว Leave-one-province-out:
  - HRDI ตำบล: $-0.5285$ ถึง $+0.0303$
  - HRDI จังหวัด: $-1.0000$ ถึง $-0.4000$
  - HII จังหวัด: $-1.0000$ ถึง $-0.8000$

---

## 🌐 การเผยแพร่บน Streamlit Community Cloud

โปรเจกต์ได้รับการออกแบบให้พร้อม Deploy บน Streamlit Community Cloud ทันที:
- ระบุ Dependencies ครบถ้วนใน `requirements.txt`
- อ้างอิง Path ของไฟล์ด้วย Relative Path (`Path(__file__).resolve().parent.parent`)
- ปลอดภัยต่อ Sandbox และโครงข่ายออฟไลน์ (ไม่มีการดึง Asset ภายนอกที่อาจทำให้แอปค้าง)
- มีระบบจัดการ Empty State เมื่อผู้ใช้กรองข้อมูลจนไม่พบระเบียน
