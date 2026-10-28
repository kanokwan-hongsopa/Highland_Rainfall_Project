import subprocess
import time
import urllib.request
import os
import tempfile
import re

def main():
    print("Starting Streamlit app.py...")
    proc = subprocess.Popen(
        ['streamlit', 'run', 'app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        # Wait for Streamlit to start
        for i in range(20):
            time.sleep(1)
            try:
                with urllib.request.urlopen('http://localhost:8501', timeout=1) as resp:
                    if resp.status == 200:
                        print(f"Streamlit HTTP 200 OK after {i+1}s")
                        break
            except Exception:
                pass
        
        # Give Streamlit 5 seconds to run the script and establish connection
        time.sleep(5)
        
        udir = tempfile.mkdtemp()
        log_file = os.path.join(udir, "chrome_debug.log")
        
        edge_cmd = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "--headless=new",
            "--disable-gpu",
            f"--user-data-dir={udir}",
            "--enable-logging",
            f"--log-file={log_file}",
            "--v=1",
            "--dump-dom",
            "http://localhost:8501"
        ]
        
        edge_proc = subprocess.run(edge_cmd, capture_output=True, text=True, timeout=20)
        dom = edge_proc.stdout
        print(f"DOM Output length: {len(dom)}")
        
        if '<iframe' in dom:
            print("Found <iframe in DOM!")
            srcs = re.findall(r'<iframe[^>]*src=[\'"]([^\'"]*)[\'"]', dom)
            print("Iframe srcs:", srcs)
        else:
            print("NO IFRAME IN DOM!")
            print("DOM sample:\n", dom[:1000])
            
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8", errors="ignore") as lf:
                logs = lf.read()
                print("Chrome debug log length:", len(logs))
                # print any error lines
                errors = [l for l in logs.splitlines() if "ERROR" in l or "CONSOLE" in l]
                print(f"Found {len(errors)} error/console log entries:")
                for e in errors[:20]:
                    print("  ", e)
    finally:
        proc.terminate()
        proc.wait()
        stdout, stderr = proc.communicate()
        print("\n--- Streamlit STDOUT ---")
        print(stdout[:1000])
        print("\n--- Streamlit STDERR ---")
        print(stderr[:1000])

if __name__ == "__main__":
    main()
