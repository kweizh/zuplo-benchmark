FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g create-zuplo-api && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project with a mock authentication policy."

RUN cd /home/user && \
    npx --yes create-zuplo-api@latest my-zuplo-api --empty --install=false --yes && \
    cd my-zuplo-api && \
    npm install && \
    mkdir -p modules && \
    cat > modules/mock-auth.ts <<'EOF'
import { ZuploContext, ZuploRequest } from "@zuplo/runtime";

export default async function (
  request: ZuploRequest,
  context: ZuploContext,
  options: never,
  policyName: string
) {
  const tenantId = request.headers.get("x-mock-tenant-id");
  if (tenantId) {
    request.user = {
      sub: "mock-user",
      data: { tenantId }
    };
  } else {
    request.user = {
      sub: "mock-user",
      data: {}
    };
  }
  return request;
}
EOF

RUN cd /home/user/my-zuplo-api && \
    cat > config/policies.json <<'EOF'
{
  "policies": [
    {
      "name": "mock-auth",
      "policyType": "mock-auth",
      "handler": {
        "export": "default",
        "module": "$import(./modules/mock-auth)"
      }
    }
  ]
}
EOF

RUN cd /home/user/my-zuplo-api && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My API"
  },
  "paths": {
    "/api/data": {
      "get": {
        "summary": "Get data",
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(@zuplo/runtime)",
            "options": {
              "rewrite": "https://example.com"
            }
          },
          "policies": {
            "inbound": [
              "mock-auth"
            ]
          }
        }
      }
    }
  }
}
EOF

# Container contents:
#   - Node.js v24 installed
#   - /home/user/my-zuplo-api — Zuplo project with mock-auth policy

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
