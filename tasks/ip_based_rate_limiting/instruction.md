# IP-Based Rate Limiting in Zuplo

## Background
You have a Zuplo project initialized at `/home/user/myproject`. Your goal is to protect the API from abuse by adding an IP-based rate limit to an existing route.

## Requirements
1. In `config/policies.json`, create a new policy named `ip-rate-limit` of type `rate-limit-inbound`.
2. Configure the policy options to limit by `ip`, allowing exactly `5` requests per `1` minute window.
3. In `config/routes.oas.json`, apply the `ip-rate-limit` policy to the `inbound` policies array of the `GET /hello` route.

## Implementation Guide
- Edit `/home/user/myproject/config/policies.json` to include the rate limit policy configuration.
- Edit `/home/user/myproject/config/routes.oas.json` to add `ip-rate-limit` to the inbound policies of the `/hello` route.

## Constraints
- Project path: `/home/user/myproject`