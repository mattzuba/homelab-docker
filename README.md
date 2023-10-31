## Intro

This is a Docker Compose setup to use Vaultwarden with a locally configured Cloudflared tunnel which allows websockets to work correctly.

## Prereqs

* Cloudflare account
* Some sort of SMTP host (if you want to send emails)
* Familiarity with configuration of Vaultwarden (visit their wiki)

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary
3. Copy cloudflared.example.yml to cloudflared.yml (no need to adjust yet, we'll get there)
4. Run docker-compose run --rm cloudflared-login and follow the instructions
5. Run docker-compose run --rm cloudflared-create.  Note the tunnel id displayed in the output and then modify your cloudflared.yml file appropriately
5. Run docker-compose run --rm cloudflared-route to create your DNS route to your tunnel
5. Run docker-compose --profile tunnel up -d
6. Visit https://vault.your.tld/admin and use your configured admin password to begin your configuration

