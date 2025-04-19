## Intro

This is a Docker Compose setup that uses Wazuh

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `git clone --depth 1 --branch <tag> https://github.com/wazuh/wazuh-docker` to clone the Wazuh Docker repo
4. Run `cd wazuh-docker/single-node` to enter the Wazuh Docker repo
5. Run `docker compose -f generate-indexer-certs.yml run --rm generator` to generate the default certs
6. Run `export COMPOSE_FILE=wazuh-docker/single-node/docker-compose.yml:compose.override.yaml COMPOSE_ENV_FILES=.env COMPOSE_PROJECT_NAME=wazuh`
6. Run `docker compose up -d` to spin up everything