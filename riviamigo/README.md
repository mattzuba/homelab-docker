## Intro

This is a Docker Compose setup for [Riviamigo](https://github.com/bballdavis/Riviamigo) with a locally configured Cloudflared tunnel and Pocket ID for OIDC login. Also includes Watchtower.

The stack is the app (API, web app and nginx origin in one container), TimescaleDB and Redis. Nothing is published on the host; cloudflared reaches the app at `riviamigo:8080` over the Docker network.

## Prereqs

* Cloudflare account
* A running Pocket ID instance (see ../pocketid)
* A Rivian account

## Instructions

1. Clone the repo
2. Copy .env.example to .env and adjust as necessary (hostnames, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `RIVIAMIGO_SETUP_TOKEN`)
3. In Pocket ID, create an OIDC client (Administration > OIDC Clients) with callback URL `https://riviamigo.your.tld/v1/auth/oidc/callback`. Copy the client id/secret into `.env`
4. Copy cloudflared.example.yaml to cloudflared.yaml (no need to adjust yet, we'll get there)
5. Run `docker compose run --rm cloudflared-login` and follow the instructions
6. Run `docker compose run --rm cloudflared-create`. Note the tunnel id displayed in the output and then modify your cloudflared.yaml file appropriately
7. Run `docker compose run --rm cloudflared-route` to create your DNS route to your tunnel
8. Run `docker compose up -d`. The first start runs database migrations, so give the app a couple of minutes to turn healthy
9. Visit https://riviamigo.your.tld/ and create the first owner account, using the `RIVIAMIGO_SETUP_TOKEN` value when asked
10. Delete or comment out `RIVIAMIGO_SETUP_TOKEN` in `.env`, then run `docker compose up -d --no-deps --force-recreate riviamigo`
11. Connect your Rivian account under Settings > Vehicles > Add Vehicle

### Turning on Pocket ID login

The first owner is always a local password account; SSO is added afterwards. The connection details come from `.env`, the switches are in the UI.

1. Settings > Authentication: select **Test provider**
2. Settings > Account: select **Connect SSO** and link your Pocket ID identity
3. Settings > Authentication: turn on **Enable SSO**, sign out, and sign back in with the Pocket ID button
4. Optional, once that works: turn off **Allow password login**. If SSO later breaks, use the break-glass lines at the bottom of `.env.example`

## Notes

* Upstream does not consider a tunnel on its own enough protection and wants an authenticated gateway in front of the app. To follow that, add a Cloudflare Access application for `riviamigo.your.tld` in Zero Trust (Pocket ID can be the identity provider there too). Without it, Riviamigo's own login is the only thing between the internet and your vehicle data.
* Riviamigo holds a session for your Rivian account and stores its encryption keys in the database, so treat the `riviamigo-db` volume and any recovery packages as secrets.
* `ALLOWED_ORIGINS` and `RIVIAMIGO_OIDC_PUBLIC_BASE_URL` must be the exact public origin, and the callback URL registered in Pocket ID must match exactly.
* New SSO users are not created automatically. Invite them from the app, or look at `RIVIAMIGO_OIDC_AUTO_SIGNUP` in the upstream [OIDC guide](https://riviamigo.com/docs/getting-started/oidc-sso/).
* The app image is `ghcr.io/bballdavis/riviamigo:latest` and Watchtower keeps it up to date. Database migrations run on startup and only go forward, so rolling back means restoring a backup (Settings > Backups), not just pinning an older tag.
* TimescaleDB (`latest-pg18`) and Valkey (`latest`, standing in for upstream's Redis) are also kept up to date by Watchtower, so they run ahead of the versions upstream pins in its [compose file](https://github.com/bballdavis/Riviamigo/blob/main/compose/docker-compose.yml).
* A new TimescaleDB image does not upgrade the extension inside an existing database; it stays on the version it was created with until you run `docker compose exec timescaledb psql -X -U riviamigo -d riviamigo -c 'ALTER EXTENSION timescaledb UPDATE'`.
* Recovery packages only restore onto the same or a newer TimescaleDB version, so a package made here may not restore onto a stock upstream stack until upstream's pin catches up.
* All requests reach the app from the cloudflared container, so its built-in rate limits are shared across every visitor rather than applied per client.
