import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/zuplo-project"
PORT = 8787
BASE_URL = f"http://localhost:{PORT}/api/status"

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
    if not wait_for_port(PORT):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail(f"App failed to start and listen on port {PORT}.")

    # Give it a bit more time to fully initialize routes
    time.sleep(2)

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_circuit_breaker_behavior(start_app):
    """Verify that the circuit breaker trips after 5 consecutive 5xx errors."""
    
    # 1. Send a GET request to 200, should be OK
    res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{BASE_URL}/200"], capture_output=True, text=True)
    assert res.stdout.strip() == "200", f"Expected initial 200 request to succeed, got {res.stdout.strip()}"
    
    # 2. Send 5 consecutive 500 requests
    for i in range(5):
        res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{BASE_URL}/500"], capture_output=True, text=True)
        assert res.stdout.strip() == "500", f"Expected 500 request {i+1} to return 500, got {res.stdout.strip()}"
    
    # 3. 6th request should trip the circuit breaker and return 503
    res = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", f"{BASE_URL}/500"], capture_output=True, text=True)
    output = res.stdout.strip().split("\n")
    status_code = output[-1]
    body = "\n".join(output[:-1])
    
    assert status_code == "503", f"Expected 6th request to return 503 (tripped), got {status_code}"
    try:
        data = json.loads(body)
        assert data.get("error") == "Circuit breaker tripped", f"Expected error message 'Circuit breaker tripped', got {data}"
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response with error message, got: {body}")
        
    # 4. Subsequent 200 request should also return 503 since the circuit is tripped
    res = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", f"{BASE_URL}/200"], capture_output=True, text=True)
    output = res.stdout.strip().split("\n")
    status_code = output[-1]
    body = "\n".join(output[:-1])
    
    assert status_code == "503", f"Expected subsequent request to return 503 (tripped), got {status_code}"
    try:
        data = json.loads(body)
        assert data.get("error") == "Circuit breaker tripped", f"Expected error message 'Circuit breaker tripped', got {data}"
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response with error message, got: {body}")
