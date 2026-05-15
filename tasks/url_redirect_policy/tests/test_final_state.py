import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/my-zuplo-api"

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

def test_url_redirect(start_app):
    """Priority 1: Use curl to verify the redirect response."""
    result = subprocess.run(
        ["curl", "-I", "-s", "http://localhost:8787/old-api"],
        capture_output=True, text=True
    )
    
    assert "301" in result.stdout, \
        f"Expected HTTP status code 301, got:\n{result.stdout}"
    
    assert "Location: /new-api" in result.stdout or "location: /new-api" in result.stdout, \
        f"Expected Location header to be /new-api, got:\n{result.stdout}"

def test_config_file_updated():
    """Priority 3 fallback: check if routes.oas.json is updated."""
    config_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(config_path) as f:
        content = f.read()
    
    assert "/old-api" in content, "Expected '/old-api' path in routes.oas.json."
    assert "RedirectHandler" in content or "redirect" in content.lower(), "Expected RedirectHandler in routes.oas.json."
    assert "/new-api" in content, "Expected '/new-api' location in routes.oas.json."
