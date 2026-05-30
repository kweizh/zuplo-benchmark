# API Versioning with Zuplo

## Background
Zuplo is an edge-native API gateway that allows programmable routing and policies. In this task, you will implement header-based API versioning where requests to a single endpoint are routed to different backend URLs depending on the value of a specific HTTP header.

## Requirements
- Create a new Zuplo project in `/home/user/myproject`.
- Implement a single route for `GET /api/data`.
- Inspect the `api-version` header of the incoming request.
- If `api-version` is `v2`, route the request to `https://echo.zuplo.io/v2/data`.
- If `api-version` is `v1` or not provided, route the request to `https://echo.zuplo.io/v1/data`.
- Ensure the dev server runs on port 9200.
- **IMPORTANT**: Kill the background dev server before completing the task.

## Implementation Hints
- Create the project using: `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes`
- You can implement this using a custom handler in the `modules/` directory that reads `request.headers.get("api-version")`, constructs the target URL, and uses `fetch()` to proxy the request.
- Map your custom handler to the `GET /api/data` route in `config/routes.oas.json`.
- Start the dev server on port 9200 (e.g., `npx zuplo dev --port 9200`).

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npx zuplo dev --port 9200
- Port: 9200
- API Endpoints:
  - GET `/api/data`:
    - When header `api-version: v1` is provided, returns the response from `https://echo.zuplo.io/v1/data`.
    - When header `api-version: v2` is provided, returns the response from `https://echo.zuplo.io/v2/data`.
    - When no `api-version` header is provided, defaults to returning the response from `https://echo.zuplo.io/v1/data`.

