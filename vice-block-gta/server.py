import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    # Find free port if 8000 is taken
    port = PORT
    for p in range(8000, 8020):
        try:
            with socketserver.TCPServer(("", p), Handler) as httpd:
                url = f"http://localhost:{p}/index.html"
                print("=" * 60)
                print("  VICE CITY BLOCKS: The Low-Spec GTA 6 (Roblox Edition)")
                print("=" * 60)
                print(f"  Game running at: {url}")
                print("  Press Ctrl+C to stop the game server.")
                print("=" * 60)
                webbrowser.open(url)
                httpd.serve_forever()
        except OSError:
            continue

if __name__ == "__main__":
    run()
