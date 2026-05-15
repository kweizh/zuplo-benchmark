FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g zuplo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment with Zuplo CLI installed."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    echo "No" | npx --yes create-zuplo-api@latest . || true && \
    if [ ! -f zuplo.jsonc ]; then \
        echo '{\n  "version": 1,\n  "project": "myproject",\n  "compatibilityDate": "2024-03-14"\n}' > zuplo.jsonc && \
        mkdir -p config modules && \
        echo '{\n  "routes": []\n}' > config/routes.oas.json && \
        echo '{\n  "policies": []\n}' > config/policies.json && \
        echo '{\n  "name": "myproject",\n  "version": "1.0.0",\n  "dependencies": {\n    "@zuplo/runtime": "latest"\n  }\n}' > package.json && \
        npm install; \
    fi

# Container contents:
#   - Node.js v24 and zuplo CLI installed
#   - /home/user/myproject  — initialized Zuplo project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]