import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
ROUTES_FILE = os.path.join(PROJECT_DIR, "config", "routes.oas.json")

def test_routes_file_exists():
    assert os.path.isfile(ROUTES_FILE), f"Routes file {ROUTES_FILE} does not exist."

def test_websocket_route_configured():
    with open(ROUTES_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {ROUTES_FILE}: {e}")
            
    assert "paths" in data, "Expected 'paths' in routes.oas.json"
    assert "/ws" in data["paths"], "Expected path '/ws' in routes.oas.json"
    
    ws_path = data["paths"]["/ws"]
    assert "get" in ws_path, "Expected 'get' method for '/ws' path"
    
    get_method = ws_path["get"]
    assert "x-zuplo-route" in get_method, "Expected 'x-zuplo-route' in 'get' method"
    
    route = get_method["x-zuplo-route"]
    assert route.get("corsPolicy") == "none", "Expected 'corsPolicy' to be 'none'"
    
    handler = route.get("handler", {})
    assert handler.get("export") == "webSocketHandler", "Expected handler 'export' to be 'webSocketHandler'"
    assert handler.get("module") == "$import(@zuplo/runtime)", "Expected handler 'module' to be '$import(@zuplo/runtime)'"
    
    options = handler.get("options", {})
    assert options.get("rewritePattern") == "wss://echo.websocket.org", "Expected handler 'options.rewritePattern' to be 'wss://echo.websocket.org'"
