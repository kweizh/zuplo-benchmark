# Request Size Limit Policy

## Background
In API gateways, it is common to restrict the size of incoming requests to prevent abuse, such as denial-of-service (DoS) attacks, or to ensure that payload sizes remain within acceptable boundaries for downstream services. Zuplo provides a built-in `request-size-limit-inbound` policy to enforce a maximum size in bytes for incoming requests.

## Requirements
- Create a Zuplo project in `/home/user/myproject`.
- Configure a `POST` route at `/upload` that proxies requests to `https://echo.zuplo.io/`.
- Configure a `request-size-limit-inbound` policy named `size-limit`.
- The policy must restrict the maximum request size to `50` bytes.
- The policy must actually verify the request size by setting `trustContentLengthHeader` to `false`.
- Apply the `size-limit` policy to the `/upload` route.

## Implementation Guide
1. Initialize a new Zuplo project at `/home/user/myproject` using `npx --yes create-zuplo-api@latest myproject`.
2. In `config/policies.json`, define the `request-size-limit-inbound` policy with `maxSizeInBytes` set to `50` and `trustContentLengthHeader` set to `false`.
3. In `config/routes.oas.json`, add a `POST` route for `/upload`.
4. Configure the route handler to use the `urlRewrite` handler pointing to `https://echo.zuplo.io/`.
5. Apply the `size-limit` policy to the `inbound` policies array for the `/upload` route.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev`
- Port: `8787`