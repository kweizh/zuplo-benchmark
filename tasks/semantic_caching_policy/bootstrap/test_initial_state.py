import os
import shutil
import subprocess
import pytest

def test_npx_binary_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_npm_binary_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."
