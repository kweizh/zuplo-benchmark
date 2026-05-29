import os
import shutil

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found in {PROJECT_DIR}."

def test_zuplo_config_exists():
    config_path = os.path.join(PROJECT_DIR, "zuplo.jsonc")
    assert os.path.isfile(config_path), f"zuplo.jsonc not found in {PROJECT_DIR}."
