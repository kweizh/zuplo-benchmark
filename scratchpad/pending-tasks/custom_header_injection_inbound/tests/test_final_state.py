import os
import subprocess
import time
import socket
import pytest
import json

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
    if not wait_for_port(8787):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 8787.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_custom_header_injected(start_app):
    """Priority 1: Use HTTP requests to verify the custom header injection policy."""
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8787/hello"],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {result.stdout}")
        
    assert "x-custom-injected" in data, f"Expected 'x-custom-injected' in JSON response, got: {data}"
    assert data["x-custom-injected"] == "Zuplo-Rules", f"Expected 'Zuplo-Rules' for 'x-custom-injected', got: {data['x-custom-injected']}"
