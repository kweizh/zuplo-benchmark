import os
import socket
import requests
import pytest
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the dev server using xprocess. Confirms readiness via port check.
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
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_post_request(start_app):
    """Verify that POST requests are proxied correctly."""
    url = "http://localhost:8787/graphql"
    payload = {"query": "{ countries { code } }"}
    response = requests.post(url, json=payload)
    
    assert response.status_code == 200, f"Expected status 200 for POST, got {response.status_code}"
    
    data = response.json()
    assert "data" in data and "countries" in data["data"], \
        f"Expected response to contain data.countries, got {data}"

def test_get_request_with_query(start_app):
    """Verify that GET requests with a query parameter are converted to POST and proxied."""
    url = "http://localhost:8787/graphql"
    params = {"query": "{ countries { code } }"}
    response = requests.get(url, params=params)
    
    assert response.status_code == 200, f"Expected status 200 for GET with query, got {response.status_code}"
    
    data = response.json()
    assert "data" in data and "countries" in data["data"], \
        f"Expected response to contain data.countries, got {data}"

def test_get_request_without_query(start_app):
    """Verify that GET requests without a query parameter return a 400 Bad Request."""
    url = "http://localhost:8787/graphql"
    response = requests.get(url)
    
    assert response.status_code == 400, f"Expected status 400 for GET without query, got {response.status_code}"
    assert response.text == "Missing query parameter", f"Expected 'Missing query parameter', got {response.text}"
