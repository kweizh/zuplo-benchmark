FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g zuplo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment for URL redirect policy task."

RUN cd /home/user && \
    mkdir -p my-zuplo-api/config && \
    cd my-zuplo-api && \
    npm init -y && \
    npm install @zuplo/runtime && \
    cat > zuplo.jsonc <<'EOF'
{
  "version": 1,
  "project": "my-zuplo-api",
  "compatibilityDate": "2024-03-14"
}
EOF
RUN cd /home/user/my-zuplo-api && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "title": "my-zuplo-api",
    "version": "1.0.0"
  },
  "paths": {
    "/": {
      "get": {
        "summary": "My Endpoint",
        "description": "A simple endpoint",
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(./modules/hello-world)"
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
    mkdir -p modules && \
    cat > modules/hello-world.ts <<'EOF'
import { ZuploContext, ZuploRequest } from "@zuplo/runtime";

export default async function (
  request: ZuploRequest,
  context: ZuploContext,
) {
  return new Response("What's up, world!");
}
EOF
RUN cd /home/user/my-zuplo-api && \
    cat > package.json <<'EOF'
{
  "name": "my-zuplo-api",
  "version": "1.0.0",
  "scripts": {
    "dev": "zuplo dev"
  },
  "dependencies": {
    "@zuplo/runtime": "^3.0.0"
  }
}
EOF

# Container contents:
#   - Node.js v24 and zuplo CLI installed.
#   - /home/user/my-zuplo-api - Zuplo project with initial configuration.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
