import pytest
import os
import requests
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npx", "zuplo", "dev", "--port", "8080"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8080)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_eu_routing_gb(start_app):
    url = "http://localhost:8080/api/data"
    headers = {"cf-ipcountry": "GB"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "https://echo.zuplo.io/eu/api/data" in data.get("url", ""), f"Expected URL to be EU, got {data.get('url')}"

def test_eu_routing_fr(start_app):
    url = "http://localhost:8080/api/data"
    headers = {"cf-ipcountry": "FR"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "https://echo.zuplo.io/eu/api/data" in data.get("url", ""), f"Expected URL to be EU, got {data.get('url')}"

def test_us_routing_jp(start_app):
    url = "http://localhost:8080/api/data"
    headers = {"cf-ipcountry": "JP"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "https://echo.zuplo.io/us/api/data" in data.get("url", ""), f"Expected URL to be US, got {data.get('url')}"

def test_us_routing_missing_header(start_app):
    url = "http://localhost:8080/api/data"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert "https://echo.zuplo.io/us/api/data" in data.get("url", ""), f"Expected URL to be US, got {data.get('url')}"
