import os
import socket
import pytest
import requests
import subprocess
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session", autouse=True)
def npm_install():
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)

@pytest.fixture(scope="session")
def start_mock_server(xprocess):
    mock_server_path = os.path.join(PROJECT_DIR, "mock_server.py")
    with open(mock_server_path, "w") as f:
        f.write("""
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/fast':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'fast')
        elif self.path == '/slow':
            time.sleep(3)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'slow')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), MockHandler)
    server.serve_forever()
""")

    class MockServerStarter(ProcessStarter):
        name = "mock_server"
        args = ["python3", "mock_server.py"]
        env = os.environ.copy()
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 30
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8080)) == 0

    xprocess.ensure(MockServerStarter.name, MockServerStarter)
    yield
    info = xprocess.getinfo(MockServerStarter.name)
    info.terminate()

@pytest.fixture
def start_zuplo_fast(xprocess, start_mock_server):
    class ZuploFastStarter(ProcessStarter):
        name = "zuplo_fast"
        args = ["npx", "zuplo", "dev", "--no-start-editor", "--no-start-docs", "--port", "9200"]
        env = os.environ.copy()
        env["UPSTREAM_URL"] = "http://localhost:8080/fast"
        env["UPSTREAM_TIMEOUT_MS"] = "1000"
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9200)) == 0

    xprocess.ensure(ZuploFastStarter.name, ZuploFastStarter)
    yield
    info = xprocess.getinfo(ZuploFastStarter.name)
    info.terminate()

@pytest.fixture
def start_zuplo_slow(xprocess, start_mock_server):
    class ZuploSlowStarter(ProcessStarter):
        name = "zuplo_slow"
        args = ["npx", "zuplo", "dev", "--no-start-editor", "--no-start-docs", "--port", "9200"]
        env = os.environ.copy()
        env["UPSTREAM_URL"] = "http://localhost:8080/slow"
        env["UPSTREAM_TIMEOUT_MS"] = "1000"
        popen_kwargs = {"cwd": PROJECT_DIR, "text": True}
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9200)) == 0

    xprocess.ensure(ZuploSlowStarter.name, ZuploSlowStarter)
    yield
    info = xprocess.getinfo(ZuploSlowStarter.name)
    info.terminate()

def test_fast_response(start_zuplo_fast):
    response = requests.get("http://localhost:9200/proxy")
    assert response.status_code == 200, f"Expected status 200 for fast response, got {response.status_code}. Response: {response.text}"
    assert response.text == "fast", f"Expected response text 'fast', got {response.text}"

def test_slow_response_timeout(start_zuplo_slow):
    response = requests.get("http://localhost:9200/proxy")
    assert response.status_code == 504, f"Expected status 504 for slow response timeout, got {response.status_code}. Response: {response.text}"
