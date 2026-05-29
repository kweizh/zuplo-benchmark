import os
import time
import requests
import pytest
import subprocess
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_echo_server(xprocess):
    class Starter(ProcessStarter):
        name = "echo_server"
        args = ["python3", "-c", """
import http.server
class EchoHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'ECHO: ' + post_data)

http.server.HTTPServer(('127.0.0.1', 8080), EchoHandler).serve_forever()
"""]
        timeout = 10
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("127.0.0.1", 8080)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

@pytest.fixture(scope="session")
def start_zuplo_app(xprocess):
    log_path = os.path.join(PROJECT_DIR, "dev.log")
    log_file = open(log_path, "w")
    
    class Starter(ProcessStarter):
        name = "zuplo_app"
        args = ["npm", "run", "dev"]
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "stdout": log_file,
            "stderr": subprocess.STDOUT,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("127.0.0.1", 3000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()
    log_file.close()

def test_echo_and_logging(start_echo_server, start_zuplo_app):
    url = "http://localhost:3000/api/echo"
    headers = {"Content-Type": "text/plain"}
    body = "Hello Zuplo Cloning Test"
    
    response = requests.post(url, headers=headers, data=body)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.text == "ECHO: Hello Zuplo Cloning Test", f"Expected 'ECHO: Hello Zuplo Cloning Test', got {response.text}"
    
    time.sleep(2)
    
    log_path = os.path.join(PROJECT_DIR, "dev.log")
    assert os.path.exists(log_path), "dev.log does not exist"
    
    with open(log_path, "r") as f:
        logs = f.read()
    
    assert "Intercepted Request: Hello Zuplo Cloning Test" in logs, "Request body was not logged correctly in dev.log"
    assert "Intercepted Response: ECHO: Hello Zuplo Cloning Test" in logs, "Response body was not logged correctly in dev.log"
