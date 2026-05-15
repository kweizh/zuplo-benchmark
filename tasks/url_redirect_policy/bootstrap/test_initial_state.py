import os
import shutil
import pytest

PROJECT_DIR = "/home/user/my-zuplo-api"

def test_zuplo_binary_available():
    assert shutil.which("zuplo") is not None, "zuplo binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_config_exists():
    config_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(config_path), f"Routes config file {config_path} does not exist."
