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
LABEL Description="Zuplo project with initial routes and policies configuration."

RUN mkdir -p /home/user/myproject/config && \
    cd /home/user/myproject && \
    cat > config/policies.json <<'EOF'
{
  "policies": [
    {
      "name": "api-key-inbound",
      "policyType": "api-key-inbound",
      "handler": {
        "export": "ApiKeyInboundPolicy",
        "module": "$import(@zuplo/runtime)"
      }
    }
  ]
}
EOF

RUN cd /home/user/myproject && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "title": "My API",
    "version": "1.0.0"
  },
  "paths": {
    "/hello": {
      "get": {
        "x-zuplo-route": {
          "handler": {
            "export": "default",
            "module": "$import(./modules/hello-world)"
          },
          "policies": {
            "inbound": ["api-key-inbound"]
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

# Container contents:
#   - Node.js v24 and @zuplo/cli installed globally.
#   - /home/user/myproject — Zuplo project with initial config
#   - config/policies.json with basic policies
#   - config/routes.oas.json with a GET /hello route

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
