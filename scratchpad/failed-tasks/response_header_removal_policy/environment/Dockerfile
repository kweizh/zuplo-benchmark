FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g @zuplo/cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project with a handler that adds x-powered-by header."

RUN mkdir -p /home/user/zuplo-project/config /home/user/zuplo-project/modules && \
    cd /home/user/zuplo-project && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My Zuplo API"
  },
  "paths": {
    "/hello": {
      "get": {
        "summary": "Say Hello",
        "responses": {
          "200": {
            "description": "OK"
          }
        },
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(./modules/hello)"
          }
        }
      }
    }
  }
}
EOF

RUN cd /home/user/zuplo-project && \
    cat > config/policies.json <<'EOF'
{
  "policies": []
}
EOF

RUN cd /home/user/zuplo-project && \
    cat > zuplo.jsonc <<'EOF'
{
  "version": 1,
  "project": "my-zuplo-api",
  "compatibilityDate": "2024-03-14"
}
EOF

RUN cd /home/user/zuplo-project && \
    cat > modules/hello.ts <<'EOF'
import { ZuploContext, ZuploRequest } from "@zuplo/runtime";

export default async function (
  request: ZuploRequest,
  context: ZuploContext
) {
  return new Response("Hello World", {
    headers: {
      "x-powered-by": "custom-backend"
    }
  });
}
EOF

RUN cd /home/user/zuplo-project && \
    cat > package.json <<'EOF'
{
  "name": "zuplo-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "zuplo dev"
  },
  "dependencies": {
    "@zuplo/runtime": "latest"
  }
}
EOF

RUN cd /home/user/zuplo-project && npm install

# Container contents:
#   - Node.js 22 and @zuplo/cli installed
#   - /home/user/zuplo-project - a basic Zuplo project
#   - /hello route returns a response with x-powered-by header

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
