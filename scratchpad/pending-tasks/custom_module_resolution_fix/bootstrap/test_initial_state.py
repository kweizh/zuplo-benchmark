import os
import shutil
import subprocess
import pytest
import json

PROJECT_DIR = "/home/user/my-zuplo-api"

def test_zuplo_binary_available():
    assert shutil.which("npx") is not None, "npx binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_file_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config file {routes_path} does not exist."

def test_hello_world_module_exists():
    module_path = os.path.join(PROJECT_DIR, "modules", "hello-world.ts")
    assert os.path.isfile(module_path), f"Module file {module_path} does not exist."

def test_initial_module_resolution_is_incorrect():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        data = json.load(f)
    
    module_path = data["paths"]["/hello"]["get"]["x-zuplo-route"]["handler"]["module"]
    assert module_path == "$import(hello-world)", \
        f"Expected initial module path to be '$import(hello-world)', got: {module_path}"
