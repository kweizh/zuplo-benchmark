import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
MODULES_DIR = os.path.join(PROJECT_DIR, "modules")
CONFIG_DIR = os.path.join(PROJECT_DIR, "config")

def test_routing_ts_exists():
    routing_path = os.path.join(MODULES_DIR, "routing.ts")
    assert os.path.isfile(routing_path), f"{routing_path} does not exist."
    
    with open(routing_path) as f:
        content = f.read()
    
    # Basic string checks for expected logic
    assert "request.user.data.environment" in content, "routing.ts does not read request.user.data.environment"
    assert "https://sandbox.example.com" in content, "routing.ts does not contain sandbox URL"
    assert "https://api.example.com" in content, "routing.ts does not contain production URL"
    assert "context.custom.downstreamUrl" in content, "routing.ts does not set context.custom.downstreamUrl"

def test_policies_json_valid():
    policies_path = os.path.join(CONFIG_DIR, "policies.json")
    assert os.path.isfile(policies_path), f"{policies_path} does not exist."
    
    with open(policies_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("policies.json is not valid JSON.")
            
    policies = data.get("policies", [])
    policy_names = [p.get("name") for p in policies]
    
    assert "api-key-auth" in policy_names, "api-key-auth policy is missing."
    assert "dynamic-routing" in policy_names, "dynamic-routing policy is missing."
    
    for p in policies:
        if p.get("name") == "dynamic-routing":
            assert "routing" in p.get("handler", {}).get("module", ""), "dynamic-routing does not reference routing module."

def test_routes_oas_json_valid():
    routes_path = os.path.join(CONFIG_DIR, "routes.oas.json")
    assert os.path.isfile(routes_path), f"{routes_path} does not exist."
    
    with open(routes_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("routes.oas.json is not valid JSON.")
            
    paths = data.get("paths", {})
    assert "/api/data" in paths, "Route /api/data is missing."
    
    get_method = paths["/api/data"].get("get", {})
    zuplo_route = get_method.get("x-zuplo-route", {})
    
    handler = zuplo_route.get("handler", {})
    assert handler.get("name") == "url-rewrite" or "url-rewrite" in handler.get("module", ""), "Handler is not url-rewrite."
    
    policies = zuplo_route.get("policies", {}).get("inbound", [])
    assert "api-key-auth" in policies, "api-key-auth is not in inbound policies."
    assert "dynamic-routing" in policies, "dynamic-routing is not in inbound policies."

def test_simulated_routing_logic():
    # We will write a small Node.js script that uses typescript to load the module and test it
    test_script_path = os.path.join(PROJECT_DIR, "test_runner.js")
    routing_path = os.path.join(MODULES_DIR, "routing.ts")
    
    script_content = f"""
    const fs = require('fs');
    const path = require('path');
    const {{execSync}} = require('child_process');

    try {{
        // We compile the TS file to JS to test it without tsx
        execSync('npx -y typescript tsc {routing_path} --target es2022 --module commonjs --esModuleInterop');
        const jsPath = '{routing_path}'.replace('.ts', '.js');
        const handler = require(jsPath).default || require(jsPath);

        async function runTest() {{
            // Test 1: Sandbox
            let context1 = {{ custom: {{}} }};
            let req1 = {{ user: {{ data: {{ environment: 'sandbox' }} }} }};
            await handler(req1, context1);
            if (context1.custom.downstreamUrl !== 'https://sandbox.example.com') throw new Error('Sandbox failed');

            // Test 2: Production
            let context2 = {{ custom: {{}} }};
            let req2 = {{ user: {{ data: {{ environment: 'production' }} }} }};
            await handler(req2, context2);
            if (context2.custom.downstreamUrl !== 'https://api.example.com') throw new Error('Production failed');

            // Test 3: Invalid
            let context3 = {{ custom: {{}} }};
            let req3 = {{ user: {{ data: {{ environment: 'invalid' }} }} }};
            let res3 = await handler(req3, context3);
            if (!res3 || res3.status !== 400) throw new Error('Invalid environment did not return 400');
            
            console.log('SUCCESS');
        }}
        
        runTest().catch(e => {{ console.error(e.message); process.exit(1); }});
    }} catch (e) {{
        console.error("Compilation or execution failed: " + e.message);
        process.exit(1);
    }}
    """
    
    with open(test_script_path, "w") as f:
        f.write(script_content)
        
    result = subprocess.run(
        ["node", test_script_path],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert "SUCCESS" in result.stdout, f"Simulated test failed: {result.stderr} {result.stdout}"
