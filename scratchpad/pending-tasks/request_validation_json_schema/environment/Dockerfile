FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @zuplo/cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project with a POST /users route and an initial configuration."

RUN cd /home/user && \
    npx create-zuplo-api@latest myproject --yes && \
    cd myproject && \
    cat > config/policies.json <<'EOF'
{
  "policies": []
}
EOF

RUN cd /home/user/myproject && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My API",
    "description": "This is my API"
  },
  "paths": {
    "/users": {
      "post": {
        "summary": "Create User",
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(./modules/users.ts)"
          }
        },
        "responses": {
          "200": {
            "description": "OK"
          }
        }
      }
    }
  }
}
EOF

RUN cd /home/user/myproject && \
    cat > modules/users.ts <<'EOF'
import { ZuploContext, ZuploRequest } from "@zuplo/runtime";

export default async function (request: ZuploRequest, context: ZuploContext) {
  return new Response("OK", { status: 200 });
}
EOF

# Container contents:
#   - Node.js v24 and @zuplo/cli installed.
#   - /home/user/myproject - Zuplo project with initial config.
#   - config/routes.oas.json has a POST /users route without request validation.
#   - config/policies.json has no policies.
#   - modules/users.ts has a simple handler.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
