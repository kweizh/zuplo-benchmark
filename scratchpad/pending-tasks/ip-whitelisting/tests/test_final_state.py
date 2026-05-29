import pytest
import requests
import os
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev"]
        env = os.environ.copy()
        env["ALLOWED_IPS"] = "192.168.1.1,10.0.0.1"
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_allowed_ip_1(start_app):
    url = "http://localhost:8787/hello"
    headers = {"x-test-ip": "192.168.1.1"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200 for allowed IP, got {response.status_code}"
    assert response.json() == {"message": "Hello from the edge!"}, f"Unexpected response body: {response.text}"

def test_allowed_ip_2(start_app):
    url = "http://localhost:8787/hello"
    headers = {"x-test-ip": "10.0.0.1"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200 for allowed IP, got {response.status_code}"
    assert response.json() == {"message": "Hello from the edge!"}, f"Unexpected response body: {response.text}"

def test_forbidden_ip(start_app):
    url = "http://localhost:8787/hello"
    headers = {"x-test-ip": "192.168.1.2"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 403, f"Expected status 403 for forbidden IP, got {response.status_code}"
    assert response.json() == {"error": "Forbidden IP"}, f"Unexpected response body: {response.text}"

def test_missing_ip(start_app):
    url = "http://localhost:8787/hello"
    response = requests.get(url)
    assert response.status_code == 403, f"Expected status 403 for missing IP header, got {response.status_code}"
    assert response.json() == {"error": "Forbidden IP"}, f"Unexpected response body: {response.text}"
