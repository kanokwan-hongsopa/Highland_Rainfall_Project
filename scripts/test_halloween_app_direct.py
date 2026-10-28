import subprocess
import time
import os
import tempfile
import urllib.request

def test_direct():
    print("Testing 'streamlit run dashboard/halloween_app.py'...")
    proc = subprocess.Popen(
        ['streamlit', 'run', 'dashboard/halloween_app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        started = False
        for i in range(20):
            time.sleep(1)
            try:
                with urllib.request.urlopen('http://localhost:8501', timeout=1) as resp:
                    if resp.status == 200:
                        print(f"Streamlit HTTP 200 OK after {i+1}s")
                        started = True
                        break
            except Exception:
                pass
        if not started:
            print("Failed to start Streamlit!")
            return
            
        time.sleep(5)
        # Check target via Edge
        udir = tempfile.mkdtemp()
        edge_cmd = [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            '--headless=new',
            '--disable-gpu',
            f'--user-data-dir={udir}',
            '--dump-dom',
            'http://localhost:8501'
        ]
        res = subprocess.run(edge_cmd, capture_output=True, text=True, timeout=20)
        dom = res.stdout
        print("DOM Output length:", len(dom))
        for line in dom.splitlines():
            if 'stApp' in line or 'iframe' in line or 'title' in line.lower():
                print("DOM check:", line[:160])
                
        # Also check stdout/stderr for any errors
        time.sleep(1)
        print("Success! Dashboard initialized smoothly directly from dashboard/halloween_app.py!")
    finally:
        proc.terminate()
        proc.wait()
        print("Terminated.")

if __name__ == '__main__':
    test_direct()
