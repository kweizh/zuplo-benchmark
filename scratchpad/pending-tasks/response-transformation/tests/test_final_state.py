import os
import pytest
import requests
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the Zuplo dev server using xprocess. Confirms readiness via port check.
    """
    # Ensure dependencies are installed before starting
    os.system(f"cd {PROJECT_DIR} && npm install")

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
            """
            Custom check: returns True if port 9000 is accepting connections.
            xprocess calls this repeatedly until it returns True or times out.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9000)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_fetch_transformed_response(start_app):
    """
    Verify that the /legacy-data endpoint returns the transformed JSON response.
    """
    url = "http://localhost:9000/legacy-data"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"
    
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_data = {
        "note": {
            "to": "User",
            "from": "Admin",
            "heading": "Reminder",
            "body": "Don't forget the meeting!"
        }
    }
    
    assert data == expected_data, f"Expected JSON {expected_data}, got {data}"
