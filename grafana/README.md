## Intro

This is a Docker Compose setup to use Grafana and Loki; includes acme for https access, Watchtower and Portainer.

## Prereqs

* Familiarity with configuration of Grafana and Loki (visit their docs)

## Instructions

1. Clone the repo
1. Copy .env.example to .env and adjust as necessary
1. Run `docker compose up -d acme`
1. Run `docker compose exec acme --issue -d grafana.your.tld --dns dns_cf --server letsencrypt` to generate the ssl cert
1. Run `docker compose exec acme --install-cert -d grafana.your.tld --key-file /opt/ssl/grafana.key --fullchain-file /opt/ssl/grafana.crt --reloadcmd "chown 472:472 /opt/ssl/*"` to install the cert into the shared folder
1. Run `docker compose up -d` to kick up the rest of the containers
1. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=grafana -e DEPLOY_DOCKER_CONTAINER_KEY_FILE=/opt/ssl/dns.key -e DEPLOY_DOCKER_CONTAINER_FULLCHAIN_FILE=/opt/ssl/dns.crt -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='chown 472:472 /opt/ssl/*; killall grafana' acme --deploy -d grafana.zuba.dev --deploy-hook docker` to set up the reload of portainer when the cert renews
1. Visit https://grafana.your.tld/

