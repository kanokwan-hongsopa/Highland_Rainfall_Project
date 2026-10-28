import subprocess
import time
import os
import tempfile
import re

def test_streamlit_real():
    print("Testing Streamlit app.py with real browser rendering...")
    proc = subprocess.Popen(
        ['streamlit', 'run', 'app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        # Wait for Streamlit to start up
        time.sleep(4)
        
        udir = tempfile.mkdtemp()
        shot_path = os.path.abspath('reports/screenshots/streamlit_real_render.png')
        
        # We run edge headless without virtual-time-budget, but navigate to http://localhost:8501
        # To let it render, we give it a 5-second delay or run a small CDP script
        edge_cmd = [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            '--headless=new',
            '--disable-gpu',
            f'--user-data-dir={udir}',
            '--window-size=1920,1080',
            '--no-first-run',
            '--no-default-browser-check',
            f'--screenshot={shot_path}',
            'http://localhost:8501'
        ]
        
        res = subprocess.run(edge_cmd, capture_output=True, text=True, timeout=25)
        print("Edge exit:", res.returncode, "Size:", os.path.getsize(shot_path) if os.path.exists(shot_path) else 0)
        
    finally:
        proc.terminate()
        proc.wait()
        print("Streamlit stopped.")

if __name__ == '__main__':
    test_streamlit_real()
