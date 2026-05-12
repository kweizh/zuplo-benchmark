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
LABEL Description="Zuplo project environment for query parameter transformation task."

RUN cd /home/user && \
    npx --yes create-zuplo-api@latest myproject --yes --install

# Container contents:
#   - Node.js v24 installed
#   - zuplo CLI installed
#   - /home/user/myproject - Default Zuplo API project
#   - Python pytest for verifier

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
