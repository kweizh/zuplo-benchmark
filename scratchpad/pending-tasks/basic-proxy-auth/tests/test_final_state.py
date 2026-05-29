import pytest
import requests
import socket
import os
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the zuplo dev service using xprocess. Confirms readiness via port check.
    """
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["zuplo", "dev", "--port", "9200"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            """
            Custom check: returns True if port 9200 is accepting connections.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9200)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_proxy_without_api_key(start_app):
    """Test that accessing /proxy without an API key returns 401 Unauthorized."""
    response = requests.get("http://localhost:9200/proxy")
    assert response.status_code == 401, f"Expected status 401 without API key, got {response.status_code}"

def test_proxy_with_valid_api_key(start_app):
    """Test that accessing /proxy with the valid API key returns 200 OK."""
    headers = {
        "authorization": "Bearer test-api-key-123"
    }
    response = requests.get("http://localhost:9200/proxy", headers=headers)
    assert response.status_code == 200, f"Expected status 200 with valid API key, got {response.status_code}. Response: {response.text}"
