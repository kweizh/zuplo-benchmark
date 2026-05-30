import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_node_and_npm_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_project_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"File {package_json_path} does not exist."

def test_project_routes_config_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"File {routes_path} does not exist."
