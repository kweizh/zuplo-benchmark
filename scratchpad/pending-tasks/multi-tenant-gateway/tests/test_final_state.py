import os
import time
import socket
import pytest
import requests
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the zuplo dev server using xprocess. Confirms readiness via port check.
    """
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
            """
            Wait until port 9000 is open.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 9000)) == 0

    xprocess.ensure(Starter.name, Starter)
    # Give the dev server an extra moment to fully initialize its routes
    time.sleep(5)
    
    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_tenant_a_routing(start_app):
    """
    Test that providing x-mock-tenant: customer-a routes correctly to echo.zuplo.io/customer-a.
    """
    url = "http://localhost:9000/api/data"
    headers = {"x-mock-tenant": "customer-a"}
    
    response = requests.get(url, headers=headers, timeout=10)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/customer-a", \
        f"Expected response to contain url 'https://echo.zuplo.io/customer-a', got {data.get('url')}"

def test_tenant_b_routing(start_app):
    """
    Test that providing x-mock-tenant: customer-b routes correctly to echo.zuplo.io/customer-b.
    """
    url = "http://localhost:9000/api/data"
    headers = {"x-mock-tenant": "customer-b"}
    
    response = requests.get(url, headers=headers, timeout=10)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert data.get("url") == "https://echo.zuplo.io/customer-b", \
        f"Expected response to contain url 'https://echo.zuplo.io/customer-b', got {data.get('url')}"

def test_missing_tenant(start_app):
    """
    Test that missing x-mock-tenant header returns a 400 Bad Request.
    """
    url = "http://localhost:9000/api/data"
    
    response = requests.get(url, timeout=10)
    assert response.status_code == 400, f"Expected status 400 for missing tenant, got {response.status_code}"
    
    data = response.json()
    assert "error" in data, "Expected 'error' key in JSON response"
    assert "tenantId" in data["error"] or "tenant" in data["error"].lower(), \
        f"Expected error message to mention tenantId, got {data['error']}"