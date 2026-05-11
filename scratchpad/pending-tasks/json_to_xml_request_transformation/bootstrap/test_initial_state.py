import os
import shutil
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/myproject"

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    pkg_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_json_path), f"package.json not found at {pkg_json_path}."
    
    with open(pkg_json_path) as f:
        data = json.load(f)
    
    assert "zuplo" in data.get("dependencies", {}) or "zuplo" in data.get("devDependencies", {}), "zuplo dependency not found in package.json."

def test_config_dir_exists():
    config_dir = os.path.join(PROJECT_DIR, "config")
    assert os.path.isdir(config_dir), f"config directory not found at {config_dir}."
    
    routes_path = os.path.join(config_dir, "routes.oas.json")
    assert os.path.isfile(routes_path), f"routes.oas.json not found at {routes_path}."
    
    policies_path = os.path.join(config_dir, "policies.json")
    assert os.path.isfile(policies_path), f"policies.json not found at {policies_path}."

def test_zuplo_jsonc_exists():
    zuplo_jsonc_path = os.path.join(PROJECT_DIR, "zuplo.jsonc")
    assert os.path.isfile(zuplo_jsonc_path), f"zuplo.jsonc not found at {zuplo_jsonc_path}."