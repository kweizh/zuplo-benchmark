# Configure Strict Timeouts for Upstream Requests

## Background
Zuplo is an edge-native API gateway where custom handlers can be written in TypeScript using standard Web APIs. When proxying requests to an upstream backend, it's critical to enforce strict timeouts to prevent hanging connections and ensure a responsive gateway. In this task, you will create a custom handler that enforces a timeout when calling an upstream service.

## Requirements
- Create a custom request handler in Zuplo that proxies incoming requests to an upstream backend.
- The upstream backend URL must be read from the `UPSTREAM_URL` environment variable.
- The timeout duration (in milliseconds) must be read from the `UPSTREAM_TIMEOUT_MS` environment variable.
- If the upstream backend does not respond within the specified timeout, the handler must return an HTTP `504 Gateway Timeout` response.
- If the upstream backend responds within the timeout, the handler must return the upstream's response.
- Map this custom handler to a `GET /proxy` route in the Zuplo configuration.

## Implementation Hints
- Use the `environment` object from `@zuplo/runtime` to read the `UPSTREAM_URL` and `UPSTREAM_TIMEOUT_MS` variables.
- Use the native `fetch` API combined with standard Web APIs (like `AbortSignal.timeout()`) to enforce the timeout on the request.
- Catch the resulting error (typically an `AbortError` or `TimeoutError`) from `fetch` and return a `new Response` with status `504`.
- Configure the route in `config/routes.oas.json` to point to your custom handler module.
- Do not use URL Rewrite or URL Forward built-in handlers, as they do not support custom timeout configurations natively without custom code.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: zuplo dev --no-start-editor --no-start-docs --port 9200
- Port: 9200
- API Endpoints:
  - GET `/proxy`: Proxies the request to `UPSTREAM_URL`.
    - If the upstream response time > `UPSTREAM_TIMEOUT_MS`, returns status 504.
    - If the upstream response time <= `UPSTREAM_TIMEOUT_MS`, returns the upstream's response status and body.

