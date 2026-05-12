import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/project"

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
    if not wait_for_port(9000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 9000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def make_request(payload):
    req = urllib.request.Request(
        "http://localhost:9000/ask",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            headers = response.headers
            status = response.status
            return status, headers, json.loads(body)
    except urllib.error.HTTPError as e:
        return e.code, e.headers, {}
    except Exception as e:
        pytest.fail(f"Request failed: {str(e)}")

def test_semantic_caching(start_app):
    # Request 1: Initial question
    payload1 = {"query": {"text": "What is the capital of France?"}}
    status1, headers1, body1 = make_request(payload1)
    
    assert status1 == 200, f"Expected status 200, got {status1}"
    assert headers1.get('zp-semantic-cache') == 'MISS', f"Expected MISS, got {headers1.get('zp-semantic-cache')}"
    timestamp1 = body1.get('generatedAt')
    assert timestamp1 is not None, "Expected 'generatedAt' in response body"

    # Request 2: Exact same question
    status2, headers2, body2 = make_request(payload1)
    assert status2 == 200, f"Expected status 200, got {status2}"
    assert headers2.get('zp-semantic-cache') == 'HIT', f"Expected HIT, got {headers2.get('zp-semantic-cache')}"
    assert body2.get('generatedAt') == timestamp1, "Expected the same timestamp for a cached response"

    # Request 3: Semantically similar question
    payload3 = {"query": {"text": "Tell me the capital city of France"}}
    status3, headers3, body3 = make_request(payload3)
    assert status3 == 200, f"Expected status 200, got {status3}"
    assert headers3.get('zp-semantic-cache') == 'HIT', f"Expected HIT for semantically similar query, got {headers3.get('zp-semantic-cache')}"
    assert body3.get('generatedAt') == timestamp1, "Expected the same timestamp for a semantically similar cached response"

    # Request 4: Different question
    payload4 = {"query": {"text": "What is the population of Tokyo?"}}
    status4, headers4, body4 = make_request(payload4)
    assert status4 == 200, f"Expected status 200, got {status4}"
    assert headers4.get('zp-semantic-cache') == 'MISS', f"Expected MISS for a different query, got {headers4.get('zp-semantic-cache')}"
    assert body4.get('generatedAt') != timestamp1, "Expected a different timestamp for a new response"