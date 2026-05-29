FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    pip3 install --break-system-packages pytest-json-ctrf pytest-xprocess requests && \
    npm install -g zuplo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN cd /home/user && \
    npx -y create-zuplo-api@latest myproject --git=false --install=true --no-portal --no-eslint --yes

LABEL Author="generate-harbor-tasks"
LABEL Description="Zuplo project environment for custom 404 error handling task."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - always required pip3 packages: pytest-json-ctrf, pytest-xprocess, requests
#   - Node.js v24 for running Zuplo
#   - zuplo CLI installed globally via npm
#   - /home/user/myproject: scaffolded Zuplo project
