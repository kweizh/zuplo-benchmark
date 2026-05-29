import pytest
import subprocess
import os
import socket
import requests
import time
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the Zuplo dev server using xprocess. Confirms readiness via port check.
    """
    class Starter(ProcessStarter):
        name = "zuplo_dev"
        args = ["bash", "-c", "npm install && npm run build && npx zuplo dev --editor-port 9200"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 300
        terminate_on_interrupt = True

        def startup_check(self):
            """
            Custom check: returns True if port 8787 is accepting connections.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 8787)) == 0

    xprocess.ensure(Starter.name, Starter)
    
    # Wait a little bit more after port is open to ensure the gateway is fully initialized
    time.sleep(2)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_mcp_tool_execution(start_app):
    """
    Verify the MCP tool execution by sending a POST request to /mcp.
    """
    url = "http://localhost:8787/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_customer_summary",
            "arguments": {
                "customerId": "123"
            }
        }
    }
    
    response = requests.post(url, json=payload, timeout=10)
    
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert data.get("jsonrpc") == "2.0", f"Expected jsonrpc 2.0, got: {data.get('jsonrpc')}"
    assert data.get("id") == 1, f"Expected id 1, got: {data.get('id')}"
    
    result = data.get("result")
    assert result is not None, "Response does not contain a 'result' object."
    assert "content" in result, "Result object does not contain 'content'."
    
    # Ensure there's some text returned
    content = result["content"]
    assert len(content) > 0, "Content array is empty."
    assert "text" in content[0], "Content does not contain text."
    
    text_val = content[0]["text"]
    assert isinstance(text_val, str) and len(text_val) > 0, "Summary text is missing or empty."
