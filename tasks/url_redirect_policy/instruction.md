# Zuplo URL Redirect Policy

## Background
You have a Zuplo project initialized at `/home/user/my-zuplo-api`. You need to configure a route that redirects legacy traffic to a new endpoint.

## Requirements
- Create a new route that intercepts `GET` requests to `/old-api`.
- The route must redirect the client to `/new-api`.
- The redirect must use a `301` (Permanent Redirect) HTTP status code.
- Use Zuplo's built-in Redirect Handler.

## Implementation Guide
1. Open the Zuplo configuration file `config/routes.oas.json`.
2. Add a new path `/old-api` with a `get` method.
3. Configure the `x-zuplo-route` extension to use the Redirect Handler.
4. Set the handler options to redirect to `/new-api` with a `301` status code.

## Constraints
- Project path: /home/user/my-zuplo-api
- Start command: npm run dev
- Port: 8787