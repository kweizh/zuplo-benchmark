import os
import pytest
import requests
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    # Setup .env file
    run_id = os.environ.get("ZEALT_RUN_ID", "zr-12345")
    env_path = os.path.join(PROJECT_DIR, ".env")
    with open(env_path, "w") as f:
        f.write(f"ZEALT_RUN_ID={run_id}\n")

    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev", "--", "--port", "9000", "--editor-port", "9200", "--docs-port", "9300"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_custom_404_response(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "zr-12345")
    url = "http://localhost:9000/some-random-missing-path"
    
    response = requests.get(url)
    
    # Check status code
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}. Response: {response.text}"
    
    # Check headers
    assert response.headers.get("x-custom-404") == "true", f"Expected header 'x-custom-404' to be 'true'. Headers: {response.headers}"
    assert "application/json" in response.headers.get("content-type", ""), f"Expected 'application/json' in content-type, got {response.headers.get('content-type')}"
    
    # Check body
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")
        
    assert data.get("error") == "Not Found", f"Expected error 'Not Found', got {data.get('error')}"
    assert data.get("path") == "/some-random-missing-path", f"Expected path '/some-random-missing-path', got {data.get('path')}"
    assert data.get("run_id") == run_id, f"Expected run_id '{run_id}', got {data.get('run_id')}"
