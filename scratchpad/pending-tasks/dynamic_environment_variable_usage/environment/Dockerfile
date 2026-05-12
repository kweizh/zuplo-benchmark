FROM node:20-bookworm

RUN useradd -m -s /bin/bash user

USER user
WORKDIR /home/user

# Pre-cache create-zuplo-api
RUN npx --yes create-zuplo-api@latest --help || true
