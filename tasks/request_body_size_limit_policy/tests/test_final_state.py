import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 8787.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_valid_request_under_limit(start_app):
    """Priority 1: Use curl to verify the route handles valid payloads correctly."""
    # 40 bytes body
    body = '{"data": "This is exactly forty bytes!"}'
    assert len(body) == 40, "Test data length mismatch"
    
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-d", body, "http://localhost:8787/upload"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl command failed: {result.stderr}"
    assert result.stdout.strip() == "200", f"Expected HTTP 200 OK for 40-byte request, got: {result.stdout}"

def test_oversized_request_over_limit(start_app):
    """Priority 1: Use curl to verify the route rejects oversized payloads."""
    # 60 bytes body
    body = '{"data": "This is a much longer string that exceeds the fifty byte limit"}'
    assert len(body) == 74, "Test data length mismatch"
    # Wait, the body length is 74, which is over 50. That's fine.
    
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-d", body, "http://localhost:8787/upload"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl command failed: {result.stderr}"
    assert result.stdout.strip() == "413", f"Expected HTTP 413 Payload Too Large for oversized request, got: {result.stdout}"

def test_policy_config_exists():
    """Priority 3: Verify the policy is configured in policies.json."""
    policies_file = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_file), f"policies.json not found at {policies_file}"
    
    with open(policies_file) as f:
        content = f.read()
    
    assert "request-size-limit-inbound" in content, "Expected 'request-size-limit-inbound' in policies.json"
    assert "50" in content, "Expected maxSizeInBytes to be 50 in policies.json"
    assert "false" in content, "Expected trustContentLengthHeader to be false in policies.json"
