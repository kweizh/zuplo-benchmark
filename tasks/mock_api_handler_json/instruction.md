# Mock API Handler with JSON Response

## Background
Zuplo allows developers to create custom request handlers using TypeScript. You need to create a mock endpoint that returns a specific JSON payload for frontend testing.

## Requirements
- You have an existing Zuplo project at `/home/user/my-zuplo-api`.
- Create a custom handler in `modules/mock-handler.ts` that returns a JSON response: `{"status": "success", "data": [1, 2, 3]}`.
- Update `config/routes.oas.json` to add a `GET /mock-data` route that uses this custom handler.

## Implementation Guide
1. Navigate to `/home/user/my-zuplo-api`.
2. Create `modules/mock-handler.ts` and write a default export function that returns a `Response` object with the required JSON and a `Content-Type: application/json` header.
3. Modify `config/routes.oas.json` to define the `/mock-data` path for the `get` method, binding it to the custom handler using the `x-zuplo-route` extension.

## Constraints
- Project path: /home/user/my-zuplo-api
- The handler must return a standard web `Response` object with JSON data.
- Do not use any external dependencies in the handler.