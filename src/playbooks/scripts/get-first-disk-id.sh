#!/bin/bash

set -exou

FIRST_DISK_SERIAL=$(lsblk --json -S -o type,name,label,size,model,serial,wwn,uuid | jq -r '.blockdevices[] | select(.type=="disk") | .serial' | head -1)

FIRST_DISK_ID=$(ls /dev/disk/by-id/ | grep $FIRST_DISK_SERIAL| head -1)

DISK=/dev/disk/by-id/$FIRST_DISK_ID
