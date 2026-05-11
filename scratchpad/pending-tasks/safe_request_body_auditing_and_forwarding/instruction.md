A common developer friction point in edge runtimes is consuming a request body multiple times, which throws a "body used" exception and breaks downstream systems.

You need to implement a custom inbound policy in `./modules/audit-logger.ts` that reads the incoming JSON request body, extracts the `userId` field, logs it via Zuplo's context logger, and then safely passes the request to the upstream backend.

**Constraints:**
- You MUST use `request.clone()` to read the JSON payload so the original request body remains intact for the downstream handler.
- Strictly use `context.log.info()` for logging.
- Do NOT use native Node.js functions like `console.log` or file system (`fs`) modules.