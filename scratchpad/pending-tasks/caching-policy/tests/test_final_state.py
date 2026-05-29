import os
import pytest
import requests
import socket
import json
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"
PORT = 9200

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "zuplo_dev"
        args = ["zuplo", "dev", "--port", str(PORT)]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", PORT)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_cache_miss_and_hit(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "default-run-id")
    url = f"http://localhost:{PORT}/api/{run_id}/data"

    # First Request (Cache Miss)
    response1 = requests.get(url)
    assert response1.status_code == 200, f"First request failed with status code {response1.status_code}"
    assert "x-cache" in response1.headers, "Response missing 'x-cache' header"
    assert response1.headers["x-cache"] == "miss", f"Expected x-cache 'miss', got {response1.headers['x-cache']}"
    
    try:
        data1 = response1.json()
    except ValueError:
        pytest.fail("First response body is not valid JSON")

    # Second Request (Cache Hit)
    response2 = requests.get(url)
    assert response2.status_code == 200, f"Second request failed with status code {response2.status_code}"
    assert "x-cache" in response2.headers, "Response missing 'x-cache' header"
    assert response2.headers["x-cache"] == "hit", f"Expected x-cache 'hit', got {response2.headers['x-cache']}"
    
    try:
        data2 = response2.json()
    except ValueError:
        pytest.fail("Second response body is not valid JSON")
        
    assert data1 == data2, "Data from cache hit does not match data from cache miss"