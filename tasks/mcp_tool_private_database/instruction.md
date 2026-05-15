# Zuplo MCP Tool for Private Database

## Background
You are building an AI agent integration for a company's internal sales database using Zuplo. The database is exposed via a local HTTP server. You need to create an MCP (Model Context Protocol) server on Zuplo that provides a custom tool to fetch and summarize sales by region.

## Requirements
1. **Local Database Server**: Create a simple Node.js HTTP server in `/home/user/db-server/server.js` listening on port 8080. It must have a `GET /sales?region=<region>` endpoint. If `region=US`, return `[{"amount": 100}, {"amount": 200}]`. If `region=EU`, return `[{"amount": 150}]`.
2. **Zuplo Project**: Initialize a Zuplo project in `/home/user/zuplo-mcp`.
3. **Custom Auth Policy**: Create a custom inbound policy in Zuplo named `custom-auth` that checks the `authorization` header. It should reject requests with a 401 status if the header does not match the expected Bearer token passed via policy configuration options.
4. **Internal Route**: Create a route `GET /internal/sales` that uses a custom handler to proxy the request to `http://localhost:8080/sales?region={region}`. Protect this route with your `custom-auth` policy, requiring the token `secret-internal-key`.
5. **MCP Server**: Create an MCP server route at `POST /mcp`. 
6. **MCP Auth**: Protect the `/mcp` route so clients can pass `?apiKey=secret-mcp-key`. Use the built-in `query-param-to-header-inbound` policy to map the `apiKey` query param to the `authorization` header, followed by your `custom-auth` policy requiring the token `secret-mcp-key`.
7. **Custom MCP Tool**: Add a custom tool named `summarize_sales` to the MCP server. 
   - It should accept a `region` string argument.
   - The handler must use `context.invokeRoute()` to call `GET /internal/sales?region=<region>`, passing the `authorization: Bearer secret-internal-key` header.
   - It must sum the `amount` values from the response and return `{"region": "<region>", "totalSales": <sum>}`.
8. **Configuration**: Ensure the OpenAPI spec for the tool is correctly configured with `x-zuplo-route.mcp: {"type": "tool"}` and properly integrated into the MCP Server handler's `operations` array.

## Constraints
- Project path: `/home/user/zuplo-mcp`
- DB Server path: `/home/user/db-server`
- DB Server Start command: `node /home/user/db-server/server.js`
- Zuplo Start command: `npm run dev` (inside `/home/user/zuplo-mcp`)
- Ports: DB Server on 8080, Zuplo on 3000 (default for `zuplo dev`)
- Do not use external APIs or Zuplo Cloud deployments. Everything must run locally.
- Do not use `fetch` to call the internal route from the tool handler; you must use `context.invokeRoute()`.

## Implementation Guide
- Use `npx create-zuplo-api@latest zuplo-mcp` to scaffold the project.
- For `custom-auth`, create a module `./modules/custom-auth.ts`.
- For the MCP Server, configure `routes.oas.json` to use the `@zuplo/runtime`'s `mcp-server-inbound` handler (Wait, MCP Server is a request handler, so `handler: { export: "McpServerHandler", module: "$import(@zuplo/runtime)" }`).
- Configure the MCP operations to point to your `summarize_sales` operation ID.
- Remember to clone the request/response body if you read it multiple times.
