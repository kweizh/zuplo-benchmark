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
LABEL Description="Zuplo project with an initial /protected route."

RUN mkdir -p /home/user/myproject/config && \
    mkdir -p /home/user/myproject/modules && \
    cd /home/user/myproject && \
    npm init -y && \
    npm install @zuplo/runtime typescript @tsconfig/node20 && \
    cat > package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "scripts": {
    "build": "zuplo build"
  },
  "dependencies": {
    "@zuplo/runtime": "latest"
  },
  "devDependencies": {
    "typescript": "latest",
    "@tsconfig/node20": "latest"
  }
}
EOF

RUN cat > /home/user/myproject/zuplo.jsonc <<'EOF'
{
  "version": 1,
  "project": "myproject",
  "compatibilityDate": "2024-03-14"
}
EOF

RUN cat > /home/user/myproject/config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "title": "My API",
    "version": "1.0.0"
  },
  "paths": {
    "/protected": {
      "get": {
        "responses": {
          "200": {
            "description": "Success"
          }
        },
        "x-zuplo-route": {
          "corsPolicy": "none",
          "handler": {
            "export": "default",
            "module": "$import(./modules/hello-world)"
          }
        }
      }
    }
  }
}
EOF

RUN cat > /home/user/myproject/config/policies.json <<'EOF'
{
  "policies": []
}
EOF

RUN cat > /home/user/myproject/modules/hello-world.ts <<'EOF'
import { ZuploRequest, ZuploContext } from "@zuplo/runtime";

export default async function (request: ZuploRequest, context: ZuploContext) {
  return new Response("Hello World");
}
EOF

RUN cat > /home/user/myproject/tsconfig.json <<'EOF'
{
  "extends": "@tsconfig/node20/tsconfig.json",
  "compilerOptions": {
    "target": "es2022",
    "module": "esnext",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
EOF

# Container contents:
#   - Node.js v24 and zuplo CLI installed.
#   - /home/user/myproject - A basic Zuplo project with a /protected route.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
