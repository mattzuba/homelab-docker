#!/bin/sh

# Fix Repositories
sed -i 's/#http/http/g' /etc/apk/repositories
sed -i 's/http:/https:/g' /etc/apk/repositories
echo '@edge-testing https://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories
echo '@edge-community https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories

# Now update all packages
apk update

# Install open-vm-tools
apk add open-vm-tools open-vm-tools-guestinfo open-vm-tools-openrc
rc-update add open-vm-tools
service open-vm-tools start

# Install apk-autoupdater
apk add apk-autoupdate@edge-testing
echo '0 2 * * * /usr/sbin/apk-autoupdate' >> /etc/crontabs/root

# Install Docker
apk add docker docker-cli-compose@edge-community
rc-update add docker
sed -i 's~DOCKER_OPTS.*~DOCKER_OPTS="--userland-proxy=false --log-driver=gelf --log-opt=gelf-address=udp://10.0.2.5:12201"~g' /etc/conf.d/docker
service docker start

# Reboot for good measure
reboot
