# Zuplo CORS Policy Configuration

## Background
You have a Zuplo API project initialized at `/home/user/myproject`. You need to configure a custom CORS policy and apply it to an existing route.

## Requirements
- Create a custom CORS policy named `my-cors-policy`.
- The policy must allow origins `https://app.example.com` and `http://localhost:3000`.
- The policy must allow methods `GET` and `POST`.
- The policy must allow headers `Authorization` and `Content-Type`.
- The policy must allow credentials (`allowCredentials: true`).
- Apply `my-cors-policy` to the `GET /hello` route.

## Implementation Guide
1. Modify `/home/user/myproject/config/policies.json` to include the `corsPolicies` array with your custom policy.
2. Modify `/home/user/myproject/config/routes.oas.json` to add `"corsPolicy": "my-cors-policy"` to the `x-zuplo-route` configuration for the `GET /hello` path.

## Constraints
- Project path: /home/user/myproject
- Only modify the existing `config/policies.json` and `config/routes.oas.json` files.

## Integrations
- None