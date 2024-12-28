#!/bin/sh

HEADERS_SENT=false

send_headers() {
  if [ "$HEADERS_SENT" = false ]; then
    printf "Content-type: text/plain\n\n"
    HEADERS_SENT=true
  fi
}

message() {
  send_headers
  printf "%s\n\n" "$1"
}

# Which firmware file are we working with
FIRMWARE=$(basename "$PATH_INFO")

if [ "$FIRMWARE" = "complete" ]; then
  message "Missing firmware file name"
  exit
fi

message "Request to delete firmware file $FIRMWARE by $REMOTE_ADDR"

# Verify the firmware file exists
if [ ! -f "/srv/www/$FIRMWARE" ]; then
  message "Firmware file does not exist"
  exit
fi

message "Deleting firmware file $FIRMWARE"
rm "/srv/www/$FIRMWARE"
rm -f "/srv/www/$FIRMWARE.md5"
