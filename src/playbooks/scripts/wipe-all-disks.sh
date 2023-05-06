#!/bin/bash


#
# WARNING: This script will wipe all disks on
# the system!
#
# Partition table, MBR and signatures are removed
# This WILL cause any boot disk to be un-bootable.
# Note this does not dban the disks.

if [ "$1" != "continue-i-know-what-i-am-doing" ]; then
   echo you must pass "continue-i-know-what-i-am-doing" as first argument
   exit 1
fi


DISKS=$(lsblk --json -S -o type,name,label,size,model,serial,wwn,uuid | jq -r '.blockdevices[] | select(.type=="disk") | .name')

set -x

for DISK in $DISKS
do
    echo "Clearing partition table of $DISK"
    sgdisk --zap-all /dev/$DISK
    echo "Clearing signatures from disk $DISK"
    # See also https://www.cyberciti.biz/faq/howto-use-wipefs-to-wipe-a-signature-from-disk-on-linux/
    wipefs /dev/$DISK --all
done


