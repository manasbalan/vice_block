import subprocess, time, json, urllib.request, socket, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--remote-debugging-port=9224',
    '--disable-gpu',
    'http://localhost:8000/index.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9224/json').read())
    ws_url = tabs[0]['webSocketDebuggerUrl']
    path = ws_url.split('localhost:9224')[1]
    s = socket.create_connection(('127.0.0.1', 9224))
    key = base64.b64encode(b'0123456789abcdef').decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:9224\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    s.recv(4096)

    def send_ws(msg_dict):
        payload = json.dumps(msg_dict).encode('utf-8')
        mask_key = b'\x12\x34\x56\x78'
        frame = bytearray([0x81, 0x80 | len(payload)]) + mask_key
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        s.sendall(frame)

    # Evaluate JavaScript in the page
    expr = "({ frameCount: _frameCount, inMenu: State.inMenu, playerPos: player ? player.group.position : null, animErr: window._lastAnimErr || null })"
    send_ws({"id": 10, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}})

    time.sleep(1)
    data = s.recv(4096)
    # decode payload
    for part in data.split(b'{"id":10,'):
        if len(part) > 1:
            print("Eval result:", (b'{"id":10,' + part).decode('utf-8', errors='ignore')[:500])

finally:
    proc.terminate()
