import pytest
import os
import socket
import requests
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 3000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_us_routing(start_app):
    url = "http://localhost:3000/route"
    headers = {"cf-ipcountry": "US"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/us", f"Expected url https://echo.zuplo.io/us, got {data.get('url')}"

def test_gb_routing(start_app):
    url = "http://localhost:3000/route"
    headers = {"cf-ipcountry": "GB"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/gb", f"Expected url https://echo.zuplo.io/gb, got {data.get('url')}"

def test_default_routing(start_app):
    url = "http://localhost:3000/route"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/default", f"Expected url https://echo.zuplo.io/default, got {data.get('url')}"
