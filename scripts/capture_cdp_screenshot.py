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

def send_ws_command(ws_url, method, params=None):
    # Minimal WebSocket frame encoder/decoder in Python socket
    # To avoid external dependencies
    import re
    m = re.match(r'ws://([^:]+):(\d+)(/.*)', ws_url)
    host, port, path = m.group(1), int(m.group(2)), m.group(3)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    # Handshake
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    )
    sock.sendall(handshake.encode('utf-8'))
    
    resp = b""
    while b"\r\n\r\n" not in resp:
        resp += sock.recv(4096)
        
    # Send JSON message
    msg = json.dumps({"id": 1, "method": method, "params": params or {}}).encode('utf-8')
    frame = bytearray([0x81]) # FIN + text opcode
    length = len(msg)
    if length <= 125:
        frame.append(0x80 | length)
    elif length <= 65535:
        frame.append(0x80 | 126)
        frame.extend(length.to_bytes(2, 'big'))
    else:
        frame.append(0x80 | 127)
        frame.extend(length.to_bytes(8, 'big'))
        
    mask_key = os.urandom(4)
    frame.extend(mask_key)
    masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(msg))
    frame.extend(masked)
    sock.sendall(frame)
    
    # Read response
    raw = b""
    sock.settimeout(10)
    while True:
        chunk = sock.recv(65536)
        if not chunk:
            break
        raw += chunk
        # Look for full message
        try:
            # Simple check if json payload is complete
            if b'"id":1' in raw and b'"result"' in raw:
                # Extract text payload from frame
                # Skip websocket header
                idx = raw.find(b'{"id":1')
                if idx != -1:
                    # check if ends with }
                    sub = raw[idx:]
                    # find matching closing brace
                    parsed = json.loads(sub.decode('utf-8', errors='ignore'))
                    sock.close()
                    return parsed
        except Exception:
            pass
            
    sock.close()
    return None

def main():
    print("Launching Streamlit...")
    st_proc = subprocess.Popen(
        ['streamlit', 'run', 'app.py', '--server.port', '8501', '--server.headless', 'true'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    cdp_port = get_free_port()
    udir = tempfile.mkdtemp()
    print(f"Launching Edge on port {cdp_port}...")
    edge_proc = subprocess.Popen([
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        '--headless=new',
        '--disable-gpu',
        f'--user-data-dir={udir}',
        f'--remote-debugging-port={cdp_port}',
        '--window-size=1920,1080',
        '--no-first-run',
        '--no-default-browser-check',
        'http://localhost:8501'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        time.sleep(10) # Wait 10s for Streamlit React frontend & iframe to load
        targets_url = f"http://127.0.0.1:{cdp_port}/json"
        with urllib.request.urlopen(targets_url, timeout=5) as r:
            targets = json.loads(r.read().decode('utf-8'))
            
        page_targets = [t for t in targets if 'localhost:8501' in t.get('url', '')]
        if not page_targets:
            print("No page target!")
            return
            
        target = page_targets[0]
        ws_url = target.get('webSocketDebuggerUrl')
        print("Page Target:", target.get('title'))
        print("Target URL:", target.get('url'))
        
        # Also check all targets to see if iframe is a target!
        print("All targets:")
        for t in targets:
            print(" -", t.get('type'), t.get('title'), t.get('url'))
            
    finally:
        edge_proc.terminate()
        st_proc.terminate()

if __name__ == '__main__':
    main()
