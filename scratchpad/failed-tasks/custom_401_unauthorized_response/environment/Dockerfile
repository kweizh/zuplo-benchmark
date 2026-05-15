FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Zuplo project environment initialized with create-zuplo-api."

RUN cd /home/user && \
    npx --yes create-zuplo-api@latest myproject && \
    cd myproject && \
    npm install

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/myproject  — Zuplo project initialized with create-zuplo-api

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
