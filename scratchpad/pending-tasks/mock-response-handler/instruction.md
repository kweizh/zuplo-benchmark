# Zuplo Mock Response Handler

## Background
Zuplo allows developers to create custom handlers using TypeScript. In this task, you will create a custom handler that returns a static JSON response, which is useful for mocking backend services during development.

## Requirements
- Initialize a new Zuplo project named `myproject`.
- Create a custom TypeScript handler that returns a static JSON response: `{"status": "success", "message": "This is a mocked response"}`.
- Configure a new route `GET /mock` in `routes.oas.json` that uses this custom handler.

## Implementation Hints
- Use `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold the project.
- Create the custom handler in the `modules/` directory (e.g., `modules/mock-handler.ts`).
- In the handler, use `new Response(JSON.stringify({...}), { headers: { 'content-type': 'application/json' } })` to return the JSON.
- Update `config/routes.oas.json` to define the `/mock` path with the `get` method, and bind your custom handler using the `x-zuplo-route` extension with `$import(./modules/mock-handler)`.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev -- --port 9200
- Port: 9200
- API Endpoints:
  - GET `/mock`: Returns status 200 and a JSON object.
    ```json
    // Response
    {
      "status": "success",
      "message": "This is a mocked response"
    }
    ```

