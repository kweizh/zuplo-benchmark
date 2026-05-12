import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_routes_oas_json_exists():
    routes_path = os.path.join(PROJECT_DIR, "config", "routes.oas.json")
    assert os.path.isfile(routes_path), f"Routes config file {routes_path} does not exist."
    
    with open(routes_path) as f:
        routes = json.load(f)
        
    paths = routes.get("paths", {})
    assert "/graphql" in paths, "Expected '/graphql' route in routes.oas.json"
    
    graphql_route = paths["/graphql"]
    assert "post" in graphql_route or "POST" in graphql_route, "Expected POST method for '/graphql' route"
    
    post_route = graphql_route.get("post", graphql_route.get("POST"))
    zuplo_route = post_route.get("x-zuplo-route", {})
    
    handler = zuplo_route.get("handler", {})
    assert handler, "Expected handler configuration for '/graphql' route"
    
    # Check if handler exports url-forward or custom module that forwards to the correct URL
    # Or just check if the URL is somewhere in the config
    routes_str = json.dumps(routes)
    assert "countries.trevorblades.com" in routes_str, "Expected 'countries.trevorblades.com' in routes.oas.json"
    
    policies = zuplo_route.get("policies", {})
    inbound_policies = policies.get("inbound", [])
    
    assert len(inbound_policies) >= 2, "Expected at least 2 inbound policies (API key and disable introspection)"

def test_policies_json_exists():
    policies_path = os.path.join(PROJECT_DIR, "config", "policies.json")
    assert os.path.isfile(policies_path), f"Policies config file {policies_path} does not exist."
    
    with open(policies_path) as f:
        policies_config = json.load(f)
        
    policies = policies_config.get("policies", [])
    
    policy_types = [p.get("policyType") for p in policies]
    
    assert "api-key-inbound" in policy_types, "Expected 'api-key-inbound' policy in policies.json"
    assert "graphql-disable-introspection-inbound" in policy_types, "Expected 'graphql-disable-introspection-inbound' policy in policies.json"
