# Custom Auth Policy in Zuplo

## Background
You need to implement a custom authentication policy for a Zuplo API Gateway that validates a proprietary token format.

## Requirements
- Create a new Zuplo project at `/home/user/myproject`.
- Implement a custom inbound policy in TypeScript that checks the `Authorization` header.
- The header must be in the format `CustomToken <token>`.
- The `<token>` must exactly match `secret-token-${run-id}` (read `run-id` from the `ZEALT_RUN_ID` environment variable).
- If the token is valid, allow the request to proceed to a handler that returns a 200 OK response with the body `Hello, authenticated user!`.
- If the header is missing, incorrectly formatted, or the token is invalid, return a 401 Unauthorized status with a JSON body `{"error": "Unauthorized"}`.
- Apply this custom policy to a `GET /protected` route.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Create a custom TypeScript module in the `modules/` directory for your policy.
- Configure the policy in `config/policies.json` and apply it to the route in `config/routes.oas.json`.
- You can use a simple custom handler for the route response, or just a mock response policy.
- Zuplo's local dev server typically runs the API on port 8787.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8787
- API Endpoints:
  - GET `/protected`: Protected endpoint that requires the custom token.
    - Request Header: `Authorization: CustomToken secret-token-${run-id}`
    - Success Response: 200 OK with text `Hello, authenticated user!`
    - Failure Response: 401 Unauthorized with JSON `{"error": "Unauthorized"}`

