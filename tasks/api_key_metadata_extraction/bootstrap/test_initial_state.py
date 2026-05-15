import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/my-zuplo-api"

def test_zuplo_binary_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_mock_auth_policy_exists():
    mock_auth_path = os.path.join(PROJECT_DIR, "modules", "mock-auth.ts")
    assert os.path.isfile(mock_auth_path), f"Mock auth policy {mock_auth_path} does not exist."

def test_routes_oas_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config {routes_path} does not exist."
    with open(routes_path) as f:
        content = f.read()
    assert "/api/data" in content, "Expected /api/data route in routes.oas.json."

def test_policies_json_exists():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Policies config {policies_path} does not exist."
    with open(policies_path) as f:
        content = f.read()
    assert "mock-auth" in content, "Expected mock-auth policy in policies.json."