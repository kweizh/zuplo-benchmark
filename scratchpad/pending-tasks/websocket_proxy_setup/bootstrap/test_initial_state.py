import os
import shutil
import pytest
import json

PROJECT_DIR = "/home/user/myproject"

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_file_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes file {routes_path} does not exist."

def test_initial_routes_is_empty():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        data = json.load(f)
    assert "paths" in data, "Expected 'paths' in routes.oas.json."
    assert len(data["paths"]) == 0, "Expected initial paths to be empty."
