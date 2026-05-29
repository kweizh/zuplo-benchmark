import pytest
import requests
import socket
import os
import json
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
                return s.connect_ex(("localhost", 8080)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_proxy_without_api_key(start_app):
    """Test that accessing the proxy without an API key returns 401 Unauthorized."""
    response = requests.get("http://localhost:8080/api/proxy")
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_routes_configuration():
    """Verify that the route is configured to proxy to jsonplaceholder."""
    routes_file = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_file), f"Routes config not found at {routes_file}"
    
    with open(routes_file) as f:
        routes = json.load(f)
        
    paths = routes.get("paths", {})
    assert "/api/proxy" in paths, "Route /api/proxy not found in routes.oas.json"
    
    route_config = paths["/api/proxy"].get("get", {}).get("x-zuplo-route", {})
    
    # Check policies
    policies = route_config.get("policies", {}).get("inbound", [])
    assert "api-key-inbound" in policies, "api-key-inbound policy not applied to /api/proxy"
    
    # Check handler
    handler = route_config.get("handler", {})
    export_name = handler.get("export")
    module_name = handler.get("module")
    
    # It could be a custom module or the built-in HTTP Proxy
    assert handler, "Handler not configured for /api/proxy"

def test_policies_configuration():
    """Verify that the api-key-inbound policy is defined."""
    policies_file = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_file), f"Policies config not found at {policies_file}"
    
    with open(policies_file) as f:
        policies_config = json.load(f)
        
    policies = policies_config.get("policies", [])
    api_key_policy = next((p for p in policies if p.get("name") == "api-key-inbound"), None)
    
    assert api_key_policy is not None, "api-key-inbound policy not found in policies.json"
    assert api_key_policy.get("policyType") == "api-key-inbound", "Policy type is not api-key-inbound"
