# Response Transformation (XML to JSON)

## Background
You need to proxy an API that returns legacy XML responses and transform those responses into modern JSON format before returning them to the client. This is a common pattern when modernizing legacy backends using an API gateway.

## Requirements
- Create a new Zuplo project.
- Create a custom handler module that returns a predefined XML response (to simulate the legacy backend).
- Define a route `GET /legacy-data` that uses this custom handler.
- Create an outbound policy that intercepts the XML response, parses it into JSON, and returns the JSON payload to the client.
- Apply the policy to the `/legacy-data` route.

## Implementation Hints
- Use `fast-xml-parser` (which works in edge environments) to parse the XML.
- The custom handler should return a `Response` with `Content-Type: application/xml` and the exact XML body: `<note><to>User</to><from>Admin</from><heading>Reminder</heading><body>Don't forget the meeting!</body></note>`.
- The outbound policy should read the response body as text, parse it using `fast-xml-parser`, and create a new `Response` object with `Content-Type: application/json` and the JSON stringified body.
- Remember to install `fast-xml-parser` in your Zuplo project.
- Start the dev server using the appropriate ports to avoid conflicts.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: npm run dev -- --port 9000 --editor-port 9200 --docs-port 9300
- Port: 9000
- API Endpoints:
  - GET `/legacy-data`: Returns status 200 and a JSON object representing the XML data.

    ```json
    // Expected JSON Response
    {
      "note": {
        "to": "User",
        "from": "Admin",
        "heading": "Reminder",
        "body": "Don't forget the meeting!"
      }
    }
    ```

