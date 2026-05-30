# GraphQL Endpoint Proxy with GET Support

## Background
Zuplo is an edge-native API gateway. A common requirement is to proxy a GraphQL API. While GraphQL typically uses POST requests with a query in the body, some clients may send GET requests with the query in the URL parameters. Zuplo strictly enforces that `GET` and `HEAD` requests cannot have bodies. You need to create a Zuplo API that proxies to a public GraphQL API and handles GET requests by converting them into POST requests for the upstream server.

## Requirements
- Create a new Zuplo project.
- Set up a route at `/graphql` that proxies requests to `https://countries.trevorblades.com/graphql`.
- Support `POST` requests by passing them through directly to the upstream.
- Support `GET` requests by extracting the `query` parameter from the URL and transforming the request into a `POST` request with a JSON body (`{"query": "<query_value>"}`) before sending it to the upstream.
- If a `GET` request does not include a `query` parameter, return a `400 Bad Request` with the text `Missing query parameter`.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest` to scaffold the project.
- Define a custom handler for the `/graphql` route to inspect the request method.
- If the method is `GET`, read the `query` search parameter from the URL, construct a new `POST` request with a JSON body, and `fetch` the upstream URL.
- If the method is `POST`, simply forward the request to the upstream URL.
- Make sure the dev server can be started with `npm run dev` or `zuplo dev`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 8787
- API Endpoints:
  - POST `/graphql`: Proxies the request body to the upstream and returns the GraphQL response.
  - GET `/graphql?query=...`: Converts the request to a POST with a JSON body containing the query, proxies it to the upstream, and returns the response.
  - GET `/graphql`: Returns a 400 status code with the text `Missing query parameter`.

