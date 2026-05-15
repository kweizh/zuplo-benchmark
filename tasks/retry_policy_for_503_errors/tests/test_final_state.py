import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

PROJECT_DIR = "/home/user/myproject"

class MockUpstreamHandler(BaseHTTPRequestHandler):
    request_count = 0
    status_to_return = 503

    def do_GET(self):
        MockUpstreamHandler.request_count += 1
        self.send_response(MockUpstreamHandler.status_to_return)
        self.end_headers()
        self.wfile.write(b"Mock Response")

def run_mock_server():
    server = HTTPServer(('127.0.0.1', 8080), MockUpstreamHandler)
    server.serve_forever()

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def setup_environment():
    # Start mock upstream server
    mock_server_thread = threading.Thread(target=run_mock_server, daemon=True)
    mock_server_thread.start()
    assert wait_for_port(8080), "Mock server failed to start on port 8080"

    # Start Zuplo dev server
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Zuplo dev server failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_retry_on_503(setup_environment):
    MockUpstreamHandler.request_count = 0
    MockUpstreamHandler.status_to_return = 503

    try:
        urllib.request.urlopen("http://localhost:3000/data")
    except urllib.error.HTTPError as e:
        assert e.code == 503, f"Expected 503 response, got {e.code}"
    
    # 1 initial request + 3 retries = 4 requests
    assert MockUpstreamHandler.request_count == 4, f"Expected 4 requests to upstream, got {MockUpstreamHandler.request_count}"

def test_no_retry_on_200(setup_environment):
    MockUpstreamHandler.request_count = 0
    MockUpstreamHandler.status_to_return = 200

    try:
        response = urllib.request.urlopen("http://localhost:3000/data")
        assert response.getcode() == 200, f"Expected 200 response, got {response.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 response, got HTTPError {e.code}")
    
    # 1 initial request, no retries
    assert MockUpstreamHandler.request_count == 1, f"Expected 1 request to upstream, got {MockUpstreamHandler.request_count}"
