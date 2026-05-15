import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
import base64

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(9000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 9000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_unauthenticated_request_returns_401(start_app):
    url = "http://localhost:9000/todos"
    req = urllib.request.Request(url)
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 Unauthorized, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized, got {e.code}"

def test_authenticated_request_returns_200(start_app):
    url = "http://localhost:9000/todos"
    req = urllib.request.Request(url)
    
    # Add Basic Auth header
    auth_str = "admin:secretpassword"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    req.add_header("Authorization", f"Basic {auth_base64}")
    
    try:
        response = urllib.request.urlopen(req)
        assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK, but got {e.code}: {e.read().decode('utf-8')}")
