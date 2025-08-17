## Intro

This is a Docker Compose setup to use Ollam/Open WebUI with a locally configured Cloudflared tunnel.

## Prereqs

* Cloudflare account
* Familiarity with configuration of Open WebUI and Ollama (visit their docs)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
4. Copy cloudflared.example.yml to cloudflared.yml (no need to adjust yet, we'll get there)
5. Run `docker compose run --rm cloudflared-login` and follow the instructions
6. Run `docker compose run --rm cloudflared-create`.  Note the tunnel id displayed in the output and then modify your cloudflared.yml file appropriately
7. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
11. Run `docker compose up -d` to kick up the rest of the containers
14. Visit https://chat.your.tld/

