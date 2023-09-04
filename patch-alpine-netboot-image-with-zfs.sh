#!/bin/sh

# Purpose: Patch alpine netboot image with
# - include zfs kernel module by default
#   (note the 'alpine extended iso' includes the zfs module
#    but that is not a netboot image)
# - ping delay wait until network links are up and can
#   reach gateway
#

set -x

# Force a wait for interfaces to come up
# on slow switches

WORK_DIR=$PWD
pwd
ls -lh
cd iso
tar -xvf alpine-netboot-*.tar.gz
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

# Re-tar the netbook image for sending to boot server
tar -cvf alpine-netboot-zfs.tar.gz ./

cd $WORK_DIR
