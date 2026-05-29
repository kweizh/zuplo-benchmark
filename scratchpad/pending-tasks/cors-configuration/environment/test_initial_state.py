import os
import shutil

def test_zuplo_cli_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_npm_npx_available():
    assert shutil.which("npm") is not None, "npm not found in PATH."
    assert shutil.which("npx") is not None, "npx not found in PATH."

def test_home_dir_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
