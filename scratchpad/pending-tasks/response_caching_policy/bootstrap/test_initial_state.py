import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo binary not found in PATH."

def test_node_npm_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_config_files_exist():
    routes_path = os.path.join(PROJECT_DIR, "config/routes.oas.json")
    policies_path = os.path.join(PROJECT_DIR, "config/policies.json")
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    
    assert os.path.isfile(routes_path), f"Routes file {routes_path} does not exist."
    assert os.path.isfile(policies_path), f"Policies file {policies_path} does not exist."
    assert os.path.isfile(package_json_path), f"package.json {package_json_path} does not exist."
