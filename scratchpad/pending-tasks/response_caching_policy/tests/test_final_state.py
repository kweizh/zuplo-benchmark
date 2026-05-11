import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request
import urllib.error

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
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_response_is_cached(start_app):
    url = "http://localhost:3000/cached-data"
    
    try:
        req1 = urllib.request.Request(url)
        with urllib.request.urlopen(req1) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body1 = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        pytest.fail(f"First request failed: {e}")

    # Small delay to ensure it's not just a fast consecutive request issue
    time.sleep(1)

    try:
        req2 = urllib.request.Request(url)
        with urllib.request.urlopen(req2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body2 = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        pytest.fail(f"Second request failed: {e}")

    assert body1 == body2, "Expected the second response to be identical to the first due to caching, but they differed."

def test_policy_configured_correctly():
    policies_path = os.path.join(PROJECT_DIR, "config/policies.json")
    assert os.path.isfile(policies_path), f"Policies file {policies_path} does not exist."
    
    with open(policies_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("config/policies.json is not valid JSON.")
            
    policies = data.get("policies", [])
    cache_policy = next((p for p in policies if p.get("name") == "my-cache-policy"), None)
    
    assert cache_policy is not None, "Policy 'my-cache-policy' not found in config/policies.json."
    assert cache_policy.get("policyType") == "caching-inbound", f"Expected policyType 'caching-inbound', got {cache_policy.get('policyType')}."
    
    handler = cache_policy.get("handler", {})
    options = handler.get("options", {})
    ttl = options.get("expirationSecondsTtl")
    
    assert ttl == 120, f"Expected expirationSecondsTtl to be 120, got {ttl}."
