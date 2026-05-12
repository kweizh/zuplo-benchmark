import os
import pytest

PROJECT_DIR = "/home/user/myproject"
RUNTIME_FILE = os.path.join(PROJECT_DIR, "modules/zuplo.runtime.ts")

def test_runtime_file_exists():
    assert os.path.isfile(RUNTIME_FILE), f"The file {RUNTIME_FILE} does not exist."

def test_datadog_plugin_configured():
    with open(RUNTIME_FILE, "r") as f:
        content = f.read()

    assert "runtimeInit" in content, "The file must export a 'runtimeInit' function."
    assert "DataDogLoggingPlugin" in content, "The 'DataDogLoggingPlugin' must be imported and used."
    assert "runtime.addPlugin" in content or "runtime.plugins.add" in content, "The plugin must be registered using 'runtime.addPlugin'."
    
    # Check for specific configuration options
    assert "process.env.DATADOG_API_KEY" in content, "The 'apiKey' must use 'process.env.DATADOG_API_KEY'."
    assert "zuplo-gateway" in content, "The 'source' option must be set to 'zuplo-gateway'."
    assert "env:" in content and "production" in content, "The 'tags' option must include 'env: production'."
