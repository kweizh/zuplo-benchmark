import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_zuplo_project_initialized():
    config_path = os.path.join(PROJECT_DIR, "zuplo.jsonc")
    assert os.path.isfile(config_path), f"Zuplo config file {config_path} does not exist."
