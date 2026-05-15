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
LABEL Description="Zuplo project environment for creating a mock API handler."

RUN mkdir -p /home/user/my-zuplo-api/config && \
    mkdir -p /home/user/my-zuplo-api/modules && \
    cd /home/user/my-zuplo-api && \
    cat > zuplo.json <<'EOF'
{
  "version": "1.0.0",
  "project": "my-zuplo-api"
}
EOF
RUN cd /home/user/my-zuplo-api/config && \
    cat > routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "title": "My Zuplo API",
    "version": "1.0.0"
  },
  "paths": {}
}
EOF
RUN cd /home/user/my-zuplo-api/config && \
    cat > policies.json <<'EOF'
{
  "policies": []
}
EOF
RUN cd /home/user/my-zuplo-api && \
    cat > package.json <<'EOF'
{
  "name": "my-zuplo-api",
  "version": "1.0.0",
  "dependencies": {
    "@zuplo/runtime": "latest"
  }
}
EOF

# Container contents:
#   - Node.js v24 and zuplo CLI installed.
#   - /home/user/my-zuplo-api — initialized Zuplo project with config/routes.oas.json

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
