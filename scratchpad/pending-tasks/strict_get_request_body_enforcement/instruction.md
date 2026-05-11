Zuplo strictly enforces that `GET` and `HEAD` requests cannot contain a body, which often surprises developers migrating from less compliant gateways.

You need to create a custom error-handling policy in `./modules/get-body-guard.ts` that intercepts incoming requests. If the request method is `GET` and a `content-length` header is present with a value greater than `0`, immediately reject the request.

**Constraints:**
- Return a `400 Bad Request` status code with the JSON payload `{"error": "GET requests must not contain a body"}`.
- Ensure this logic only triggers for `GET` requests; allow `POST`, `PUT`, and `PATCH` requests to pass through untouched.
- Do NOT throw an unhandled exception; you must return a valid, formatted `Response` object.