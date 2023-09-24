#!/bin/sh
set -x

# The two smallest disks are always used as the boot and root pool
# as a ZFS mirror.
# This script automates:
# - Finding the first two smallest disks (excluding Floppy and virtual disks)
# - TODO install ing the root & boot pools onto them
# - Based on manual steps in OpenZFS docs:
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#:~:text=page%20for%20examples.-,Declare%20disk%20array,-DISK%3D%27/dev


# For each disk found, get it's /dev/disk/by-id address by querying udevadm
# Initilize DISK list
DISK=""

DISK_ADDRESSES=$(lsblk --bytes --json -S -o type,name,label,size,model,serial,wwn,uuid | jq -r 'limit(2; [.blockdevices[] | select(.type=="disk" and (.model | contains("Floppy") or contains("Flash Disk") | not))] | sort_by(.size) | .[]) | .name')

for DISK_ADDRESS in $DISK_ADDRESSES
do
        DISK_UDEV_PATH=/dev/$(udevadm info --query=symlink  --name=/dev/"$DISK_ADDRESS"| cut -d ' ' -f 1)
        # Append disk to $DISK list
        DISK="$DISK $DISK_UDEV_PATH"
done

echo DISK is now set to: "$DISK"




