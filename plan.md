# Zuplo Evaluation Dataset Research Report
Zuplo is a serverless, programmable API gateway designed for high performance at the edge. It allows developers to add authentication, rate limiting, and documentation to APIs using a GitOps-based workflow and TypeScript.
### 1. Library Overview
*   **Description**: Zuplo is an edge-native API gateway that combines the ease of a managed service with the flexibility of custom code (TypeScript). It runs on the edge (Cloudflare Workers) and is configured via OpenAPI files and JSON policies.
*   **Ecosystem Role**: Acts as a security and governance layer in front of any API (REST, GraphQL, etc.). It integrates with major identity providers (Auth0, Okta, Clerk), logging platforms (Datadog, Splunk), and supports the Model Context Protocol (MCP) for AI integration.
*   **Project Setup**:
    1.  **CLI Installation**: `npm install -g zuplo`
    2.  **Authentication**: Get an API Key from the [Zuplo Portal](https://portal.zuplo.com) (Settings > API Keys).
    3.  **Initialization**: `npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes` to scaffold a project, note the `--yes` for non-interactive mode.
    4.  **Local Development**: `zuplo dev` starts a local gateway and the "Route Designer" UI. Make sure to kill the background server before completing the task.
    5.  **Deployment**: `zuplo deploy --project <project-name>`
### 2. Core Primitives & APIs
*   **`config/routes.oas.json`**: An OpenAPI 3.1 file where routes are defined. Zuplo uses the `x-zuplo-route` extension to bind handlers and policies.
    ```json
    {
      "paths": {
        "/hello": {
          "get": {
            "x-zuplo-route": {
              "handler": {
                "export": "default",
                "module": "$import(./modules/hello-world)"
              },
              "policies": {
                "inbound": ["api-key-inbound"]
              }
            }
          }
        }
      }
    }
    ```
*   **`config/policies.json`**: Defines policy instances.
    ```json
    {
      "policies": [
        {
          "name": "api-key-inbound",
          "policyType": "api-key-inbound",
          "handler": {
            "export": "ApiKeyInboundPolicy",
            "module": "$import(@zuplo/runtime)"
          }
        }
      ]
    }
    ```
*   **`ZuploRequest` & `ZuploContext`**: Core objects for custom handlers and policies.
    ```ts
    import { ZuploRequest, ZuploContext } from "@zuplo/runtime";
    export default async function (request: ZuploRequest, context: ZuploContext) {
      context.log.info(`Request ID: ${context.requestId}`);
      return new Response("Hello from the edge!");
    }
    ```
    *   [ZuploRequest Documentation](https://zuplo.com/docs/programmable-api/zuplo-request)
    *   [ZuploContext Documentation](https://zuplo.com/docs/programmable-api/zuplo-context)
### 3. Real-World Use Cases & Templates
*   **Multi-Tenant Gateway**: Routing requests to different backends based on API key metadata or JWT claims. [Guide](https://zuplo.com/docs/guides/user-based-backend-routing)
*   **BFF (Backend-for-Frontend)**: Aggregating multiple microservices into a single frontend-optimized response.
*   **MCP Gateway**: Exposing internal APIs to AI agents like Claude or ChatGPT using the [MCP Server Handler](https://zuplo.com/docs/handlers/mcp-server).
*   **Semantic Caching**: Using vector-based matching to cache AI model responses. [Example](https://zuplo.com/examples/semantic-caching)
### 4. Developer Friction Points
*   **Request/Response Body Cloning**: A common error is trying to read the body twice (e.g., once for logging and once for forwarding). Developers must use `request.clone()` to avoid "body used" exceptions. [Ref](https://zuplo.com/docs/programmable-api/safely-clone-a-request-or-response)
*   **Module Resolution**: Zuplo uses a specific `$import()` syntax in JSON config. Local modules must start with `./modules/`.
*   **Native Node.js Dependencies**: Zuplo runs in a Web-standard edge runtime, not Node.js. Packages using `fs`, `child_process`, or native C++ bindings will fail.
*   **GET/HEAD Body Constraint**: Zuplo strictly enforces that `GET` and `HEAD` requests cannot have bodies, which can surprise developers using certain HTTP clients.
*   **Start Dev Server**: It may take some time to start a dev server, please make sure the project could be built before starting the background server,
    and the editor should run on 9200 above ports since 9100 may be used; MUST also add notes that should kill the background server before completing the task.
### 5. Evaluation Ideas
1.  **Basic Proxy with Auth**: Create a route that proxies to a public API and requires a Zuplo-managed API Key.
2.  **Custom Response Header**: Implement a custom outbound policy that adds a signature header based on the response body.
3.  **Dynamic Upstream Routing**: Route requests to `us-east-1.api.com` or `eu-west-1.api.com` based on the `cf-ipcountry` header (or Zuplo's geolocation data).
4.  **Request Body Transformation**: Implement a policy that transforms an incoming JSON payload to a legacy XML format before calling the backend.
5.  **Tiered Rate Limiting**: Apply different rate limits (Free vs. Pro) based on a value extracted from a JWT claim.
6.  **MCP Tool Implementation**: Create a Zuplo handler that serves as an MCP tool to fetch and summarize data from a private database.
7.  **Circuit Breaker Setup**: Configure a circuit breaker policy that trips after 5 consecutive 5xx errors from the backend.
### 6. Required Auth Info & Env Vars
To interact with the Zuplo Cloud Platform via CLI or API, the following information is required:
*   **`ZUPLO_API_KEY`**: (Required) The account-level API key obtained from the Zuplo Portal.
*   **`ZUPLO_PROJECT`**: (Required for many CLI commands) The name of your Zuplo project.
*   **`ZUPLO_ACCOUNT`**: (Optional/Contextual) The name of the account if the user belongs to multiple.
*   **`ZUPLO_ENVIRONMENT`**: (Optional) The target environment (e.g., `production`, `preview`).
### 7. Sources
1.  [Zuplo Documentation llms.txt](https://zuplo.com/docs/llms.txt) - Structured index of all Zuplo documentation.
2.  [Zuplo Project Structure](https://zuplo.com/docs/concepts/project-structure) - Details on file layout and configuration.
3.  [Zuplo CLI Authentication](https://zuplo.com/docs/cli/authentication) - Instructions for API key and OAuth setup.
4.  [Zuplo Examples](https://zuplo.com/examples) - Curated list of starter templates and use cases.
5.  [Zuplo Troubleshooting Guide](https://zuplo.com/docs/articles/troubleshooting) - Common errors and friction points.
6.  [Zuplo Programmable API Overview](https://zuplo.com/docs/programmable-api/overview) - Index of runtime classes and methods.