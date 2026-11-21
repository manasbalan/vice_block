import subprocess, time, json, urllib.request, socket, hashlib, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--remote-debugging-port=9223',
    '--disable-gpu',
    'http://localhost:8000/index.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9223/json').read())
    ws_url = tabs[0]['webSocketDebuggerUrl']
    print('Connecting to:', ws_url)
    
    # Simple RFC 6455 client over raw socket
    # ws_url looks like ws://localhost:9223/devtools/page/...
    path = ws_url.split('localhost:9223')[1]
    s = socket.create_connection(('127.0.0.1', 9223))
    key = base64.b64encode(b'0123456789abcdef').decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:9223\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    resp = s.recv(4096)
    print('Handshake response:', resp[:30].decode('utf-8', errors='ignore'))

    def send_ws(msg_dict):
        payload = json.dumps(msg_dict).encode('utf-8')
        frame = bytearray([0x81]) # text frame
        length = len(payload)
        mask_key = b'\x12\x34\x56\x78'
        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, 'big'))
        frame.extend(mask_key)
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        s.sendall(frame)

    # Enable Console and Runtime
    send_ws({"id": 1, "method": "Console.enable"})
    send_ws({"id": 2, "method": "Runtime.enable"})
    send_ws({"id": 3, "method": "Log.enable"})

    time.sleep(1)
    s.settimeout(2.0)
    data = b''
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
        except socket.timeout:
            break

    # Parse incoming text frames
    idx = 0
    while idx < len(data):
        if idx + 2 > len(data): break
        b1 = data[idx]
        b2 = data[idx+1]
        payload_len = b2 & 0x7f
        header_len = 2
        if payload_len == 126:
            payload_len = int.from_bytes(data[idx+2:idx+4], 'big')
            header_len = 4
        elif payload_len == 127:
            payload_len = int.from_bytes(data[idx+2:idx+10], 'big')
            header_len = 10
        
        frame_end = idx + header_len + payload_len
        if frame_end > len(data): break
        payload = data[idx+header_len:frame_end]
        try:
            msg = json.loads(payload.decode('utf-8', errors='ignore'))
            m_method = msg.get('method', '')
            params = msg.get('params', {})
            if 'Console' in m_method or 'Runtime.consoleAPICalled' in m_method or 'exceptionThrown' in m_method:
                print(f"[{m_method}]", json.dumps(params, indent=2)[:300])
        except:
            pass
        idx = frame_end

finally:
    proc.terminate()
