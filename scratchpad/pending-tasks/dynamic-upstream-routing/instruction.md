# Dynamic Upstream Routing with Zuplo

## Background
Zuplo is a programmable API gateway that runs at the edge. In this task, you will create a Zuplo project that implements dynamic upstream routing based on the client's geolocation (using the `cf-ipcountry` header).

## Requirements
- Initialize a new Zuplo project named `myproject`.
- Create a single route `GET /api/data`.
- Implement a custom TypeScript handler for this route.
- The handler must inspect the `cf-ipcountry` header of the incoming request.
- If the `cf-ipcountry` header is `GB`, `FR`, or `DE`, the handler should forward the request to `https://echo.zuplo.io/eu/api/data`.
- If the header is missing or has any other value, forward the request to `https://echo.zuplo.io/us/api/data`.
- The handler must return the exact response received from the upstream server.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Define the route in `config/routes.oas.json` and map it to a custom handler module.
- In your custom handler, read the `cf-ipcountry` header from the `ZuploRequest` object.
- Use the standard `fetch` API available in the edge runtime to call the appropriate upstream URL, and return the `Response`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run env -- zuplo dev --port 8080
- Port: 8080
- API Endpoints:
  - GET `/api/data`: Forwards requests dynamically based on `cf-ipcountry` header.
    - If `cf-ipcountry` is `GB`, it returns the response from `https://echo.zuplo.io/eu/api/data`.
    - If `cf-ipcountry` is missing, it returns the response from `https://echo.zuplo.io/us/api/data`.

