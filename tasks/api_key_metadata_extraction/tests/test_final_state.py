import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/my-zuplo-api"
PORT = 9000

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
    if not wait_for_port(PORT):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required port.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_missing_tenant_id_returns_400(start_app):
    """Priority 1: Verify the API response when tenantId is missing."""
    req = urllib.request.Request(f"http://localhost:{PORT}/api/data")
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 400 Bad Request, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected status code 400, got {e.code}"
        body = e.read().decode('utf-8')
        try:
            data = json.loads(body)
            assert data.get("error") == "Missing tenantId", f"Expected error 'Missing tenantId', got {data}"
        except json.JSONDecodeError:
            pytest.fail(f"Expected JSON response, got: {body}")

def test_valid_tenant_id_returns_correct_response(start_app):
    """Priority 1: Verify the API response with a valid tenantId."""
    req = urllib.request.Request(f"http://localhost:{PORT}/api/data")
    req.add_header("x-mock-tenant-id", "acme")
    try:
        response = urllib.request.urlopen(req)
        assert response.code == 200, f"Expected status code 200, got {response.code}"
        body = response.read().decode('utf-8')
        data = json.loads(body)
        assert data.get("downstreamUrl") == "https://acme.api.example.com", f"Expected downstreamUrl 'https://acme.api.example.com', got {data.get('downstreamUrl')}"
        assert data.get("tenantHeader") == "acme", f"Expected tenantHeader 'acme', got {data.get('tenantHeader')}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with status {e.code}: {e.read().decode('utf-8')}")

def test_tenant_routing_policy_implementation():
    """Priority 3: Verify the tenant-routing.ts implementation clones the request."""
    policy_path = os.path.join(PROJECT_DIR, "modules", "tenant-routing.ts")
    assert os.path.isfile(policy_path), f"Policy file {policy_path} not found."
    with open(policy_path) as f:
        content = f.read()
    assert "new ZuploRequest" in content, "Expected 'new ZuploRequest' to be used to clone the request in tenant-routing.ts."
