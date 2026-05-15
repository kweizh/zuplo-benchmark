# Auth0 JWT Authentication Policy

## Background
You have a Zuplo API project initialized at `/home/user/myproject`. You need to secure the `/protected` route using an Auth0 JWT authentication policy.

## Requirements
- Add an inbound policy named `my-auth0-jwt-auth-inbound-policy` to the `/protected` route in `config/routes.oas.json`.
- Configure the policy in `config/policies.json` with the following properties:
  - `policyType`: `auth0-jwt-auth-inbound`
  - `handler.export`: `Auth0JwtInboundPolicy`
  - `handler.module`: `$import(@zuplo/runtime)`
  - `handler.options.auth0Domain`: `my-company.auth0.com`
  - `handler.options.audience`: `https://api.example.com/`

## Implementation Guide
1. Modify `/home/user/myproject/config/routes.oas.json` to add the policy to the `/protected` route's `x-zuplo-route.policies.inbound` array.
2. Modify `/home/user/myproject/config/policies.json` to define the policy with the required options.

## Constraints
- Project path: /home/user/myproject
- Do not change the existing route path or method.
