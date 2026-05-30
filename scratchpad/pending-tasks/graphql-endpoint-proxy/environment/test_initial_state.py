import os
import shutil

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_zuplo_available():
    assert shutil.which("zuplo") is not None, "zuplo CLI not found in PATH."

def test_home_directory_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."
