# Basic Proxy with Auth

## Background
Zuplo is an edge-native API gateway. You need to create a new Zuplo project that proxies requests to a public API and secures the route using a Zuplo-managed API Key.

## Requirements
- Initialize a new Zuplo project.
- Create a route `/api/proxy` that proxies all GET requests to `https://jsonplaceholder.typicode.com/todos/1`.
- Secure the route with the `api-key-inbound` policy.
- Ensure the project runs successfully locally.

## Implementation Hints
- Use `npx create-zuplo-api@latest` or `zuplo init` to scaffold the project.
- Configure the route in `config/routes.oas.json` to use a URL Rewrite or HTTP Proxy handler pointing to the public API.
- Add the `api-key-inbound` policy to the route's inbound policies.
- Verify your configuration by running the local development server.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8080
- API Endpoints:
  - GET `/api/proxy`: 
    - Without an API key (or invalid key), returns 401 Unauthorized.
    - With a valid API key, returns 200 OK and the proxied JSON response from jsonplaceholder.

