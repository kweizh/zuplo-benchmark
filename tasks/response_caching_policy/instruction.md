# Configure Response Caching in Zuplo

## Background
You have a Zuplo API gateway project. To improve performance, you need to configure a caching policy that caches responses for 120 seconds.

## Requirements
- Create a caching policy named `my-cache-policy` of type `caching-inbound` in `config/policies.json`.
- Set the `expirationSecondsTtl` option to 120.
- Create a route `GET /cached-data` in `config/routes.oas.json`.
- The route should use a custom handler located at `modules/data.ts`.
- The custom handler should simply return a new Response with a random number (e.g., `new Response(Math.random().toString())`).
- Apply the `my-cache-policy` to the inbound policies of the `GET /cached-data` route.

## Implementation Guide
1. Navigate to `/home/user/myproject`.
2. Edit `config/policies.json` to include the `my-cache-policy`.
3. Create `modules/data.ts` with the custom handler.
4. Edit `config/routes.oas.json` to define the `GET /cached-data` route and apply the policy.

## Constraints
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 3000