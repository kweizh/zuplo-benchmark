import os
import subprocess
import time
import socket
import json
import pytest

DB_SERVER_DIR = "/home/user/db-server"
ZUPLO_DIR = "/home/user/zuplo-mcp"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def start_servers():
    # Start DB server
    db_process = subprocess.Popen(
        ["node", "server.js"],
        cwd=DB_SERVER_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Start Zuplo server
    zuplo_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=ZUPLO_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for both ports
    db_ready = wait_for_port(8080)
    zuplo_ready = wait_for_port(3000)

    if not db_ready or not zuplo_ready:
        import signal
        if db_process.poll() is None:
            os.killpg(os.getpgid(db_process.pid), signal.SIGTERM)
        if zuplo_process.poll() is None:
            os.killpg(os.getpgid(zuplo_process.pid), signal.SIGTERM)
        pytest.fail("Servers failed to start and listen on required ports.")

    yield

    # Shut down servers
    import signal
    if db_process.poll() is None:
        os.killpg(os.getpgid(db_process.pid), signal.SIGTERM)
    if zuplo_process.poll() is None:
        os.killpg(os.getpgid(zuplo_process.pid), signal.SIGTERM)

def test_db_server_directly(start_servers):
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8080/sales?region=US"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl to DB server failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert isinstance(data, list) and len(data) == 2, f"Expected 2 items for US, got: {data}"
    assert data[0].get("amount") == 100, f"Expected amount 100, got: {data}"

def test_internal_route_protected(start_servers):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:3000/internal/sales?region=US"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "401", f"Expected 401 Unauthorized, got: {result.stdout}"

def test_internal_route_with_auth(start_servers):
    result = subprocess.run(
        ["curl", "-s", "-H", "Authorization: Bearer secret-internal-key", "http://localhost:3000/internal/sales?region=US"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl to Zuplo internal route failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert isinstance(data, list) and len(data) == 2, f"Expected 2 items for US, got: {data}"

def test_mcp_server_auth(start_servers):
    payload = json.dumps({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/mcp"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "401", f"Expected 401 Unauthorized for MCP without auth, got: {result.stdout}"

def test_mcp_server_tool_list(start_servers):
    payload = json.dumps({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/mcp?apiKey=secret-mcp-key"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl to MCP tools/list failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert "result" in data, f"Expected jsonrpc result, got: {data}"
    tools = data["result"].get("tools", [])
    tool_names = [t.get("name") for t in tools]
    assert "summarize_sales" in tool_names, f"Expected 'summarize_sales' tool, got: {tool_names}"

def test_mcp_tool_execution(start_servers):
    payload = json.dumps({
        "jsonrpc": "2.0", 
        "method": "tools/call", 
        "id": 2, 
        "params": {
            "name": "summarize_sales", 
            "arguments": {"region": "US"}
        }
    })
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json", "-d", payload, "http://localhost:3000/mcp?apiKey=secret-mcp-key"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl to MCP tools/call failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert "result" in data, f"Expected jsonrpc result, got: {data}"
    content = data["result"].get("content", [])
    assert len(content) > 0, f"Expected content in tool result, got: {data}"
    
    # The content text should be a JSON string
    text_content = content[0].get("text", "")
    try:
        parsed_text = json.loads(text_content)
        assert parsed_text.get("region") == "US", f"Expected region US, got: {parsed_text}"
        assert parsed_text.get("totalSales") == 300, f"Expected totalSales 300, got: {parsed_text}"
    except json.JSONDecodeError:
        # If it's not JSON, check if it contains the correct values
        assert "US" in text_content and "300" in text_content, f"Expected US and 300 in text content, got: {text_content}"
