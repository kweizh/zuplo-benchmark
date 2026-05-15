import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_policies_json_exists():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Config file {policies_path} does not exist."

def test_routes_oas_json_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Config file {routes_path} does not exist."
