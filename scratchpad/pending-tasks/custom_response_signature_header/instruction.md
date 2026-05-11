Zuplo allows custom outbound policies to modify responses before they are sent back to the client, providing a secure governance layer.

You need to implement a custom outbound policy in `./modules/response-signer.ts` that reads the upstream response body, calculates a base64-encoded SHA-256 hash of the content, and appends it to the response via a new `X-Response-Signature` header.

**Constraints:**
- Because Zuplo runs in a Web-standard edge runtime, you MUST use the Web Crypto API (`crypto.subtle.digest`) rather than the Node.js `crypto` module.
- You MUST construct and return a new `Response` object, as standard `Response` headers from fetch are immutable.
- Ensure the original response status code and existing headers are preserved.