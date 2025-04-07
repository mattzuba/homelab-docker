## Overview

IaC for my home lab

## Core Services

* Vaultwarden
* Ntfy
* Grafana
* AdGuard Home
* esp-updater
* Frigate
* Wazuh

## Common Services

* acme.sh
* cloudflared
* watchtower

## Instructions

Spin up AL2023 VM with the user-data.yaml in cloud-init, clone to /opt/homelab, then `git sparse-checkout set common <dir>` where `<dir>` is the service that will run on that machine, then `cd /opt/homelab/<dir>` and follow the readme.
