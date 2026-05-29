# Zuplo Circuit Breaker Policy

## Background
Zuplo allows you to build custom policies using TypeScript. To protect downstream services from cascading failures, you need to implement a Circuit Breaker pattern that stops forwarding requests to a backend if it is consistently failing.

## Requirements
- Create a custom policy in Zuplo that acts as a circuit breaker.
- The policy should monitor the response status from the backend.
- If the backend returns a 5xx status code for 5 consecutive requests, the circuit breaker should "trip" (open).
- When the circuit breaker is open, the gateway should immediately return a `503 Service Unavailable` response to the client without calling the backend.
- Use Zuplo's `ZoneCache` to store the circuit breaker state (e.g., consecutive failure count, circuit state) across requests, ensuring it is scoped correctly.
- Apply this policy to a route `GET /api/data` that proxies to a backend URL (provided via environment variable or hardcoded for testing).
- Ensure the circuit breaker state is isolated per `run-id` by appending the `run-id` to the cache key.

## Implementation Hints
- You may need both an inbound policy (to check if the circuit is open and reject early) and an outbound policy (to monitor the backend response and update the failure count).
- Read the current `run-id` from the `ZEALT_RUN_ID` environment variable.
- Use `ZoneCache` to persist the failure count and state. Use the `run-id` in the cache key to avoid conflicts between parallel test runs.
- Use `HttpProblems.serviceUnavailable` or return a `new Response` with status 503 when the circuit is open.
- Create a route in `config/routes.oas.json` and configure the policies in `config/policies.json`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run start (or zuplo dev)
- Port: 3000
- Route: `GET /api/data` proxies to a backend.
- When the backend returns 200, the route returns 200.
- When the backend returns 500 for 5 consecutive requests, the 6th request must return 503 immediately without hitting the backend, and the response should indicate the service is unavailable.
- The cache key used to store the circuit state MUST include the `run-id` from the `ZEALT_RUN_ID` environment variable.

