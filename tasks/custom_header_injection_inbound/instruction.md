# Custom Header Injection Policy

## Background
Zuplo is a programmable API gateway that uses custom policies to modify requests. You have a basic Zuplo project at `/home/user/myproject` with a single route `GET /hello`.

## Requirements
- Create a custom inbound policy that injects a new header `x-custom-injected: Zuplo-Rules` into incoming requests.
- Apply this policy to the `GET /hello` route.
- Ensure the handler for `/hello` echoes back all request headers as a JSON response so we can verify the injection.

## Implementation Guide
1. In `/home/user/myproject`, create a custom inbound policy module at `modules/custom-header.ts`.
2. The policy should create a new `ZuploRequest`, add the header `x-custom-injected: Zuplo-Rules`, and return the modified request.
3. Register the policy in `config/policies.json` with the name `custom-header-inbound` and `policyType: custom-code-inbound`.
4. Apply the policy to the `GET /hello` route in `config/routes.oas.json`.
5. Update the handler for `GET /hello` (e.g., `modules/hello.ts`) to return the request headers as a JSON response (`Object.fromEntries(request.headers)`).

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev`
- Port: 8787