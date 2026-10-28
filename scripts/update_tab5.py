# -*- coding: utf-8 -*-
with open("dashboard/halloween_app.py", "r", encoding="utf-8") as f:
    text = f.read()

old_sec = """                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">1. ความครบถ้วนของข้อมูลสภาพภูมิอากาศ (QA Completeness)</h4>
                        <p>50 สถานี × 24 เดือน = 1,200 สถานี–เดือน</p>
                        <p>• ระเบียนข้อมูลจริง: <strong>983 แถว</strong> (Missing Rows: <strong>217 แถว</strong> หรือ 18.08% เนื่องจากสถานียังไม่ติดตั้งหรือหยุดส่งสัญญาณ)</p>
                        <p>• ข้อมูลค่าฝนว่าง (Missing Values): <strong>7 ค่า</strong> จาก 983 แถว</p>"""

new_sec = """                        <h4 style="color:#ffffff; margin-bottom:0.4rem;">1. ความครบถ้วนและการรองรับ Dual Mode (Observed vs Exploratory)</h4>
                        <p>50 สถานี × 24 เดือน = 1,200 สถานี–เดือน (ชุดข้อมูล 9 จังหวัด ภาคเหนือ)</p>
                        <p>• <strong>🧪 โหมดตรวจวัดจริง (Observed Only):</strong> 977 เดือนตรวจวัดจริง (ปี 2022 ครบ 12 ด. 46 สถานี, ขาด 4 สถานี / ปี 2023 ตรวจวัดได้สูงสุด 9 ด. 0 สถานีครบ 12 ด.) ห้ามแสดงผลรวมทั้งปีสำหรับสถานีที่ข้อมูลไม่ครบตามหลักสถิติ</p>
                        <p>• <strong>🔮 โหมดทดลองวิเคราะห์ (Exploratory 12 ด.):</strong> ไฟล์ <code>data/analysis_ready/HRDI_2022_2023_12months_EXPLORATORY.csv</code> (1,200 แถว ครบ 100% ไม่มีคีย์ซ้ำ) เติมเต็ม 223 สถานี-เดือน ด้วย Donor Station Spatial Correlation และ Historical Medians สำหรับงานวิจัยเชิงสำรวจ</p>"""

if old_sec in text:
    text = text.replace(old_sec, new_sec, 1)
    with open("dashboard/halloween_app.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Tab 5 updated successfully!")
else:
    print("Could not find old_sec in text")
