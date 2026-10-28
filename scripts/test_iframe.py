import subprocess
import os
import tempfile

def test_iframe():
    test_html = """<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background:#100B1B;">
<iframe src="standalone_preview.html" style="width: 100vw; height: 100vh; border: none;"></iframe>
</body>
</html>"""
    
    with open('dashboard/test_iframe.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
        
    udir = tempfile.mkdtemp()
    out_shot = os.path.abspath('reports/screenshots/test_iframe_shot.png')
    
    res = subprocess.run([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new', '--disable-gpu', f'--user-data-dir={udir}',
        '--window-size=1920,1080', '--no-first-run', '--no-default-browser-check',
        f'--screenshot={out_shot}',
        'file:///' + os.path.abspath('dashboard/test_iframe.html').replace('\\', '/')
    ], capture_output=True, text=True)
    
    print('Exit:', res.returncode, 'exists:', os.path.exists(out_shot), 'size:', os.path.getsize(out_shot) if os.path.exists(out_shot) else 0)

if __name__ == '__main__':
    test_iframe()
