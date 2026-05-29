import os
import sys
import json
import socket
import subprocess
import time
import requests
import pytest
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def mock_backend():
    """Starts a mock backend on port 8080."""
    mock_script = os.path.join(PROJECT_DIR, "mock_backend.py")
    with open(mock_script, "w") as f:
        f.write('''\
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

status_code = 200

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(b"Mock Response")

    def do_POST(self):
        global status_code
        if self.path == '/set-status':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            status_code = data.get('status', 200)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Status updated")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MockHandler)
    server.serve_forever()
''')

    proc = subprocess.Popen([sys.executable, mock_script])
    
    # Wait for mock backend to start
    for _ in range(30):
        try:
            requests.get("http://localhost:8080/")
            break
        except requests.ConnectionError:
            time.sleep(0.5)
            
    yield
    
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def start_zuplo(xprocess, mock_backend):
    """Starts the zuplo dev server."""
    class Starter(ProcessStarter):
        name = "zuplo_dev"
        args = ["npm", "run", "dev", "--", "--port", "3000"]
        env = os.environ.copy()
        env["BACKEND_URL"] = "http://localhost:8080"
        env["ZEALT_RUN_ID"] = "zr-test123"
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 60
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 3000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()


def test_circuit_breaker(start_zuplo):
    """Verifies the circuit breaker trips after 5 consecutive 5xx errors."""
    
    # 1. Initial State: Backend returns 200
    requests.post("http://localhost:8080/set-status", json={"status": 200})
    resp = requests.get("http://localhost:3000/api/data")
    assert resp.status_code == 200, f"Expected 200 OK when backend is healthy, got {resp.status_code}"
    
    # 2. Trigger Failures: Backend returns 500
    requests.post("http://localhost:8080/set-status", json={"status": 500})
    for i in range(5):
        resp = requests.get("http://localhost:3000/api/data")
        assert resp.status_code == 500, f"Expected 500 from backend on request {i+1}, got {resp.status_code}"
        
    # 3. Circuit Open: 6th request should return 503 from Zuplo immediately
    resp = requests.get("http://localhost:3000/api/data")
    assert resp.status_code == 503, f"Expected 503 Service Unavailable (circuit open) on 6th request, got {resp.status_code}"
