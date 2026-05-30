import os
import socket
import pytest
import requests
import jwt
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"
JWT_SECRET = os.environ.get("JWT_SECRET", "my-super-secret-key")

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["npm", "run", "dev", "--", "--port", "3000"]
        env = os.environ.copy()
        env["JWT_SECRET"] = JWT_SECRET
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

def test_missing_token(start_app):
    response = requests.get("http://localhost:3000/protected")
    assert response.status_code == 401, f"Expected 401 for missing token, got {response.status_code}"

def test_invalid_token(start_app):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = requests.get("http://localhost:3000/protected", headers=headers)
    assert response.status_code == 401, f"Expected 401 for invalid token, got {response.status_code}"

def test_valid_token(start_app):
    token = jwt.encode({"sub": "user123"}, JWT_SECRET, algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:3000/protected", headers=headers)
    assert response.status_code == 200, f"Expected 200 for valid token, got {response.status_code}"
    data = response.json()
    assert "message" in data and data["message"] == "Hello, authenticated user!", \
        f"Expected 'Hello, authenticated user!' message, got {data}"

def test_invalid_signature_token(start_app):
    token = jwt.encode({"sub": "user123"}, "wrong-secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:3000/protected", headers=headers)
    assert response.status_code == 401, f"Expected 401 for invalid signature token, got {response.status_code}"
