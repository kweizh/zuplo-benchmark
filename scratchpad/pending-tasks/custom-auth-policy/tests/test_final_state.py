import os
import requests
import socket
import pytest
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_valid_token(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "default-run-id")
    url = "http://localhost:8787/protected"
    headers = {"Authorization": f"CustomToken secret-token-{run_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    assert "Hello, authenticated user!" in response.text, f"Expected 'Hello, authenticated user!' in response, got: {response.text}"

def test_missing_token(start_app):
    url = "http://localhost:8787/protected"
    response = requests.get(url)
    assert response.status_code == 401, f"Expected status 401 for missing token, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"error": "Unauthorized"}, f"Expected JSON error response, got: {response.text}"

def test_invalid_token_format(start_app):
    run_id = os.environ.get("ZEALT_RUN_ID", "default-run-id")
    url = "http://localhost:8787/protected"
    headers = {"Authorization": f"Bearer secret-token-{run_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, f"Expected status 401 for invalid format, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"error": "Unauthorized"}, f"Expected JSON error response, got: {response.text}"

def test_incorrect_token_value(start_app):
    url = "http://localhost:8787/protected"
    headers = {"Authorization": "CustomToken invalid-token"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, f"Expected status 401 for incorrect token, got {response.status_code}. Response: {response.text}"
    assert response.json() == {"error": "Unauthorized"}, f"Expected JSON error response, got: {response.text}"