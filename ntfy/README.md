## Intro

This is a Docker Compose setup to use Ntfy with a locally configured Cloudflared tunnel which allows websockets to work correctly.  Also includes acme.sh for local access, Watchtower and Portainer.

## Prereqs

* Cloudflare account
* Familiarity with configuration of Ntfy (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Copy ntfy.example.yaml to ntfy.yaml and adjust as necessary
4. Copy cloudflared.example.yml to cloudflared.yml (no need to adjust yet, we'll get there)
5. Run `docker compose run --rm cloudflared-login` and follow the instructions
6. Run `docker compose run --rm cloudflared-create`.  Note the tunnel id displayed in the output and then modify your cloudflared.yml file appropriately
7. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
8. Run `docker compose up -d acme.sh`
9. Run `docker compose exec acme.sh --issue -d ntfy.your.tld --dns dns_cf --server letsencrypt` to generate the ssl cert
10. Run `docker compose exec acme.sh --install-cert -d ntfy.your.tld --key-file /opt/ssl/ntfy.key --fullchain-file /opt/ssl/ntfy.crt` to install the cert into the shared folder
11. Run `docker compose up -d` to kick up the rest of the containers
12. Run `docker compose exec -e DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=ntfy -e DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='killall -HUP ntfy' acme.sh --deploy -d ntfy.your.tld --deploy-hook docker` to set up the reload of ntfy when the cert renews
13. If you set up auth, add some users with `docker exec ntfy ntfy users ...`
14. Visit https://ntfy.your.tld/

