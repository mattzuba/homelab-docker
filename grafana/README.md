## Intro

This is a Docker Compose setup to use Grafana and Loki; includes acme for https access, Watchtower and Portainer.

## Prereqs

* Familiarity with configuration of Grafana and Loki (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d acme`
4. Run `docker compose exec acme --issue -d grafana.your.tld --dns dns_cf --server letsencrypt` to generate the ssl cert
5. Run `docker compose exec acme --install-cert -d grafana.your.tld --key-file /opt/ssl/grafana.key --fullchain-file /opt/ssl/grafana.crt` to install the cert into the shared folder
6. Run `docker compose up -d` to kick up the rest of the containers
7. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=grafana -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='killall grafana' acme --deploy -d grafana.your.tld --deploy-hook docker` to set up the reload of portainer when the cert renews
8. Visit https://grafana.your.tld/

