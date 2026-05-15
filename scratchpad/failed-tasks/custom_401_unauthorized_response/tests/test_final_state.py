import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
import json

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["npx", "zuplo", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(9000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Zuplo dev server failed to start and listen on port 9000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_custom_401_response(start_app):
    """Priority 1: Test the actual response of the server."""
    req = urllib.request.Request("http://localhost:9000/protected")
    try:
        response = urllib.request.urlopen(req)
        pytest.fail(f"Expected 401 Unauthorized, but got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected status code 401, got {e.code}"
        
        body = e.read().decode('utf-8')
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Response body is not valid JSON: {body}")
            
        assert data.get("error") == "Custom Unauthorized", f"Expected error message 'Custom Unauthorized', got {data.get('error')}"
        assert data.get("status") == 401, f"Expected status 401 in JSON, got {data.get('status')}"
