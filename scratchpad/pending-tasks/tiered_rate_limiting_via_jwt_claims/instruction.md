Zuplo supports advanced rate limiting strategies by extracting authenticated user data directly from JWT claims.

You need to configure a rate-limiting policy in `config/policies.json` that dynamically assigns quotas based on a `plan` claim extracted from the user's JWT. Set the limit to 100 requests per minute for `free` users and 1000 requests per minute for `pro` users.

**Constraints:**
- The policy type in the JSON configuration MUST be `rate-limit-inbound`.
- Assume a previous policy has already validated the JWT and populated the `request.user.data` object.
- Do NOT hardcode API keys; the rate limit identifier must rely strictly on the extracted `plan` property.