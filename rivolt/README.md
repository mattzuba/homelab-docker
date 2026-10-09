## Intro

This is a Docker Compose setup for [Rivolt](https://github.com/apohor/rivolt) with a locally configured Cloudflared tunnel, Pocket ID for OIDC login, and Anthropic for AI features. Also includes Watchtower.

## Prereqs

* Cloudflare account
* A running Pocket ID instance (see ../pocketid)
* An Anthropic API key

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary (hostnames, `ANTHROPIC_API_KEY`, `RIVOLT_COOKIE_SECRET`)
3. In Pocket ID, create an OIDC client (Administration > OIDC Clients) with callback URL `https://rivolt.your.tld/api/auth/oidc/pocketid/callback`. Copy the client id/secret into `.env`
4. Copy cloudflared.example.yaml to cloudflared.yaml (no need to adjust yet, we'll get there)
5. Run `docker compose run --rm cloudflared-login` and follow the instructions
6. Run `docker compose run --rm cloudflared-create`. Note the tunnel id displayed in the output and then modify your cloudflared.yaml file appropriately
7. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
8. Run `docker compose up -d`
9. Visit https://rivolt.your.tld/

## Notes

* The provider slug (`pocketid`) is used in the env var names and the callback path; the redirect URL must match what is registered in Pocket ID exactly.
* Rivolt requests `openid email profile`. Users need an email on their Pocket ID account; identity is keyed on a verified email, otherwise issuer+sub.
* The image is pulled from `ghcr.io/apohor/rivolt:latest`, which Rivolt's CI retags on each `vX.Y.Z` release (amd64 only). Watchtower keeps it up to date.
