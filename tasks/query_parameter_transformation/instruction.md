# Query Parameter Transformation

## Background
You need to transform the query parameters of incoming requests before forwarding them to a backend service. This involves removing deprecated parameters and injecting necessary new parameters.

## Requirements
- Configure the route `GET /api/data` in the Zuplo API project.
- The route should forward requests to the mock backend `https://echo.zuplo.io/`.
- Add an inbound policy to remove the query parameter `legacy_id`.
- Add an inbound policy to set the query parameter `version` to `v2`.

## Implementation Guide
1. The Zuplo project is located at `/home/user/myproject`.
2. In `config/routes.oas.json`, define the `GET /api/data` route with a URL Rewrite handler pointing to `https://echo.zuplo.io/`.
3. In `config/policies.json`, define two policies:
   - A `remove-query-params-inbound` policy that removes `legacy_id`.
   - A `set-query-params-inbound` policy that sets `version` to `v2`.
4. Apply these policies to the `GET /api/data` route in `config/routes.oas.json`.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev`
- Port: 8787
