# Transform JSON Request to XML

## Background
Zuplo is an edge-native API gateway. Sometimes we need to integrate modern JSON APIs with legacy XML backends. In this task, you will implement an inbound policy that transforms an incoming JSON payload into an XML payload before forwarding it to a backend.

## Requirements
- You are provided with a basic Zuplo project in `/home/user/myproject`.
- Create a route `POST /submit` that accepts a JSON payload, for example: `{"orderId": 123, "amount": 45.67}`.
- Implement a custom inbound policy in `modules/json-to-xml.ts` that reads the JSON body, converts it to XML, and returns a new `ZuploRequest` with the XML body and `content-type: application/xml` header.
- The resulting XML should look like this: `<order><orderId>123</orderId><amount>45.67</amount></order>`.
- The route should forward the transformed request to `https://httpbin.org/post` (which echoes the request).
- The response from the backend should be returned to the client.

## Implementation Guide
1. Navigate to `/home/user/myproject`.
2. Install a pure-JS XML builder library (e.g., `fast-xml-parser` or `xmlbuilder2`). Do not use native Node.js modules as Zuplo runs in a Web-standard edge runtime.
3. Create the inbound policy in `modules/json-to-xml.ts`. It should read `request.json()`, convert it to XML, and return a new `ZuploRequest` (using `new ZuploRequest(request, { body: xmlString, headers: newHeaders })`).
4. Configure `config/routes.oas.json` to define the `POST /submit` route and apply your new inbound policy.
5. Configure `config/policies.json` to declare your policy instance.
6. Ensure the backend URL is set to `https://httpbin.org/post`.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev`
- Port: 3000
- Use only pure JavaScript libraries for XML generation.