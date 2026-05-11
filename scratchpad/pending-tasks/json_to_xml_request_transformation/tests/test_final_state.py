import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

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

    # Additional short wait to ensure routes are fully loaded
    time.sleep(5)

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_json_to_xml_transformation(start_app):
    url = "http://localhost:3000/submit"
    req_body = json.dumps({"orderId": 123, "amount": 45.67}).encode('utf-8')
    headers = {
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=req_body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status code 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            data = json.loads(resp_body)
            
            # The backend is https://httpbin.org/post, which echoes the request body in the "data" field
            echoed_data = data.get("data", "")
            
            # Verify the XML transformation
            expected_xml = "<order><orderId>123</orderId><amount>45.67</amount></order>"
            # Allow for potential formatting differences (like newlines or xml declarations)
            assert "123" in echoed_data and "45.67" in echoed_data and "orderId" in echoed_data, \
                f"XML transformation missing expected elements. Got: {echoed_data}"
            
            # Remove whitespaces for a more robust check
            stripped_echoed = "".join(echoed_data.split())
            stripped_expected = "".join(expected_xml.split())
            assert stripped_expected in stripped_echoed, \
                f"Expected XML structure {expected_xml} not found in echoed data: {echoed_data}"
            
            # Verify the Content-Type header was transformed
            echoed_headers = data.get("headers", {})
            content_type = echoed_headers.get("Content-Type", "")
            
            assert "application/xml" in content_type, \
                f"Expected Content-Type to contain application/xml, got {content_type}"
                
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed with status {e.code}: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the server: {e.reason}")