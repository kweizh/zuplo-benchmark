FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g zuplo

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment for response caching policy task."

RUN mkdir -p /home/user/myproject/config /home/user/myproject/modules && \
    cd /home/user/myproject && \
    echo '{"name": "myproject", "version": "0.1.0", "type": "module", "private": true, "scripts": {"dev": "zuplo dev", "test": "zuplo test", "typecheck": "tsc --noEmit", "docs": "zuplo docs", "lint": "eslint"}, "dependencies": {"zuplo": "^6"}, "devDependencies": {"@eslint/js": "^10", "@types/node": "^22", "eslint": "^10", "eslint-config-prettier": "^10", "prettier": "^3", "typescript": "^5", "typescript-eslint": "^8"}}' > package.json && \
    echo '{"openapi": "3.1.0", "info": {"version": "1.0.0", "title": "My API"}, "paths": {}}' > config/routes.oas.json && \
    echo '{"policies": []}' > config/policies.json && \
    echo '{"version": 1, "project": "myproject", "compatibilityDate": "2024-03-14"}' > zuplo.jsonc && \
    echo '{"compilerOptions": {"target": "ES2022", "module": "ES2022", "moduleResolution": "Bundler", "strict": true, "esModuleInterop": true, "skipLibCheck": true, "forceConsistentCasingInFileNames": true, "outDir": "./dist", "baseUrl": "."}, "include": ["modules/**/*"]}' > tsconfig.json && \
    npm install

# Container contents:
#   - Node.js v24 and npm installed.
#   - zuplo CLI installed globally.
#   - /home/user/myproject — Initialized Zuplo project with package.json and config files.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]