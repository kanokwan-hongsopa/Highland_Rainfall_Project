import subprocess
import time
import urllib.request
import json
import os
import tempfile
import socket

def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    p = s.getsockname()[1]
    s.close()
    return p

def main():
    print("Launching Streamlit...")
    st_proc = subprocess.Popen(
        ['streamlit', 'run', 'app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    time.sleep(3)
    
    cdp_port = get_free_port()
    udir = tempfile.mkdtemp()
    print(f"Launching Edge with remote debugging on port {cdp_port}...")
    edge_cmd = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new',
        '--disable-gpu',
        f'--user-data-dir={udir}',
        f'--remote-debugging-port={cdp_port}',
        '--no-first-run',
        '--no-default-browser-check',
        'http://localhost:8501'
    ]
    edge_proc = subprocess.Popen(edge_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Connect to CDP
        time.sleep(4)
        targets_url = f"http://127.0.0.1:{cdp_port}/json"
        with urllib.request.urlopen(targets_url, timeout=5) as r:
            targets = json.loads(r.read().decode('utf-8'))
        print("CDP Targets:", len(targets))
        for t in targets:
            print("Target:", t.get('title'), t.get('url'))
            
        # Give it another 5 seconds to load and execute
        time.sleep(6)
        
        # Let's inspect pages or capture screenshot via CDP
        page_target = [t for t in targets if t.get('type') == 'page'][0]
        ws_url = page_target.get('webSocketDebuggerUrl')
        print("Page WebSocket URL:", ws_url)
        
    except Exception as e:
        print("Error during CDP inspection:", e)
    finally:
        edge_proc.terminate()
        st_proc.terminate()

if __name__ == '__main__':
    main()
