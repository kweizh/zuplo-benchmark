import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_npm_available():
    assert shutil.which("npm") is not None, "npm not found in PATH."

def test_npx_available():
    assert shutil.which("npx") is not None, "npx not found in PATH."
