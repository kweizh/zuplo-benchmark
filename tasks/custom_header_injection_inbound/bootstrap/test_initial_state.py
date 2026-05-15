import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_config_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config file {routes_path} does not exist."

def test_policies_config_exists():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Policies config file {policies_path} does not exist."

def test_hello_module_exists():
    hello_path = os.path.join(PROJECT_DIR, "modules", "hello.ts")
    assert os.path.isfile(hello_path), f"Hello module {hello_path} does not exist."
