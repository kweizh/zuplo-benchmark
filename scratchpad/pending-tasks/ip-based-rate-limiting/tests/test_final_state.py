import os
import socket
import pytest
import requests
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev", "--", "--editor-port", "9200"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_rate_limiting(start_app):
    url = "http://localhost:9000/api/data"
    
    # First Request
    response1 = requests.get(url)
    assert response1.status_code == 200, f"First request failed. Expected 200, got {response1.status_code}"
    assert "success" in response1.text, f"Expected 'success' in response, got {response1.text}"
    
    # Second Request
    response2 = requests.get(url)
    assert response2.status_code == 200, f"Second request failed. Expected 200, got {response2.status_code}"
    assert "success" in response2.text, f"Expected 'success' in response, got {response2.text}"
    
    # Third Request (Rate Limited)
    response3 = requests.get(url)
    assert response3.status_code == 429, f"Third request failed. Expected 429 Too Many Requests, got {response3.status_code}"
