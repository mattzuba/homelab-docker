## Intro

This is a Docker Compose setup that uses freeRADIUS, daloRADIUS, acme for ssl, Portainer agent and Watchtower

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d` to start it up
4. Run `docker compose exec acme --issue -d radius.your.tld --dns dns_cf --server letsencrypt` to generate the cert
5. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=radius -e DEPLOY_DOCKER_CONTAINER_KEY_FILE=/opt/etc/raddb/certs/server.key -e DEPLOY_DOCKER_CONTAINER_FULLCHAIN_FILE=/opt/etc/raddb/certs/server.crt -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='kill -HUP $(cat /opt/var/run/radiusd/radiusd.pid)' acme --deploy -d radius.your.tld --deploy-hook docker` to deploy the cert
