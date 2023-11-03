## Intro

This is a Docker Compose setup to use Portainer server; includes acme for https access, Watchtower and Portainer.

## Prereqs

* Familiarity with configuration of Portainer (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d acme`
4. Run `docker compose exec acme --issue -d portainer.your.tld --dns dns_cf --server letsencrypt` to generate the ssl cert
5. Run `docker compose exec acme --install-cert -d portainer.your.tld --key-file /opt/ssl/portainer.key --fullchain-file /opt/ssl/portainer.crt` to install the cert into the shared folder
6. Run `docker compose up -d` to kick up the rest of the containers
7. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=portainer -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='killall portainer' acme --deploy -d portainer.your.tld --deploy-hook docker` to set up the reload of portainer when the cert renews
8. Visit https://portainer.your.tld/

