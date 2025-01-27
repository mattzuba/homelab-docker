## Intro

This is a Docker Compose setup to use XO with a locally configured Cloudflared tunnel.  Also includes acme for local access and Watchtower.

## Prereqs

* Cloudflare account
* Familiarity with configuration of XO CE (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Copy cloudflared.example.yml to cloudflared.yml (no need to adjust yet, we'll get there)
4. Run `docker compose run --rm cloudflared-login` and follow the instructions
5. Run `docker compose run --rm cloudflared-create`.  Note the tunnel id displayed in the output and then modify your cloudflared.yml file appropriately
6. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
7. Run `docker compose up -d acme`
8. Run `docker compose exec acme --issue -d xo.your.tld --dns dns_cf --server letsencrypt` to generate the ssl cert
9. Run `docker compose exec acme --install-cert -d xo.your.tld --key-file /opt/ssl/ssl.key --fullchain-file /opt/ssl/ssl.crt` to install the cert into the shared folder
10. Run `docker compose up -d` to kick up the rest of the containers
11. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=xo -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='killall -HUP ntfy' acme --deploy -d ntfy.your.tld --deploy-hook docker` to set up the reload of ntfy when the cert renews
12. If you set up auth, add some users with `docker exec ntfy ntfy users ...`
13. Visit https://ntfy.your.tld/

