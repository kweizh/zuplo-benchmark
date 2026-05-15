# Multi-Tenant Routing based on API Key Metadata

## Background
Zuplo is an edge-native API gateway that allows you to easily add authentication and custom routing logic. In this task, you will implement a multi-tenant API gateway configuration that routes requests to different backend environments (sandbox or production) based on the user's API key metadata.

## Requirements
1. Create a custom inbound policy in `modules/routing.ts` that:
   - Reads `request.user.data.environment`.
   - If `environment` is `"sandbox"`, sets `context.custom.downstreamUrl` to `"https://sandbox.example.com"`.
   - If `environment` is `"production"`, sets `context.custom.downstreamUrl` to `"https://api.example.com"`.
   - If `environment` is missing or invalid, returns a 400 Bad Request response with the text `"Invalid environment"`.
2. Configure `config/policies.json` to define:
   - An `api-key-inbound` policy named `api-key-auth` using the built-in `@zuplo/runtime` handler `ApiKeyInboundPolicy`.
   - A custom inbound policy named `dynamic-routing` that uses the `routing.ts` module.
3. Configure `config/routes.oas.json` to define a `GET /api/data` route:
   - Uses the built-in `url-rewrite` handler to forward the request to `${context.custom.downstreamUrl}/data`.
   - Applies the `api-key-auth` and `dynamic-routing` policies in that order.

## Implementation Guide
1. Create the necessary directories: `mkdir -p /home/user/myproject/modules /home/user/myproject/config`.
2. Write the custom policy code in `/home/user/myproject/modules/routing.ts`.
3. Create `/home/user/myproject/config/policies.json` with the required policies.
4. Create `/home/user/myproject/config/routes.oas.json` defining the path `/api/data` and the required `x-zuplo-route` configuration.

## Constraints
- Project path: /home/user/myproject
- Ensure you use the correct Zuplo module resolution syntax (e.g., `$import(./modules/routing)` or `$import(@zuplo/runtime)`).
- Use TypeScript for the custom policy.
