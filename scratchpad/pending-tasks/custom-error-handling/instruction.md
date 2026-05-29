# Custom 404 Error Handling in Zuplo

## Background
Zuplo provides built-in error handling, but you may want to return a custom response when a route is not found (404).

## Requirements
- Create a custom not found handler in `modules/zuplo.runtime.ts`.
- When a user requests a path that does not match any route, the handler should return a 404 status code.
- The response body must be a JSON object containing:
  - `error`: "Not Found"
  - `path`: The path that was requested (e.g., `/unknown-path`)
  - `run_id`: The `run-id` value read from the `ZEALT_RUN_ID` environment variable.
- The response must include a custom header `X-Custom-404: true`.
- The response must have a `Content-Type` of `application/json`.

## Implementation Hints
- You can override the default 404 behavior by setting `runtime.notFoundHandler` in the `runtimeInit` function inside `modules/zuplo.runtime.ts`.
- Read the requested path from `request.url`.
- Read the `run-id` by importing `environment` from `@zuplo/runtime` and reading `environment.ZEALT_RUN_ID`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev -- --port 9000 --editor-port 9200 --docs-port 9300
- Port: 9000
- API Endpoints:
  - GET `/any-unknown-path`: Returns status 404.

    ```json
    // Response Body
    {
      "error": "Not Found",
      "path": "/any-unknown-path",
      "run_id": "<value-of-ZEALT_RUN_ID>"
    }
    ```
    ```http
    // Response Headers
    X-Custom-404: true
    Content-Type: application/json
    ```

