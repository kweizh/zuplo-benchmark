# IP Whitelisting Policy

## Background
Create a Zuplo API gateway that restricts access to an endpoint based on the client's IP address. You will implement a custom inbound policy to validate the IP against a whitelist.

## Requirements
- Initialize a new Zuplo project in `/home/user/myproject`.
- Create a `GET /hello` route.
- Implement a custom inbound policy named `ip-whitelist-inbound` that checks the `x-test-ip` header (to simulate the client IP for testing).
- The policy must read a comma-separated list of allowed IPs from the `ALLOWED_IPS` environment variable.
- If the `x-test-ip` value is in the allowed list, the request should proceed to the handler.
- If the `x-test-ip` value is missing or not in the allowed list, the policy must return a 403 Forbidden status with a JSON body `{"error": "Forbidden IP"}`.
- The route handler for `/hello` should return a 200 OK status with a JSON body `{"message": "Hello from the edge!"}`.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Define the route in `config/routes.oas.json`.
- Define the policy in `config/policies.json`.
- Write the policy module in `modules/ip-whitelist.ts` (or similar).
- Write the handler module in `modules/hello.ts`.
- Use `ZuploRequest` and `ZuploContext` in your custom modules.
- Read environment variables using `process.env.ALLOWED_IPS` or `context.environmentVariables`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8787
- API Endpoints:
  - GET `/hello`:
    - If `x-test-ip` is allowed: Returns status 200 and JSON `{"message": "Hello from the edge!"}`.
    - If `x-test-ip` is not allowed or missing: Returns status 403 and JSON `{"error": "Forbidden IP"}`.
