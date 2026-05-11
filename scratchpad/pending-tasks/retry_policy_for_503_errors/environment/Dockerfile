FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g zuplo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment for retry_policy_for_503_errors task"

RUN mkdir -p /home/user/myproject/config /home/user/myproject/modules && \
    cd /home/user/myproject && \
    cat > package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "scripts": {
    "dev": "zuplo dev"
  },
  "dependencies": {
    "@zuplo/runtime": "latest"
  }
}
EOF
RUN cd /home/user/myproject && \
    cat > zuplo.jsonc <<'EOF'
{
  "version": 1,
  "project": "myproject",
  "compatibilityDate": "2024-03-14"
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
    "/data": {
      "get": {
        "x-zuplo-route": {
          "handler": {
            "export": "default",
            "module": "$import(./modules/retry-handler)"
          }
        }
      }
    }
  }
}
EOF
RUN cd /home/user/myproject && \
    cat > config/policies.json <<'EOF'
{
  "policies": []
}
EOF
RUN cd /home/user/myproject && npm install

# Container contents:
#   - Node.js v24 and npm
#   - zuplo CLI installed globally
#   - /home/user/myproject initialized with package.json, zuplo.jsonc, routes.oas.json, and policies.json

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
