import os
import requests
import pytest
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "zuplo_dev"
        args = ["zuplo", "dev", "--port", "3000"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 3000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_cors_options_valid_origin(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "default-run-id")
    origin = f"https://example-{run_id}.com"
    
    response = requests.options(
        "http://localhost:3000/api/data",
        headers={"Origin": origin}
    )
    
    assert response.status_code in [200, 204], f"Expected status 200 or 204 for OPTIONS, got {response.status_code}"
    
    allow_origin = response.headers.get("access-control-allow-origin", "")
    assert allow_origin == origin, f"Expected access-control-allow-origin to be '{origin}', got '{allow_origin}'"
    
    allow_methods = response.headers.get("access-control-allow-methods", "")
    assert "GET" in allow_methods and "OPTIONS" in allow_methods, f"Expected access-control-allow-methods to contain GET and OPTIONS, got '{allow_methods}'"
    
    allow_headers = response.headers.get("access-control-allow-headers", "").lower()
    assert "content-type" in allow_headers and "authorization" in allow_headers, f"Expected access-control-allow-headers to contain Content-Type and Authorization, got '{allow_headers}'"

def test_cors_get_valid_origin(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "default-run-id")
    origin = f"https://example-{run_id}.com"
    
    response = requests.get(
        "http://localhost:3000/api/data",
        headers={"Origin": origin}
    )
    
    assert response.status_code == 200, f"Expected status 200 for GET, got {response.status_code}"
    
    allow_origin = response.headers.get("access-control-allow-origin", "")
    assert allow_origin == origin, f"Expected access-control-allow-origin to be '{origin}', got '{allow_origin}'"
    
    try:
        data = response.json()
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
        
    assert data.get("message") == "Hello CORS", f"Expected body {{'message': 'Hello CORS'}}, got {data}"

def test_cors_get_invalid_origin(start_app):
    invalid_origin = "https://evil.com"
    
    response = requests.get(
        "http://localhost:3000/api/data",
        headers={"Origin": invalid_origin}
    )
    
    allow_origin = response.headers.get("access-control-allow-origin", "")
    assert allow_origin != invalid_origin, f"Expected access-control-allow-origin NOT to be '{invalid_origin}', but it was."
