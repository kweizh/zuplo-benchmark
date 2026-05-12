import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/my-zuplo-api"

def test_module_resolution_fixed():
    """Priority 3 fallback: check the file content since there's no CLI command to verify just the file content."""
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        data = json.load(f)
    
    module_path = data["paths"]["/hello"]["get"]["x-zuplo-route"]["handler"]["module"]
    assert module_path == "$import(./modules/hello-world)", \
        f"Expected module path to be '$import(./modules/hello-world)', got: {module_path}"

def test_zuplo_build_succeeds():
    """Priority 1: Use Zuplo CLI (via npm run build or npx zuplo build) to verify the project builds successfully."""
    # Run npx zuplo build
    result = subprocess.run(
        ["npx", "zuplo", "build"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, \
        f"'npx zuplo build' failed: {result.stderr}\n{result.stdout}"
