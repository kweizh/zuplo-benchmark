import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_policy_configured_correctly():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    with open(policies_path) as f:
        policies_data = json.load(f)
    
    policies = policies_data.get("policies", [])
    auth0_policy = next((p for p in policies if p.get("name") == "my-auth0-jwt-auth-inbound-policy"), None)
    
    assert auth0_policy is not None, "Policy 'my-auth0-jwt-auth-inbound-policy' not found in config/policies.json"
    assert auth0_policy.get("policyType") == "auth0-jwt-auth-inbound", "Policy type should be 'auth0-jwt-auth-inbound'"
    
    handler = auth0_policy.get("handler", {})
    assert handler.get("export") == "Auth0JwtInboundPolicy", "Handler export should be 'Auth0JwtInboundPolicy'"
    assert handler.get("module") == "$import(@zuplo/runtime)", "Handler module should be '$import(@zuplo/runtime)'"
    
    options = handler.get("options", {})
    assert options.get("auth0Domain") == "my-company.auth0.com", "options.auth0Domain should be 'my-company.auth0.com'"
    assert options.get("audience") == "https://api.example.com/", "options.audience should be 'https://api.example.com/'"

def test_route_has_policy_attached():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    with open(routes_path) as f:
        routes_data = json.load(f)
        
    protected_route = routes_data.get("paths", {}).get("/protected", {}).get("get", {})
    zuplo_route = protected_route.get("x-zuplo-route", {})
    inbound_policies = zuplo_route.get("policies", {}).get("inbound", [])
    
    assert "my-auth0-jwt-auth-inbound-policy" in inbound_policies, \
        "Policy 'my-auth0-jwt-auth-inbound-policy' must be added to the inbound policies of the /protected route."

def test_project_builds_successfully():
    result = subprocess.run(
        ["npm", "run", "build"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"Project failed to build: {result.stderr}\n{result.stdout}"
