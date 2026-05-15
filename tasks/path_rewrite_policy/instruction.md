# Zuplo Path Rewrite Policy

## Background
Zuplo is a programmable API gateway. Often, you need to expose an API on a specific path (like `/api/v1/...`) but proxy the request to a backend that expects a different path (like `/...`).

## Requirements
- Initialize a Zuplo project in `/home/user/myproject`.
- Create a route for `GET /api/v1/users` that handles the request.
- The route must use a custom inbound policy (or built-in URL rewrite) to rewrite the URL path so that the `/api/v1` prefix is removed before forwarding the request to the backend.
- The backend URL should be `https://jsonplaceholder.typicode.com`.
- When a client makes a `GET` request to `/api/v1/users` on the gateway, the gateway should fetch `https://jsonplaceholder.typicode.com/users` and return the response.

## Implementation Guide
1. Initialize a new project using `npx create-zuplo-api@latest myproject` in `/home/user`.
2. Update `config/routes.oas.json` to define the `GET /api/v1/users` route.
3. Configure the route to use the built-in URL Rewrite policy or write a custom inbound policy in `modules/` to modify the `ZuploRequest` URL (e.g., replacing `/api/v1/users` with `/users`).
4. Set the handler to proxy to `https://jsonplaceholder.typicode.com` (using the URL handler or a custom fetch handler).
5. Ensure the project can be run with `npm run dev` or `zuplo dev`.

## Constraints
- Project path: `/home/user/myproject`
- Port: 3000
- Start command: `npm run dev -- --port 3000`