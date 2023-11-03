## Overview

IaC for my home lab

## Core Services

* Vaultwarden
* OpenSpeedtest
* freeRADIUS
* Ntfy
* Grafana (with Loki)
* AdGuard Home
* Portainer

## Common Services

* acme.sh
* cloudflared
* portainer agent
* promtail agent
* watchtower

## Instructions

Spin up Alpine VM, install Docker, clone to /opt/homelab, then `git sparse-checkout set common <dir>` where `<dir>` is the service that will run on that machine, then `cd /opt/homelab/<dir>` and follow the readme.
