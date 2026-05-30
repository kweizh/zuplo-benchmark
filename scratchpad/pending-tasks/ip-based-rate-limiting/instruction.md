# IP-Based Rate Limiting with Zuplo

## Background
Zuplo is an edge-native API gateway that allows you to easily configure rate limiting policies to protect your API from abuse. In this task, you will create a simple API gateway that rate limits requests based on the client's IP address.

## Requirements
- Initialize a new Zuplo project named `myproject`.
- Create a GET `/api/data` route that returns a JSON response `{"status": "success"}`.
- Apply a rate limiting policy to the `/api/data` route.
- The rate limit must be exactly 2 requests per minute per IP address.
- Requests exceeding the limit should receive a 429 Too Many Requests response.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Configure `config/routes.oas.json` to define the `/api/data` route and attach the rate limiting policy to it.
- Define the rate limiting policy in `config/policies.json` using the built-in `rate-limit-inbound` policy type.
- Set the `rateLimitBy` property in the policy configuration to identify requests by IP.
- Use `zuplo dev --editor-port 9200` to start the dev server, as the default port 9100 might conflict with other services in the environment.
- **IMPORTANT**: You must kill the background dev server process before completing the task.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev -- --editor-port 9200
- Port: 9000
- API Endpoints:
  - GET `/api/data`: 
    - First 2 requests within a minute return HTTP status 200 and `{"status": "success"}`.
    - The 3rd request within a minute returns HTTP status 429 Too Many Requests.

