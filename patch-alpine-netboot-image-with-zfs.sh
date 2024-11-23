#!/bin/bash

# Purpose: Patch alpine netboot image with
# - include zfs kernel module by default
#   (note the 'alpine extended iso' includes the zfs module
#    but that is not a netboot image)
# - ping delay wait until network links are up and can
#   reach gateway for download of additional packages
#

set -x


# Force a wait for interfaces to come up
# on slow switches

WORK_DIR=$PWD
NETBOOT_OUTPUT_FILENAME=alpine-zfsnetboot-patched-init.tar.gz
pwd
ls -lh
cd iso
echo Removing previously extracted ./boot if exists
rm -rf ./boot
echo "Removing previous $NETBOOT_OUTPUT_FILENAME if exists"
rm -rf $NETBOOT_OUTPUT_FILENAME
# Clean up previous runs
find . -maxdepth 1 -type f -name "*.tar.gz" -mtime +0 # Remove older than today


tar -xvf alpine-zfsnetboot-*.tar.gz
cd ./boot

mkdir patch

zcat initramfs-lts | cpio -D patch --extract --make-directories --preserve-modification-time

cd patch

# Apply the initramfs-lts patch
patch init ../../../PatchFile-init-ping

# Re-package initramfs-lts
find . | cpio --format=newc --create | gzip > initramfs-lts
mv initramfs-lts ../

cd ../
rm -rf patch

echo Re-taring the netbook image for sending to boot server
echo -n patched-init makes reference to the fact init will poll ping to verify network
echo is up before attempting to pull down additional packages over network

tar -cvf $NETBOOT_OUTPUT_FILENAME ./
mv $NETBOOT_OUTPUT_FILENAME ../
cd $WORK_DIR
