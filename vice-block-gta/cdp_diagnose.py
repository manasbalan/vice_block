import subprocess, time, json, urllib.request, socket, base64

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless=new',
    '--remote-debugging-port=9225',
    '--disable-gpu',
    'http://localhost:8000/index.html'
]
proc = subprocess.Popen(cmd)
time.sleep(2.5)

try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9225/json').read())
    ws_url = tabs[0]['webSocketDebuggerUrl']
    path = ws_url.split('localhost:9225')[1]
    s = socket.create_connection(('127.0.0.1', 9225))
    key = base64.b64encode(b'0123456789abcdef').decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:9225\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    s.recv(4096)

    def eval_js(expr):
        payload = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}).encode('utf-8')
        mask_key = b'\x12\x34\x56\x78'
        frame = bytearray([0x81, 0x80 | len(payload)]) + mask_key
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        s.sendall(frame)
        time.sleep(0.5)
        res = s.recv(8192)
        # find json
        for line in res.split(b'\r\n'):
            if b'result' in line:
                return line.decode('utf-8', errors='ignore')
        return res.decode('utf-8', errors='ignore')

    out = eval_js("JSON.stringify({ frameCount: _frameCount, animErr: window._lastAnimErr, sceneObjs: scene.children.length, camPos: camera.position })")
    print("CDP Output:", out)

finally:
    proc.terminate()
