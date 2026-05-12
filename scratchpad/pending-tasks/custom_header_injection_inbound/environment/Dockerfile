FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        ffmpeg ripgrep libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @getpochi/cli agent-browser zuplo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN agent-browser install

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment for custom header injection policy task."

RUN mkdir -p /home/user/myproject/config /home/user/myproject/modules && \
    cd /home/user/myproject && \
    cat > package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "scripts": {
    "dev": "zuplo dev",
    "build": "zuplo build"
  },
  "dependencies": {
    "@zuplo/runtime": "latest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
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

RUN cd /home/user/myproject && \
    cat > config/routes.oas.json <<'EOF'
{
  "openapi": "3.1.0",
  "info": {
    "title": "myproject",
    "version": "1.0.0"
  },
  "paths": {
    "/hello": {
      "get": {
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

RUN cd /home/user/myproject && \
    cat > config/policies.json <<'EOF'
{
  "policies": []
}
EOF

RUN cd /home/user/myproject && \
    cat > modules/hello.ts <<'EOF'
import { ZuploRequest } from "@zuplo/runtime";

export default async function (request: ZuploRequest) {
  return new Response("Hello World");
}
EOF

RUN cd /home/user/myproject && npm install

# Container contents:
#   - Node.js v24 and zuplo CLI installed
#   - Browser verification dependencies included
#   - /home/user/myproject - basic Zuplo project with a /hello route

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
