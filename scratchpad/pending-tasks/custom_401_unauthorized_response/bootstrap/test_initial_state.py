import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}."

def test_zuplo_config_exists():
    config_path = os.path.join(PROJECT_DIR, "zuplo.jsonc")
    assert os.path.isfile(config_path), f"zuplo.jsonc not found at {config_path}."
