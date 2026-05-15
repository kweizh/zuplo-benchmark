import os
import shutil
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/zuplo-project"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo binary not found in PATH."

def test_node_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_file_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config {routes_path} does not exist."
    with open(routes_path) as f:
        data = json.load(f)
    assert "/hello" in data.get("paths", {}), "Expected '/hello' route in routes.oas.json."

def test_policies_file_exists():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Policies config {policies_path} does not exist."
