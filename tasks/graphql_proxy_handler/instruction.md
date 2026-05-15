# GraphQL Proxy with Auth and Introspection Disabled

## Background
Zuplo can proxy GraphQL APIs and add security policies to them. In this task, you will create a new Zuplo project that proxies a public GraphQL API, secures it with an API key, and disables GraphQL introspection.

## Requirements
- Initialize a new Zuplo project in `/home/user/myproject`.
- Create a route for `POST /graphql`.
- Configure the route handler to forward requests to `https://countries.trevorblades.com/graphql`.
- Apply the `api-key-inbound` policy to require an API key.
- Apply the `graphql-disable-introspection-inbound` policy to block introspection queries.

## Implementation
1. Run `npx create-zuplo-api@latest myproject` in `/home/user` (or `zuplo init` in the directory).
2. Update `config/routes.oas.json` to define the `POST /graphql` route.
3. Use the `url-forward` handler (or `url-rewrite`) to proxy to `https://countries.trevorblades.com/graphql`.
4. Update `config/policies.json` to define an `api-key-inbound` policy and a `graphql-disable-introspection-inbound` policy.
5. Apply both policies to the `/graphql` route in `routes.oas.json`.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev` (or `npx zuplo dev`)
- Port: 3000
