import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_rate_limit_policy_configured():
    """Priority 3: Verify the policy is correctly configured in policies.json."""
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Policies file {policies_path} not found."
    
    with open(policies_path) as f:
        data = json.load(f)
        
    policies = data.get("policies", [])
    
    ip_policy = next((p for p in policies if p.get("name") == "ip-rate-limit"), None)
    assert ip_policy is not None, "Expected policy named 'ip-rate-limit' in policies.json."
    
    assert ip_policy.get("policyType") == "rate-limit-inbound", \
        f"Expected policyType 'rate-limit-inbound', got {ip_policy.get('policyType')}"
        
    options = ip_policy.get("handler", {}).get("options", {})
    
    assert options.get("rateLimitBy") == "ip", \
        f"Expected rateLimitBy to be 'ip', got {options.get('rateLimitBy')}"
        
    assert options.get("requestsAllowed") == 5, \
        f"Expected requestsAllowed to be 5, got {options.get('requestsAllowed')}"
        
    assert options.get("timeWindowMinutes") == 1, \
        f"Expected timeWindowMinutes to be 1, got {options.get('timeWindowMinutes')}"

def test_route_has_policy_applied():
    """Priority 3: Verify the policy is applied to the route in routes.oas.json."""
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes file {routes_path} not found."
    
    with open(routes_path) as f:
        data = json.load(f)
        
    try:
        route = data["paths"]["/hello"]["get"]["x-zuplo-route"]
        inbound_policies = route.get("policies", {}).get("inbound", [])
    except KeyError as e:
        pytest.fail(f"Could not find expected route structure in routes.oas.json: missing {e}")
        
    assert "ip-rate-limit" in inbound_policies, \
        f"Expected 'ip-rate-limit' in inbound policies for /hello route, got {inbound_policies}"
