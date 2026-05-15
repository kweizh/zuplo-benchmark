import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_file_exists():
    routes_file = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_file), f"Routes file {routes_file} does not exist."

def test_policies_file_exists():
    policies_file = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_file), f"Policies file {policies_file} does not exist."
