FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g npm@latest

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo task environment for JSON to XML transformation."

RUN mkdir -p /home/user/myproject/config && \
    mkdir -p /home/user/myproject/modules && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "myproject",
  "version": "0.1.0",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "zuplo dev",
    "test": "zuplo test"
  },
  "dependencies": {
    "zuplo": "^6.70.3"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^22.0.0"
  }
}
EOF

RUN cd /home/user/myproject && \
    cat >zuplo.jsonc <<'EOF'
{
  "version": 1,
  "compatibilityDate": "2024-01-01"
}
EOF

RUN cd /home/user/myproject && \
    cat >tsconfig.json <<'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
EOF

RUN cd /home/user/myproject && \
    cat >config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "version": "1.0.0",
    "title": "My API"
  },
  "paths": {}
}
EOF

RUN cd /home/user/myproject && \
    cat >config/policies.json <<'EOF'
{
  "policies": []
}
EOF

# Container contents:
#   - Node.js v24
#   - /home/user/myproject containing a minimal Zuplo project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]