# Zuplo Custom Response Header Policy

## Background
Zuplo is a serverless, programmable API gateway. You can use custom TypeScript policies to modify requests and responses. In this task, you will create a custom outbound policy that adds a signature header based on the response body.

## Requirements
- Scaffold a new Zuplo project named `myproject`.
- Create a route `GET /api/data` that returns a JSON response: `{"message": "hello edge"}`. You can use a standard handler or custom module for this.
- Create a custom outbound policy in TypeScript.
- The policy must read the response body, calculate the SHA-256 hash of the body text (as a hex string), and add it as the `x-response-signature` header to the response.
- Apply this policy to the `GET /api/data` route.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- To read the response body safely without consuming the original stream for the final response, use `response.clone()`.
- Use the standard Web Crypto API (`crypto.subtle.digest`) available in the edge runtime to calculate the SHA-256 hash. Convert the resulting ArrayBuffer to a hex string.
- Return a new `Response` object with the body and the updated headers.
- Configure the route in `config/routes.oas.json` and the policy in `config/policies.json`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8787
- API Endpoints:
  - GET `/api/data`: Returns status 200 and a JSON response containing `{"message": "hello edge"}`. The response MUST contain the `x-response-signature` header with the valid SHA-256 hex string of the exact response body returned.

