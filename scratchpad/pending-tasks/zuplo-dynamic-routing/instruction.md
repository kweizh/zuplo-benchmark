# Zuplo Dynamic Upstream Routing

## Background
Zuplo is an edge-native API gateway that allows programmable routing. You need to implement dynamic upstream routing that proxies requests to different backends based on the client's country, determined via the `cf-ipcountry` header.

## Requirements
- Create a Zuplo project.
- Implement a custom route handler at `GET /api/data`.
- The handler should check the `cf-ipcountry` header of the incoming request.
- If the header is `US`, proxy the request to `https://echo.zuplo.io/us`.
- For all other values (or if the header is missing), proxy the request to `https://echo.zuplo.io/default`.
- The handler must return the exact response from the proxied backend.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold a project.
- Define the route in `config/routes.oas.json`.
- Implement a custom module handler (e.g., in `modules/routing.ts`) that reads the `cf-ipcountry` header from the `ZuploRequest` and uses `fetch()` to proxy the request.
- Make sure to return the `Response` object obtained from `fetch()`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8787
- API Endpoints:
  - GET `/api/data`: Returns the response from `https://echo.zuplo.io/us` if `cf-ipcountry: US` is provided, otherwise returns the response from `https://echo.zuplo.io/default`.

