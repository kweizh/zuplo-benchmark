import os
import subprocess
import time
import socket
import json
import urllib.request
import urllib.error
import pytest

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
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=30)
    except ProcessLookupError:
        pass

def test_custom_404_handler(start_app):
    """Priority 1: Use urllib to verify the 404 handler behavior."""
    req = urllib.request.Request("http://localhost:3000/does-not-exist")
    
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTPError to be raised for 404 status.")
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected HTTP status 404, got {e.code}"
        body = e.read().decode('utf-8')
        
        try:
            response_json = json.loads(body)
        except json.JSONDecodeError:
            pytest.fail(f"Expected JSON response, got: {body}")
            
        assert response_json.get("error") == "Custom 404 - Route not found", \\
            f"Expected error message 'Custom 404 - Route not found', got {response_json.get('error')}"
            
        assert response_json.get("path") == "/does-not-exist", \\
            f"Expected path '/does-not-exist', got {response_json.get('path')}"
