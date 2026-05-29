# Zuplo MCP Tool Implementation

## Background
Create a Zuplo gateway that exposes internal data to AI agents by implementing the Model Context Protocol (MCP).

## Requirements
- Initialize a new Zuplo project.
- Create an MCP Server Handler that exposes a tool named `get_customer_summary`.
- The tool should accept a `customerId` (string) argument.
- The tool should return a summary of the customer, retrieving data from an in-memory dataset or a local file.
- Expose the MCP server on a POST route (e.g., `/mcp`).
- Configure the Zuplo dev server to use port 9200 for its editor to avoid port conflicts.

## Implementation Hints
- Use `create-zuplo-api` to scaffold the project.
- Define the route in `config/routes.oas.json` and point it to a custom module.
- Use the `@zuplo/runtime` to implement the MCP Server Handler.
- Define the tool schema and execution logic within the handler.
- Use `request.clone()` if you need to read the body multiple times, though the MCP handler usually manages this.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run build && zuplo dev --editor-port 9200
- Port: 8787
- API Endpoints:
  - POST `/mcp`: Handles MCP JSON-RPC requests. When sent a `tools/call` request for `get_customer_summary` with a valid `customerId`, it returns a successful JSON-RPC response containing the customer summary text.

