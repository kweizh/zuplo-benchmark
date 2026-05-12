import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_policies_file_exists():
    config_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(config_path), f"Policies file {config_path} does not exist."

def test_routes_file_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes file {routes_path} does not exist."

def test_hello_route_exists_in_initial_state():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        routes = json.load(f)
    
    assert "/hello" in routes.get("paths", {}), "Expected '/hello' path in routes.oas.json."
    assert "get" in routes["paths"]["/hello"], "Expected 'get' method for '/hello' path."
    assert "x-zuplo-route" in routes["paths"]["/hello"]["get"], "Expected 'x-zuplo-route' in '/hello' get method."
