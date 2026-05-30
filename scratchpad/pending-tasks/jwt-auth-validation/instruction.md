# Zuplo JWT Auth Validation

## Background
Zuplo is an edge-native API gateway that allows you to add authentication and routing to your APIs using a GitOps-based workflow and TypeScript. In this task, you will create a custom inbound policy to validate JSON Web Tokens (JWT).

## Requirements
- Initialize a new Zuplo project in `/home/user/myproject`.
- Create a single route: `GET /protected`.
- Implement a custom inbound policy in TypeScript that intercepts requests to `/protected`.
- The custom policy must read the `Authorization` header and extract a Bearer token.
- The policy must validate the JWT token's signature using the HMAC SHA-256 algorithm. The secret key for validation is provided in the `JWT_SECRET` environment variable.
- If the token is valid, allow the request to proceed and return a JSON response: `{"message": "Hello, authenticated user!"}`.
- If the token is missing, malformed, or has an invalid signature, the policy must reject the request and return a `401 Unauthorized` status.

## Implementation Hints
- Use `npx create-zuplo-api` to scaffold the project.
- You can use a library like `jose` (which is compatible with edge runtimes) to verify the JWT signature, or use the Web Crypto API directly.
- Remember that Zuplo runs on an edge runtime (similar to Cloudflare Workers), so Node.js native modules like `crypto` are not available.
- Create a custom inbound policy module (e.g., in `modules/`) and configure it in `config/policies.json` and `config/routes.oas.json`.
- To access environment variables in a Zuplo policy, use `context.env.JWT_SECRET`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev -- --port 3000
- Port: 3000
- API Endpoints:
  - GET `/protected`:
    - Request headers: `Authorization: Bearer <valid_jwt>`
    - Valid JWT Response: Status 200 OK, Body: `{"message": "Hello, authenticated user!"}`
    - Invalid/Missing JWT Response: Status 401 Unauthorized

