# Zuplo Dynamic Upstream Routing

## Background
Zuplo is an edge-native API gateway. In this task, you will create a Zuplo project and implement a custom handler to dynamically route requests to different upstreams based on the `cf-ipcountry` header.

## Requirements
- Initialize a new Zuplo project in `/home/user/myproject`.
- Create a route `/route` that handles `GET` requests.
- Implement dynamic upstream routing based on the `cf-ipcountry` request header.
- If the header is `US`, proxy the request to `https://echo.zuplo.io/us`.
- If the header is `GB`, proxy the request to `https://echo.zuplo.io/gb`.
- For any other value, or if the header is missing, proxy the request to `https://echo.zuplo.io/default`.
- The route should return the response from the upstream server.

## Implementation Hints
- Use `npx create-zuplo-api@latest myproject` to scaffold the project.
- You can use a custom TypeScript handler to inspect `request.headers.get('cf-ipcountry')` and then use `fetch(upstream, request)` to proxy the request.
- Make sure your local dev server runs on port 3000 (you may need to modify package.json scripts to add `--port 3000` to the `zuplo dev` command).

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 3000
- API Endpoints:
  - GET `/route`: Proxies the request dynamically.
    - When `cf-ipcountry: US` is sent, it should return the response from `https://echo.zuplo.io/us` (the URL in the echo response should end with `/us`).
    - When `cf-ipcountry: GB` is sent, it should return the response from `https://echo.zuplo.io/gb` (the URL in the echo response should end with `/gb`).
    - When no header is sent, it should return the response from `https://echo.zuplo.io/default`.

