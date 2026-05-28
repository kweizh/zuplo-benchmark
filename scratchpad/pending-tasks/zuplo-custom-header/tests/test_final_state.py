import pytest
import subprocess
import os
import socket
from xprocess import ProcessStarter
import requests
import base64

PROJECT_DIR = "/home/user/zuplo-project"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Runs npm install and starts zuplo dev using xprocess. Confirms readiness via port check.
    """
    # Ensure dependencies are installed
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)

    class Starter(ProcessStarter):
        name = "start_app"
        args = ["zuplo", "dev"]
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
            xprocess calls this repeatedly until it returns True or times out.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    # --- TEARDOWN ---
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_custom_header(start_app):
    """
    Verify that GET /hello returns 200 and includes the x-signature header
    containing the Base64 encoded string of the response body.
    """
    response = requests.get("http://localhost:8787/hello")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    
    body = response.text
    expected_signature = base64.b64encode(body.encode('utf-8')).decode('utf-8')
    
    assert 'x-signature' in response.headers, "Response does not contain 'x-signature' header"
    actual_signature = response.headers['x-signature']
    
    assert actual_signature == expected_signature, f"Expected signature {expected_signature}, got {actual_signature}"
