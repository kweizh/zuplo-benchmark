# Multi-Tenant Routing via API Key Metadata

## Background
You have a Zuplo API project at `/home/user/my-zuplo-api`. The project has a route `GET /api/data`. Currently, the route is protected by a custom `mock-auth` policy (already configured) which simulates API Key authentication by setting `request.user.data.tenantId` based on an incoming test header.

Your task is to implement a multi-tenant backend routing policy that reads this metadata and dynamically sets the downstream URL, while also injecting a header for the backend to use.

## Requirements
1. Create a custom inbound policy in `modules/tenant-routing.ts`.
2. The policy should extract `tenantId` from `request.user.data.tenantId`.
3. If `tenantId` is absent or `request.user` is undefined, return a `400 Bad Request` with JSON `{"error": "Missing tenantId"}`.
4. If `tenantId` is present, it must dynamically set the downstream URL by setting `context.custom.downstreamUrl = \`https://${tenantId}.api.example.com\``.
5. The policy must also add a new HTTP header `x-tenant-id` to the request, with the value of the `tenantId`. Because `Request.headers` is read-only, you must return a cloned `ZuploRequest` containing the new header and preserving `request.user` data using the `ZuploRequestInit` options.
6. Register this policy in `config/policies.json` with the name `tenant-routing` and type `tenant-routing`.
7. Add this policy to the `GET /api/data` route in `config/routes.oas.json`, placing it AFTER the existing `mock-auth` policy.
8. Create a custom handler in `modules/handler.ts` that returns a JSON response: `{"downstreamUrl": context.custom.downstreamUrl, "tenantHeader": request.headers.get("x-tenant-id")}`.
9. Configure the `GET /api/data` route in `config/routes.oas.json` to use this new handler.

## Constraints
- Project path: `/home/user/my-zuplo-api`
- Start command: `npm run dev`
- Port: 9000