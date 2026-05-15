# Zuplo Semantic Caching Policy

## Background
Implement semantic caching in a Zuplo API gateway to reduce AI API costs by caching responses for semantically similar queries.

## Requirements
- Create a Zuplo project in `/home/user/project`.
- Define a `POST /ask` route.
- Apply the `semantic-cache-inbound` policy to the route.
- Configure the policy to cache based on the `.query.text` property in the JSON body.
- Set `semanticTolerance` to `0.85`, `expirationSecondsTtl` to `300`, and `returnCacheStatusHeader` to `true`.
- Implement a custom handler for the route in `modules/question-handler.ts` that returns a JSON response containing `{"answer": "Mocked response", "generatedAt": "<timestamp>"}`.

## Implementation Guide
1. Run `npx create-zuplo-api@latest project` in `/home/user` (or initialize manually).
2. Update `config/routes.oas.json` to add the `POST /ask` route with the `semantic-cache-inbound` policy and your custom handler.
3. Update `config/policies.json` to configure the semantic cache policy according to the requirements.
4. Write the handler code in `modules/question-handler.ts`.

## Constraints
- Project path: `/home/user/project`
- Start command: `npm run dev`
- Port: 9000
- The handler module must be exported as `default` and imported as `$import(./modules/question-handler)`.