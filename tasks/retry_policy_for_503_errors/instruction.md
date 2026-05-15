# Retry Policy for 503 Errors

## Background
In distributed systems, upstream services may occasionally return 503 Service Unavailable errors due to temporary overload or restarts. You need to implement a custom handler in Zuplo that acts as a proxy to an upstream service and retries the request up to 3 times if a 503 error is encountered.

## Requirements
- Create a custom handler in Zuplo that forwards requests to `http://127.0.0.1:8080/api/data`.
- If the upstream returns a 503 status code, the handler must retry the request.
- The maximum number of retries is 3 (i.e., up to 4 attempts total).
- If all attempts fail with 503, return the final 503 response to the client.
- If the upstream returns a 200 OK, return the response immediately.
- The route should be configured at `/data`.

## Implementation Guide
1. The Zuplo project is located at `/home/user/myproject`.
2. Create a module `modules/retry-handler.ts` containing the custom handler logic.
3. The handler should use `fetch` to call `http://127.0.0.1:8080/api/data`.
4. Remember to clone the request if you need to read its body or send it multiple times, though for this GET request, cloning the body is not strictly necessary.
5. Update `config/routes.oas.json` to route `GET /data` to your custom handler.

## Constraints
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 3000
- Upstream service URL: http://127.0.0.1:8080/api/data

## Integrations
- None