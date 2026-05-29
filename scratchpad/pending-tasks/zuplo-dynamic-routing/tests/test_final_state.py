import os
import pytest
import requests
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the Zuplo dev server using xprocess. Confirms readiness via port check.
    """
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
            """
            Custom check: returns True if port 8787 is accepting connections.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_us_request(start_app):
    """Test that requests with cf-ipcountry: US are routed to the US backend."""
    response = requests.get("http://localhost:8787/api/data", headers={"cf-ipcountry": "US"})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "/us" in response.text, f"Expected response to contain '/us', got: {response.text}"

def test_default_request(start_app):
    """Test that requests with no cf-ipcountry header are routed to the default backend."""
    response = requests.get("http://localhost:8787/api/data")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "/default" in response.text, f"Expected response to contain '/default', got: {response.text}"

def test_other_country_request(start_app):
    """Test that requests with cf-ipcountry: GB are routed to the default backend."""
    response = requests.get("http://localhost:8787/api/data", headers={"cf-ipcountry": "GB"})
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "/default" in response.text, f"Expected response to contain '/default', got: {response.text}"