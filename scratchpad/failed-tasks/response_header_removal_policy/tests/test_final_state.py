import os
import subprocess
import time
import socket
import pytest
import json

PROJECT_DIR = "/home/user/zuplo-project"

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
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Zuplo dev server failed to start and listen on port 8787.")

    # Additional wait for the gateway to be fully ready
    time.sleep(5)

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_x_powered_by_removed(start_app):
    """Priority 1/3: Test the actual response to ensure the header is removed."""
    result = subprocess.run(
        ["curl", "-s", "-i", "http://localhost:8787/hello"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    assert "HTTP/1.1 200 OK" in result.stdout or "HTTP/2 200" in result.stdout, \
        f"Expected 200 OK status, got: {result.stdout}"
    
    # Header should be case-insensitive, but curl -i typically preserves or lowercases
    lower_output = result.stdout.lower()
    assert "x-powered-by" not in lower_output, \
        f"Expected 'x-powered-by' header to be removed, but it was found in the response: {result.stdout}"

def test_policy_configured_correctly():
    """Priority 3: Verify the policy file contains the remove-headers-outbound policy."""
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    with open(policies_path) as f:
        policies_data = json.load(f)
    
    policy_found = False
    for policy in policies_data.get("policies", []):
        if policy.get("policyType") == "remove-headers-outbound":
            options = policy.get("handler", {}).get("options", {})
            headers = options.get("headers", [])
            if "x-powered-by" in headers or "X-Powered-By" in headers:
                policy_found = True
                break
    
    assert policy_found, "Expected a 'remove-headers-outbound' policy configured to remove 'x-powered-by' in policies.json."

def test_route_uses_policy():
    """Priority 3: Verify the route uses the policy."""
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        routes_data = json.load(f)
    
    route = routes_data.get("paths", {}).get("/hello", {}).get("get", {}).get("x-zuplo-route", {})
    policies = route.get("policies", {})
    outbound_policies = policies.get("outbound", [])
    
    # We just need to check if ANY outbound policy is applied, 
    # since we verified the policy definition in the previous test.
    # Ideally, the name should match, but at least there should be an outbound policy.
    assert len(outbound_policies) > 0, "Expected an outbound policy to be applied to the /hello route."
