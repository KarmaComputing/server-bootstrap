#!/bin/bash

#
# Identify all 2TB drives and put them into
# one ZFS pool called 'tank'
#
# Note: The disks should be at least 1.8T in size to
#       be included. If you don't, you'll waste a *lot*
#       of space because ZFS stripes data across disks
#       in such a way that each disk holds an equal amount of data.
#       If one disk is smaller, the larger disks can't be
#       fully utilized because they must match the capacity of
#       the smallest disk.
#
# Note: zfs create will fail with "is in use and contains a unknown filesystem"
#       if the pool if already created.
#       If happy to, perform zfs destroy to destroy the pool
#


if [ "$1" != "continue-i-know-what-i-am-doing" ]; then
   echo you must pass "continue-i-know-what-i-am-doing" as first argument
   exit 1
fi

# List drives with at least 1.8TB in size.

DRIVES=$(lsblk --json --nodeps -o name,label,size,type,model,serial | jq '.blockdevices[] | select(.size | match("([0-9.]+)T"; "x") | (.captures[0].string | tonumber) >= 1.8) | {model: .model, serial: .serial, path: ("/dev/disk/by-id/ata-" + (.model | gsub(" "; "_")) + "_" + .serial)} | {path: .path}'| jq -sr '.[] | .path')

zpool create -f tank raidz2 $DRIVES
