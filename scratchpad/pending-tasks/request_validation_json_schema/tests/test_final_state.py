import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

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
        ["npx", "zuplo", "dev"],
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
        pytest.fail("Zuplo gateway failed to start and listen on port 9000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_valid_request(start_app):
    data = json.dumps({"name": "Alice", "age": 30}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:9000/users",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        response = urllib.request.urlopen(req)
        assert response.status == 200, f"Expected 200 OK for valid request, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK for valid request, but got {e.code}: {e.read().decode('utf-8')}")

def test_invalid_request_missing_age(start_app):
    data = json.dumps({"name": "Alice"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:9000/users",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 400 Bad Request for invalid request missing 'age', but got 2xx.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 Bad Request, got {e.code}"

def test_invalid_request_wrong_type(start_app):
    data = json.dumps({"name": "Alice", "age": "thirty"}).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:9000/users",
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 400 Bad Request for invalid request with wrong type, but got 2xx.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 Bad Request, got {e.code}"
