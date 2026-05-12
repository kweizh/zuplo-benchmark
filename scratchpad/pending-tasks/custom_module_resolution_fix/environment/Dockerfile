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
LABEL Description="Zuplo project with a broken module resolution in routes.oas.json."

RUN cd /home/user && \
    npx create-zuplo-api@latest my-zuplo-api --yes && \
    cd my-zuplo-api && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My API"
  },
  "paths": {
    "/hello": {
      "get": {
        "summary": "Hello World",
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(hello-world)"
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

RUN cd /home/user/my-zuplo-api && \
    cat > modules/hello-world.ts <<'EOF'
import { ZuploContext, ZuploRequest } from "@zuplo/runtime";

export default async function (request: ZuploRequest, context: ZuploContext) {
  return new Response("Hello World!", { status: 200 });
}
EOF

# Container contents:
#   - Node.js v24 and @zuplo/cli installed.
#   - /home/user/my-zuplo-api - Zuplo project with initial config.
#   - config/routes.oas.json has an invalid module import `$import(hello-world)`.
#   - modules/hello-world.ts has a simple handler.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
