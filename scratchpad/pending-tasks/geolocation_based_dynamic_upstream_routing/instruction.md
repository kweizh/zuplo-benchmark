Zuplo runs at the edge and exposes geolocation data via Cloudflare headers, which is highly useful for performance optimization and dynamic routing.

You need to write a custom TypeScript handler in `./modules/geo-router.ts` that inspects the `cf-ipcountry` header of an incoming request. If the header value is `US`, route the request to `https://us-east.example.com`; otherwise, route it to `https://eu-west.example.com`. 

**Constraints:**
- The handler must return a `fetch` response using the dynamically constructed URL.
- You MUST properly type the handler parameters using `ZuploRequest` and `ZuploContext` imported from `@zuplo/runtime`.
- Do NOT hardcode the request path; append the incoming URL path to the dynamic base URL.