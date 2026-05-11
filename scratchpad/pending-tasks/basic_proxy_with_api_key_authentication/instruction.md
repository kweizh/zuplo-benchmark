Setting up a basic secure gateway is the foundational use case for Zuplo, protecting upstream services with edge-level authentication.

You need to configure a new route in `config/routes.oas.json` that proxies all `GET` requests from the `/public-api` path to the upstream URL `https://api.publicapis.org/entries`. You must also define an inbound policy in `config/policies.json` to require a Zuplo-managed API Key for this specific route.

**Constraints:**
- You MUST use the `api-key-inbound` policy type in your `policies.json`.
- Bind the policy to the route using the `x-zuplo-route` extension in the OpenAPI configuration file.
- Do NOT modify any existing routes in the `routes.oas.json` file.