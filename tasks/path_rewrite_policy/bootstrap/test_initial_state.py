import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."
