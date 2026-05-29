# Custom Caching Handler

## Background
Zuplo provides a programmable API including `ZoneCache` to store data. In this task, you will create a custom handler that caches responses from a backend service to improve performance.

## Requirements
- Create a new route in `config/routes.oas.json` that listens on `GET /api/${run-id}/data`.
- The route must use a custom TypeScript handler.
- The handler should check `ZoneCache` (cache name: `test-cache`) using the request URL as the key.
- If the data is found in the cache, return it as a JSON response with the header `x-cache: hit`.
- If the data is not in the cache, fetch it from `https://echo.zuplo.io/`, store the parsed JSON in the cache with a TTL of 60 seconds, and return it as a JSON response with the header `x-cache: miss`.

## Implementation Hints
- Read the current `run-id` from the `ZEALT_RUN_ID` environment variable.
- Use the `ZoneCache` API available in `@zuplo/runtime` to get and put data.
- Make sure to await the cache `get` and `put` operations, or handle promises correctly.
- Return a standard `Response` object with the correct headers.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: zuplo dev --port 9200
- Port: 9200
- API Endpoints:
  - GET `/api/${run-id}/data`: 
    - First request should return status 200, the JSON data from echo.zuplo.io, and the header `x-cache: miss`.
    - Subsequent requests within 60 seconds should return status 200, the same JSON data, and the header `x-cache: hit`.

