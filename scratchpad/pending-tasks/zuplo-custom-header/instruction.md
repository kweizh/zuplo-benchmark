# Zuplo Custom Response Header Policy

## Background
Zuplo is a serverless API gateway that allows you to add custom logic using TypeScript policies. In this task, you will implement a custom outbound policy that reads the response body and adds a signature header before returning it to the client.

## Requirements
- Initialize a new Zuplo project.
- Create a route `GET /hello` that returns a simple JSON or text response.
- Implement a custom outbound policy (e.g., in `./modules/signature-outbound.ts`).
- The policy must read the response body and add a custom HTTP header named `x-signature` to the response.
- The value of `x-signature` must be the Base64 encoded string of the response body.
- Apply this outbound policy to the `/hello` route.

## Implementation Hints
- Use `zuplo init` to scaffold the project.
- In Zuplo, custom policies receive `ZuploRequest`, `ZuploContext`, and the `Response` object (for outbound policies). Or you can intercept the response in a handler.
- Remember that reading the response body consumes it. You must use `response.clone()` if you need to read the body and still return it.
- Use the standard `btoa()` function available in the edge runtime to encode the body to Base64.
- Register your policy in `config/policies.json` and attach it to the route's `outbound` policies in `config/routes.oas.json`.

## Acceptance Criteria
- Project path: /home/user/zuplo-project
- Start command: zuplo dev
- Port: 8787
- API Endpoints:
  - GET `/hello`: Returns a 200 status. The response MUST contain a custom header `x-signature` containing the Base64 encoded string of the exact response body.

