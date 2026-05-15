import os
import json
import pytest

PROJECT_DIR = "/home/user/my-zuplo-api"

def test_mock_handler_exists_and_returns_correct_json():
    handler_path = os.path.join(PROJECT_DIR, "modules", "mock-handler.ts")
    assert os.path.isfile(handler_path), f"Handler file {handler_path} does not exist."
    
    with open(handler_path, "r") as f:
        content = f.read()
    
    assert '"status"' in content and '"success"' in content, "Handler does not contain the correct 'status' field."
    assert "data" in content and "1" in content and "2" in content and "3" in content, "Handler does not contain the correct 'data' array."

def test_routes_config_has_mock_data_route():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config file {routes_path} does not exist."
    
    with open(routes_path, "r") as f:
        try:
            routes = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("routes.oas.json is not valid JSON.")
            
    paths = routes.get("paths", {})
    assert "/mock-data" in paths, "Route '/mock-data' is not defined in routes.oas.json."
    
    mock_route = paths["/mock-data"]
    assert "get" in mock_route, "GET method is not defined for '/mock-data'."
    
    get_route = mock_route["get"]
    assert "x-zuplo-route" in get_route, "'x-zuplo-route' extension is missing for GET '/mock-data'."
    
    zuplo_route = get_route["x-zuplo-route"]
    assert "handler" in zuplo_route, "Handler is not defined in 'x-zuplo-route'."
    
    handler = zuplo_route["handler"]
    assert "module" in handler, "Handler module is not defined."
    assert "mock-handler" in handler["module"], f"Handler module does not reference 'mock-handler'. Got: {handler['module']}"
