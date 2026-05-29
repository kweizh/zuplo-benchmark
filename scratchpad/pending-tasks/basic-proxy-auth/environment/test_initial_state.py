import os
import shutil
import pytest

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI is not installed or not in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm is not installed or not in PATH."

def test_npx_available():
    assert shutil.which("npx") is not None, "npx is not installed or not in PATH."

def test_project_dir_does_not_exist_yet():
    # The executor is supposed to create this directory, so it should not exist initially
    assert not os.path.exists("/home/user/myproject"), "Project directory /home/user/myproject should not exist before the task starts."
