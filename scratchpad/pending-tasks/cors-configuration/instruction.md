# Zuplo CORS Configuration

## Background
Cross-Origin Resource Sharing (CORS) is a critical security feature for APIs accessed from web browsers. You need to configure a custom CORS policy for a Zuplo API gateway to securely allow requests from a specific frontend application.

## Requirements
- Initialize a new Zuplo project in `/home/user/myproject`.
- Create a route `/api/data` that accepts `GET` requests and returns a JSON response: `{"message": "Hello CORS"}`.
- Configure a CORS policy and apply it to the `/api/data` route.
- The CORS policy must allow the origin `https://example-${run-id}.com` (where `${run-id}` is read from the `ZEALT_RUN_ID` environment variable).
- The CORS policy must allow the methods `GET` and `OPTIONS`.
- The CORS policy must allow the headers `Content-Type` and `Authorization`.

## Implementation Hints
- Use the Zuplo CLI to scaffold a new project (`create-zuplo-api`).
- Define the route in `config/routes.oas.json`.
- Define the CORS policy in `config/policies.json`. You can use Zuplo's built-in `cors-inbound` policy type and configure its `options` with the required allowed origins, methods, and headers.
- Apply the CORS policy to the `/api/data` route in the OpenAPI file.
- Ensure you read the `ZEALT_RUN_ID` environment variable to dynamically construct the allowed origin in the configuration. (You may need to write a custom TypeScript policy or a custom handler if Zuplo's JSON config doesn't support reading environment variables directly for CORS origins, or you can use a custom TS policy that handles the CORS headers manually by checking the Origin header and `process.env.ZEALT_RUN_ID`).
*Note: Since policies.json is static, a custom TypeScript inbound policy is the recommended way to dynamically read the environment variable and set the CORS headers on the response.*

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: zuplo dev --port 3000
- Port: 3000
- API Endpoints:
  - `OPTIONS /api/data`:
    - Request Header: `Origin: https://example-${run-id}.com`
    - Response Status: 200 or 204
    - Response Headers must include:
      - `Access-Control-Allow-Origin: https://example-${run-id}.com`
      - `Access-Control-Allow-Methods` containing `GET` and `OPTIONS`
      - `Access-Control-Allow-Headers` containing `Content-Type` and `Authorization`
  - `GET /api/data`:
    - Request Header: `Origin: https://example-${run-id}.com`
    - Response Status: 200
    - Response Header must include: `Access-Control-Allow-Origin: https://example-${run-id}.com`
    - Response Body: `{"message": "Hello CORS"}`
  - `GET /api/data` (Invalid Origin):
    - Request Header: `Origin: https://evil.com`
    - Response Header `Access-Control-Allow-Origin` should NOT be `https://evil.com` (it can be missing or restricted).

