# Zuplo Multi-Tenant Gateway

## Background
In a multi-tenant architecture, you often need to route requests to different backend environments based on the user's identity. Zuplo makes this simple by allowing you to read user data (from API Key metadata or JWT claims) and dynamically rewrite the request URL using a custom policy and the URL Rewrite handler.

## Requirements
- Create a Zuplo gateway that implements tenant-based routing.
- Create an API route `GET /api/data`.
- Implement a mock authentication policy that reads the `x-mock-tenant` header from the incoming request and populates `request.user.data.tenantId` with its value.
- Implement a custom inbound routing policy that reads `request.user.data.tenantId`.
- If the `tenantId` is present, the routing policy should set the downstream URL dynamically to `https://echo.zuplo.io/${tenantId}`.
- If the `tenantId` is missing, the routing policy should reject the request with a 400 Bad Request status code and a JSON payload `{"error": "Invalid or missing tenantId"}`.
- Use Zuplo's URL Rewrite handler to forward the request to the dynamically determined downstream URL.

## Implementation Hints
- Initialize a new Zuplo project if not already present.
- Write a custom policy (e.g., `mock-auth.ts`) that intercepts the request, reads the `x-mock-tenant` header, and assigns it to `request.user = { sub: "mock-user", data: { tenantId: <value> } }`. Return a new cloned request with this user object or mutate the context/request appropriately (Zuplo allows setting `request.user`).
- Write a second custom policy (e.g., `tenant-router.ts`) that reads `request.user.data.tenantId` and stores the target URL in `context.custom.downstreamUrl`.
- In your `routes.oas.json`, configure the `GET /api/data` route to apply both policies in sequence (`mock-auth` then `tenant-router`).
- Set the route's handler to use Zuplo's built-in `urlRewriteHandler` with a `rewritePattern` that references `${context.custom.downstreamUrl}`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 9000
- API Endpoints:
  - GET `/api/data`:
    - When the request includes the header `x-mock-tenant: customer-a`, the gateway routes the request to `https://echo.zuplo.io/customer-a`. The response from the echo server should contain the rewritten URL path.
    - When the request includes the header `x-mock-tenant: customer-b`, the gateway routes the request to `https://echo.zuplo.io/customer-b`.
    - When the request does not include the `x-mock-tenant` header, the gateway returns a 400 status code with `{"error": "Invalid or missing tenantId"}`.

