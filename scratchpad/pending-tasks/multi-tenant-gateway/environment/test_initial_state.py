import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json not found at {package_json}."

def test_zuplo_json_exists():
    zuplo_json = os.path.join(PROJECT_DIR, "zuplo.json")
    assert os.path.isfile(zuplo_json), f"zuplo.json not found at {zuplo_json}."