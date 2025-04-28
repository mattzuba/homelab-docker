## Intro

This is a Docker Compose setup to use XO.  Also includes acme for local access and Watchtower.

## Prereqs

* Familiarity with configuration of XO CE (visit their docs)

## Instructions

1. Clone the repo
1. Copy .env.example to .env and adjust as necessary
1. Run `sudo su` to change to root for acme
1. Run `export CF_Account_ID=<id> CF_Token=<token>`
1. Run `acme.sh --issue -d xo.your.tld --dns dns_cf --server letsencrypt` to generate the cert
1. Run `docker compose up -d` to create the containers and volumes
1. Run `DEPLOY_DOCKER_CONTAINER_LABEL=sh.acme.autoload.domain=xo DEPLOY_DOCKER_CONTAINER_KEY_FILE=/opt/ssl/ssl.key DEPLOY_DOCKER_CONTAINER_FULLCHAIN_FILE=/opt/ssl/ssl.crt DEPLOY_DOCKER_CONTAINER_RELOAD_CMD='killall -HUP remco' acme.sh --deploy -d xo.your.tld --deploy-hook docker` to set up the reload of xo when the cert renews

