import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_cors_policy_in_policies_json():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Config file {policies_path} does not exist."

    with open(policies_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{policies_path} is not valid JSON.")

    assert "corsPolicies" in data, "No 'corsPolicies' array found in policies.json."
    cors_policies = data["corsPolicies"]
    assert isinstance(cors_policies, list), "'corsPolicies' must be an array."

    my_policy = next((p for p in cors_policies if p.get("name") == "my-cors-policy"), None)
    assert my_policy is not None, "CORS policy 'my-cors-policy' not found in corsPolicies."

    # Verify allowedOrigins
    allowed_origins = my_policy.get("allowedOrigins", [])
    if isinstance(allowed_origins, str):
        allowed_origins = [o.strip() for o in allowed_origins.split(",")]
    assert "https://app.example.com" in allowed_origins, "'https://app.example.com' missing from allowedOrigins."
    assert "http://localhost:3000" in allowed_origins, "'http://localhost:3000' missing from allowedOrigins."

    # Verify allowedMethods
    allowed_methods = my_policy.get("allowedMethods", [])
    if isinstance(allowed_methods, str):
        allowed_methods = [m.strip() for m in allowed_methods.split(",")]
    assert "GET" in allowed_methods, "'GET' missing from allowedMethods."
    assert "POST" in allowed_methods, "'POST' missing from allowedMethods."

    # Verify allowedHeaders
    allowed_headers = my_policy.get("allowedHeaders", [])
    if isinstance(allowed_headers, str):
        allowed_headers = [h.strip() for h in allowed_headers.split(",")]
    assert "Authorization" in allowed_headers, "'Authorization' missing from allowedHeaders."
    assert "Content-Type" in allowed_headers, "'Content-Type' missing from allowedHeaders."

    # Verify allowCredentials
    assert my_policy.get("allowCredentials") is True, "allowCredentials must be true."

def test_cors_policy_applied_to_route():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Config file {routes_path} does not exist."

    with open(routes_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{routes_path} is not valid JSON.")

    paths = data.get("paths", {})
    hello_route = paths.get("/hello", {})
    get_method = hello_route.get("get", {})
    x_zuplo_route = get_method.get("x-zuplo-route", {})

    assert "corsPolicy" in x_zuplo_route, "'corsPolicy' not found in x-zuplo-route for GET /hello."
    assert x_zuplo_route["corsPolicy"] == "my-cors-policy", f"Expected corsPolicy to be 'my-cors-policy', got '{x_zuplo_route['corsPolicy']}'."
