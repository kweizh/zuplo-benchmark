import os
import subprocess
import time
import requests
import signal

def test_dynamic_environment_variable_usage():
    project_path = "/home/user/myproject"
    
    # Check if project exists
    assert os.path.exists(project_path), "Project directory does not exist."
    
    # Check if .env exists
    env_path = os.path.join(project_path, ".env")
    assert os.path.exists(env_path), ".env file does not exist."
    
    with open(env_path, "r") as f:
        env_content = f.read()
        assert "BACKEND_URL" in env_content, "BACKEND_URL not found in .env"
        assert "API_KEY" in env_content, "API_KEY not found in .env"
    
    # Start the dev server
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=project_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    try:
        # Wait for server to start
        server_ready = False
        for _ in range(30):
            try:
                response = requests.get("http://localhost:8787/custom", timeout=1)
                if response.status_code == 200:
                    server_ready = True
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)
                
        assert server_ready, "Zuplo dev server did not start in time."
        
        # Test /forward
        forward_response = requests.get("http://localhost:8787/forward", timeout=5)
        assert forward_response.status_code == 200, f"Expected 200 for /forward, got {forward_response.status_code}"
        # The echo service usually returns JSON with the path
        forward_data = forward_response.json()
        assert forward_data.get("url") == "https://echo.zuplo.io/forward", "Forward handler did not proxy to the correct URL."
        
        # Test /custom
        custom_response = requests.get("http://localhost:8787/custom", timeout=5)
        assert custom_response.status_code == 200, f"Expected 200 for /custom, got {custom_response.status_code}"
        custom_data = custom_response.json()
        assert custom_data.get("key") == "secret_123", f"Expected key 'secret_123', got {custom_data.get('key')}"
        
    finally:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait()
