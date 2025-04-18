## Intro

This is a Docker Compose setup that uses AdGuard Home, unbound, a metrics exporter and Watchtower

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Run `docker compose up -d` to spin up everything
4. Run `sudo su` to change to root for acme
5. Run `export CF_Account_ID=<id> CF_Token=<token>`
6. Run `acme.sh --issue -d dns.your.tld --dns dns_cf --server letsencrypt` to generate the cert
7. Run `DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=dns DEPLOY_DOCKER_CONTAINER_KEY_FILE=/opt/ssl/dns.key DEPLOY_DOCKER_CONTAINER_FULLCHAIN_FILE=/opt/ssl/dns.crt DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='/opt/adguardhome/AdGuardHome -s reload' acme.sh --deploy -d dns.your.tld --deploy-hook docker` to deploy the cert
8. Update AdGuard Home SSL settings to use /opt/ssl/dns.{key,crt} files.
