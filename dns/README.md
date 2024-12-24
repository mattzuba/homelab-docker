## Intro

This is a Docker Compose setup that uses AdGuard Home, unbound, acme for ssl, Portainer agent and Watchtower

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d acme` to start up acme
4. Run `docker compose exec acme --issue -d dns.your.tld --dns dns_cf --server letsencrypt'` to generate the cert
5. Run `docker compose exec acme --install-cert -d dns.your.tld --key-file /opt/ssl/dns.key --fullchain-file /opt/ssl/dns.crt` to install the cert into the shared folder
6. Run `docker compose up -d` to spin up everything else
7. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=dns -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='/opt/adguardhome/AdGuardHome -s reload' acme --deploy -d dns.your.tld --deploy-hook docker` to deploy the cert
8. Update AdGuard Home SSL settings to use /opt/ssl/dns.{key,crt} files.
