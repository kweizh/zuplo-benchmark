# Circuit Breaker Policy

## Background
Zuplo allows developers to write custom policies to implement advanced gateway logic. In this task, you will implement a Circuit Breaker pattern using custom inbound and outbound policies, and `ZoneCache` to track state.

## Requirements
- You have a Zuplo project initialized at `/home/user/zuplo-project`.
- Create a custom inbound policy module `modules/circuit-breaker-inbound.ts` and a custom outbound policy module `modules/circuit-breaker-outbound.ts`.
- The circuit breaker must trip after 5 consecutive 5xx errors from the backend.
- When tripped, the inbound policy must return a `503 Service Unavailable` response with the body `{"error": "Circuit breaker tripped"}` and must not forward the request to the backend.
- The circuit breaker should reset (allow requests again) after 60 seconds of being tripped.
- If a request succeeds (status < 500), the consecutive error count must be reset to 0.
- Configure a route `/api/status/{code}` that proxies to `https://httpbin.org/status/${params.code}` using the `urlRewriteHandler`.
- Apply both the inbound and outbound circuit breaker policies to this route.

## Implementation Guide
1. In `modules/circuit-breaker-inbound.ts`, use `ZoneCache` with a key like `"cb-state"`. Read the state. If `tripped` is true, return a 503 response.
2. In `modules/circuit-breaker-outbound.ts`, check `response.status`. 
   - If >= 500, increment the error count in the cache. If it reaches 5, set `tripped: true` with a TTL of 60 seconds in the cache, and reset the count.
   - If < 500, reset the error count to 0 in the cache.
3. Update `config/policies.json` to register `circuit-breaker-inbound` and `circuit-breaker-outbound`.
4. Update `config/routes.oas.json` to define `/api/status/{code}` with the `urlRewriteHandler` pointing to `https://httpbin.org/status/${params.code}` and applying both policies.

## Constraints
- Project path: `/home/user/zuplo-project`
- Start command: `npm run dev &`
- Port: 8787

## Integrations
- None