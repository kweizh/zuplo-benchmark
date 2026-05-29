import pytest
import os
import socket
import requests
import hashlib
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the npm dev service using xprocess. Confirms readiness via port check.
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

    # ensure() starts the process and blocks until startup_check is True
    xprocess.ensure(Starter.name, Starter)

    yield

    # --- TEARDOWN ---
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_api_response_and_signature(start_app):
    """
    Verify the API response contains the correct JSON message and the custom signature header.
    """
    url = "http://localhost:8787/api/data"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Check if the expected message is in the response body
    # Removing spaces to handle different formatting
    assert '{"message":"hello edge"}' in response.text.replace(" ", ""), \
        f"Expected message 'hello edge' in response body, got {response.text}"
        
    signature = response.headers.get("x-response-signature")
    assert signature is not None, "Header 'x-response-signature' is missing from the response."
    
    # Calculate expected SHA-256 hash of the exact returned response body
    expected_hash = hashlib.sha256(response.text.encode('utf-8')).hexdigest()
    assert signature == expected_hash, \
        f"Signature mismatch. Expected {expected_hash}, got {signature}."
