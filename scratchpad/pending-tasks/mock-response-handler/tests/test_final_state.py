import os
import socket
import requests
import pytest
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the npm service using xprocess. Confirms readiness via port check.
    """
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev", "--", "--port", "9200"]
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

def test_mock_response(start_app):
    """
    Verify that GET /mock returns the expected JSON response.
    """
    response = requests.get("http://localhost:9200/mock")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type.lower(), f"Expected application/json content-type, got {content_type}"
    
    data = response.json()
    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("message") == "This is a mocked response", f"Expected message 'This is a mocked response', got {data.get('message')}"
