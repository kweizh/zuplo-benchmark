# Request Body Cloning in Zuplo

## Background
In Zuplo, a common error is trying to read the body of a request or response twice (e.g., once for logging and once for forwarding). Because the body is a `ReadableStream`, it can only be read once. To log the body and still forward the request, developers must use `request.clone()` and `response.clone()` to avoid "body used" exceptions.

## Requirements
- Initialize a new Zuplo project.
- Create a custom handler for the route `POST /api/echo`.
- The handler must perform the following:
  1. Read and log the incoming request body as text using `context.log.info()`. The log message must be exactly in the format: `Intercepted Request: <body>`.
  2. Forward the request to an upstream service at `http://127.0.0.1:8080/echo` using `fetch()`.
  3. Read and log the response body from the upstream service as text using `context.log.info()`. The log message must be exactly in the format: `Intercepted Response: <body>`.
  4. Return the upstream response to the client.
- Configure `config/routes.oas.json` to route `POST /api/echo` to your custom handler.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Create a custom handler module (e.g., in `modules/`).
- Use `request.clone()` to safely read the request body for logging while keeping the original `request` intact to pass to `fetch()`.
- Use `response.clone()` to safely read the response body for logging while keeping the original `response` intact to return.
- Make sure the route in `routes.oas.json` uses the `$import()` syntax to reference your custom handler.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev
- Port: 3000
- API Endpoints:
  - `POST /api/echo`: Accepts any text/JSON body, forwards it to `http://127.0.0.1:8080/echo`, and returns the upstream response.
- The dev server output must contain the exact log messages for both the intercepted request and response bodies.
