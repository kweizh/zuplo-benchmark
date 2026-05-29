# Basic Proxy with API Key Auth

## Background
Zuplo is an edge-native API gateway that allows developers to add authentication, rate limiting, and other policies to APIs. In this task, you will create a simple proxy route protected by an API key.

## Requirements
- Initialize a new Zuplo project named `myproject`.
- Create a route at `GET /proxy` that proxies requests to `https://echo.zuplo.io/`.
- Protect the route using Zuplo's `api-key-inbound` policy so that only requests with a valid API key can access it.
- For local testing purposes, configure a local API key consumer with the API key value `test-api-key-123`.

## Implementation Hints
- Use `create-zuplo-api` to scaffold the project.
- Modify `config/routes.oas.json` to define the `/proxy` route.
- Use the `url-rewrite` handler to proxy the request to `https://echo.zuplo.io/`.
- Add the `api-key-inbound` policy to the inbound policies of the route.
- Make sure to configure `config/policies.json` to define the `api-key-inbound` policy instance.
- Create a `consumers.json` or equivalent local API key configuration to register `test-api-key-123` so it works in local dev.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: zuplo dev --port 9200
- Port: 9200
- API Endpoints:
  - GET `/proxy`: Proxies to `https://echo.zuplo.io/`.
    - If no API key or an invalid API key is provided, it should return a 401 Unauthorized status.
    - If a valid API key (`test-api-key-123`) is provided (via `authorization: Bearer test-api-key-123` header), it should return a 200 OK status and the response from `https://echo.zuplo.io/`.

