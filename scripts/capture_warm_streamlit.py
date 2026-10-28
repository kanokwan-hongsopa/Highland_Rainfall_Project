import subprocess
import time
import urllib.request
import json
import os
import tempfile
import socket
import base64

def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    p = s.getsockname()[1]
    s.close()
    return p

def main():
    print("Launching Streamlit app.py...")
    st_proc = subprocess.Popen(
        ['streamlit', 'run', 'app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    cdp_port = get_free_port()
    udir = tempfile.mkdtemp()
    print(f"Launching Edge on port {cdp_port}...")
    edge_cmd = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new',
        '--disable-gpu',
        f'--user-data-dir={udir}',
        f'--remote-debugging-port={cdp_port}',
        '--window-size=1920,1080',
        '--no-first-run',
        '--no-default-browser-check',
        'http://localhost:8501'
    ]
    edge_proc = subprocess.Popen(edge_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Wait 8 seconds for page to load in Streamlit
        time.sleep(8)
        
        targets_url = f"http://127.0.0.1:{cdp_port}/json"
        with urllib.request.urlopen(targets_url, timeout=5) as r:
            targets = json.loads(r.read().decode('utf-8'))
            
        page_targets = [t for t in targets if 'localhost:8501' in t.get('url', '')]
        if not page_targets:
            print("No page target found!")
            return
            
        page_target = page_targets[0]
        print("Page Target Found:", page_target.get('title'))
        
        # Let's use simple websocket client via python's standard library or socket
        # Or even simpler: use Edge's screenshot command on http://localhost:8501 now that the server is warm!
        time.sleep(5) # Give it 5 more seconds to execute JavaScript inside iframe
        
        shot_path = os.path.abspath('reports/screenshots/streamlit_active_screen.png')
        # Let's run a one-shot screenshot command now that the server is running and hot
        shot_cmd = [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            '--headless=new',
            '--disable-gpu',
            f'--user-data-dir={tempfile.mkdtemp()}',
            '--window-size=1920,1080',
            f'--screenshot={shot_path}',
            'http://localhost:8501'
        ]
        res = subprocess.run(shot_cmd, capture_output=True, text=True, timeout=20)
        print("Screenshot Result:", res.returncode, "Size:", os.path.getsize(shot_path) if os.path.exists(shot_path) else 0)
        
    except Exception as e:
        print("Error:", e)
    finally:
        edge_proc.terminate()
        st_proc.terminate()

if __name__ == '__main__':
    main()
