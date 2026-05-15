import os
import subprocess
import time
import socket
import json
import pytest

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
        ["npm", "run", "dev", "--", "--port", "3000"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Zuplo dev server failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_path_rewrite_returns_correct_json(start_app):
    """Verify that the path rewrite proxy works by sending a GET request."""
    result = subprocess.run(
        ["curl", "-s", "http://localhost:3000/api/v1/users"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl command failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"
    assert len(data) > 0, "Expected a non-empty array of users"
    
    first_user = data[0]
    assert "id" in first_user, "Expected user object to have 'id' property"
    assert "name" in first_user, "Expected user object to have 'name' property"