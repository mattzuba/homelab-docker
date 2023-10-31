## Intro

This is a Docker Compose setup that uses openspeedtest, iperf3, acme.sh for ssl, Portainer agent and Watchtower

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d` to start it up
4. Run `docker compose exec acme.sh --issue -d speed.your.tld --dns dns_cf --server letsencrypt --post-hook 'chmod 0644 speed.your.tld.key'` to generate the cert
5. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=speed -e DEPLOY_DOCKER_CONTAINER_KEY_FILE=/etc/ssl/nginx.key -e DEPLOY_DOCKER_CONTAINER_FULLCHAIN_FILE=/etc/ssl/nginx.crt -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='nginx -s reload' acme.sh --deploy -d speed.your.tld --deploy-hook docker` to deploy the cert
