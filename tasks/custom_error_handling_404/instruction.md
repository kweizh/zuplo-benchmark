# Custom Not Found (404) Handler

## Background
Zuplo is an edge-native API gateway that by default returns a standard Problem Details response for 404 errors. You need to override this behavior by implementing a custom not-found handler in the runtime extensions.

## Requirements
- Implement a custom Not Found (404) handler using `runtime.notFoundHandler` in `modules/zuplo.runtime.ts`.
- When a client requests an unmatched route, the gateway must return a `404 Not Found` status code.
- The response body must be a JSON object with this exact shape: `{"error": "Custom 404 - Route not found", "path": "<the-requested-path>"}`. For example, if the user requests `/missing-endpoint`, the `path` field should be `/missing-endpoint`.

## Implementation Guide
1. Initialize a new Zuplo project in `/home/user/myproject` using `npx create-zuplo-api@latest myproject`.
2. Create or modify `modules/zuplo.runtime.ts` to export a `runtimeInit(runtime: RuntimeExtensions)` function.
3. In `runtimeInit`, assign a custom async function to `runtime.notFoundHandler`.
4. Ensure the custom handler extracts the pathname from the request URL and returns a new Response with the required JSON body and a 404 status.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev`
- Port: 3000
- Return a standard JSON response, not the default `application/problem+json` format.