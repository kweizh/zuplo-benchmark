FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @zuplo/cli --unsafe-perm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment for WebSocket Proxy Setup task."

RUN mkdir -p /home/user/myproject/config /home/user/myproject/modules && \
    cd /home/user/myproject && \
    npm init -y && \
    npm install @zuplo/runtime @zuplo/cli && \
    cat > package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "scripts": {
    "dev": "zuplo dev --port 3000"
  },
  "dependencies": {
    "@zuplo/runtime": "latest"
  },
  "devDependencies": {
    "@zuplo/cli": "latest",
    "typescript": "^5.0.0"
  }
}
EOF

RUN cd /home/user/myproject && \
    cat > zuplo.json <<'EOF'
{
  "version": 1,
  "project": "myproject",
  "compatibilityDate": "2024-03-14"
}
EOF

RUN cd /home/user/myproject/config && \
    cat > routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My API"
  },
  "paths": {}
}
EOF

RUN cd /home/user/myproject/config && \
    cat > policies.json <<'EOF'
{
  "policies": []
}
EOF

# Container contents:
#   - Node.js v22 installed
#   - @zuplo/cli installed globally
#   - /home/user/myproject - basic Zuplo project with empty routes and policies

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
