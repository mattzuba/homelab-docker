## Intro

This is a Docker Compose setup to use Pocket ID with a locally configured Cloudflared tunnel. Also includes Watchtower.

## Prereqs

* Cloudflare account
* Familiarity with configuration of Pocket ID (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Copy cloudflared.example.yaml to cloudflared.yaml (no need to adjust yet, we'll get there)
4. Run `docker compose run --rm cloudflared-login` and follow the instructions
5. Run `docker compose run --rm cloudflared-create`. Note the tunnel id displayed in the output and then modify your cloudflared.yaml file appropriately
6. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
7. Run `docker compose up -d`
8. Visit https://pocket-id.your.tld/
