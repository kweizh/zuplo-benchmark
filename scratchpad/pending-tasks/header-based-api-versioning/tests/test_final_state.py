import os
import socket
import pytest
import requests
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "zuplo_dev_server"
        args = ["npx", "zuplo", "dev", "--port", "9200"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9200)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_v1_explicit(start_app):
    url = "http://localhost:9200/api/data"
    headers = {"api-version": "v1"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/v1/data", f"Expected URL to be https://echo.zuplo.io/v1/data, got {data.get('url')}"

def test_v2_explicit(start_app):
    url = "http://localhost:9200/api/data"
    headers = {"api-version": "v2"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/v2/data", f"Expected URL to be https://echo.zuplo.io/v2/data, got {data.get('url')}"

def test_default_behavior(start_app):
    url = "http://localhost:9200/api/data"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/v1/data", f"Expected URL to be https://echo.zuplo.io/v1/data, got {data.get('url')}"
