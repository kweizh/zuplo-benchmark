import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request

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
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
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

def test_query_parameter_transformation(start_app):
    url = "http://localhost:8787/api/data?legacy_id=123&other=abc"
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8')
            data = json.loads(body)
            
            query = data.get("query", {})
            
            assert "legacy_id" not in query, "The query parameter 'legacy_id' should be removed."
            assert query.get("version") == "v2", f"Expected query parameter 'version' to be 'v2', got {query.get('version')}."
            assert query.get("other") == "abc", f"Expected query parameter 'other' to be 'abc', got {query.get('other')}."
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed with status {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"Request failed: {e}")
