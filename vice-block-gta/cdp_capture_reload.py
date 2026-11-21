import subprocess, time, json, urllib.request, socket, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--remote-debugging-port=9232',
    '--disable-gpu',
    'http://localhost:8000/index.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9232/json').read())
    game_tab = [t for t in tabs if t.get('type') == 'page'][0]
    
    ws_url = game_tab['webSocketDebuggerUrl']
    path = ws_url.split('localhost:9232')[1]
    s = socket.create_connection(('127.0.0.1', 9232))
    key = base64.b64encode(b'0123456789abcdef').decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:9232\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    s.recv(4096)

    def send_ws(msg_dict):
        payload = json.dumps(msg_dict).encode('utf-8')
        length = len(payload)
        mask_key = b'\x12\x34\x56\x78'
        if length <= 125:
            header = bytearray([0x81, 0x80 | length])
        elif length <= 65535:
            header = bytearray([0x81, 0x80 | 126]) + length.to_bytes(2, 'big')
        else:
            header = bytearray([0x81, 0x80 | 127]) + length.to_bytes(8, 'big')
        frame = header + mask_key + bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        s.sendall(frame)

    # Enable debugger and runtime
    send_ws({"id": 1, "method": "Debugger.enable"})
    send_ws({"id": 2, "method": "Runtime.enable"})
    # Reload page so we capture everything from line 1 of parsing
    send_ws({"id": 3, "method": "Page.reload"})

    time.sleep(2)
    s.settimeout(3.0)
    raw = b''
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            raw += chunk
        except:
            break

    pos = 0
    while pos < len(raw):
        if pos + 2 > len(raw): break
        b1 = raw[pos]
        b2 = raw[pos+1]
        l = b2 & 0x7f
        h = 2
        if l == 126:
            l = int.from_bytes(raw[pos+2:pos+4], 'big')
            h = 4
        elif l == 127:
            l = int.from_bytes(raw[pos+2:pos+10], 'big')
            h = 10
        payload = raw[pos+h:pos+h+l]
        pos += h + l
        try:
            parsed = json.loads(payload.decode('utf-8', errors='ignore'))
            m = parsed.get('method', '')
            if 'exception' in m.lower() or 'error' in m.lower() or 'failed' in m.lower() or 'parsed' in m.lower():
                print(f"[{m}]", json.dumps(parsed.get('params', {}), indent=2)[:300])
        except:
            pass

finally:
    proc.terminate()
