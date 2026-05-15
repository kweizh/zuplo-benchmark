import os
import json
import time
import socket
import subprocess
import urllib.request
import urllib.error
import base64
import hmac
import hashlib
import pytest

PROJECT_DIR = "/home/user/myproject"
JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-key")

def base64url_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def create_jwt(sub, issuer, audience, secret):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": sub,
        "iss": issuer,
        "aud": audience,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    
    encoded_header = base64url_encode(json.dumps(header))
    encoded_payload = base64url_encode(json.dumps(payload))
    
    signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(secret.encode('utf-8'), signature_input, hashlib.sha256).digest()
    encoded_signature = base64url_encode(signature)
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

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
    # Set the secret in the environment
    env = os.environ.copy()
    env["JWT_SECRET"] = JWT_SECRET

    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Zuplo dev server failed to start and listen on port 3000.")

    # Wait a little extra to ensure routes are fully registered
    time.sleep(5)

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_policies_file_contains_policy():
    """Priority 3: Check policies.json contains the jwt policy"""
    policies_file = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_file), "config/policies.json not found"
    
    with open(policies_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("config/policies.json is not valid JSON")
            
    policies = data.get("policies", [])
    jwt_policy = next((p for p in policies if p.get("policyType") == "open-id-jwt-auth-inbound"), None)
    assert jwt_policy is not None, "open-id-jwt-auth-inbound policy not found in policies.json"
    
    options = jwt_policy.get("handler", {}).get("options", {})
    assert options.get("issuer") == "https://my-issuer.com/", "Issuer not set correctly in policy"
    assert options.get("audience") == "https://api.example.com", "Audience not set correctly in policy"
    assert options.get("secret") == "$env(JWT_SECRET)", "Secret not set correctly in policy"

def test_unauthenticated_request_fails(start_app):
    """Priority 1: Test actual server behavior without JWT"""
    req = urllib.request.Request("http://localhost:3000/api/protected")
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 401 Unauthorized, but request succeeded")
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Expected 401 Unauthorized, got {e.code}"

def test_authenticated_request_succeeds(start_app):
    """Priority 1: Test actual server behavior with valid JWT"""
    token = create_jwt("user-12345", "https://my-issuer.com/", "https://api.example.com", JWT_SECRET)
    
    req = urllib.request.Request("http://localhost:3000/api/protected")
    req.add_header("Authorization", f"Bearer {token}")
    
    try:
        response = urllib.request.urlopen(req)
        assert response.code == 200, f"Expected 200 OK, got {response.code}"
        
        data = json.loads(response.read().decode('utf-8'))
        assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
        assert data.get("user") == "user-12345", f"Expected user 'user-12345', got {data.get('user')}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Request failed with {e.code}: {e.read().decode('utf-8')}")
