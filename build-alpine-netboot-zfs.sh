#!/bin/sh

# Purpose:
# Build netboot image with zfs kernel module included

# USAGE:
# podman run  -it --rm -v $(pwd):/root/workdir alpine sh /root/workdir/build-alpine-netboot-zfs.sh


set -x

apk add alpine-sdk build-base apk-tools alpine-conf busybox fakeroot syslinux xorriso squashfs-tools sudo git


adduser build --disabled-password -G abuild
# Set password non interactively
echo -e "password\npassword" | passwd build
echo "build ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/abuild
cp -R /root/workdir /home/build/
chown -R build /home/build/workdir
su - build << 'EOF'
set -x
SUDO=sudo abuild-keygen -n -i -a
cd workdir
git clone --depth 1 https://gitlab.alpinelinux.org/alpine/aports
cd aports
mkdir -p ~/iso
./scripts/mkimage.sh --outdir ~/iso --arch x86_64 --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --profile netboot
EOF

mkdir -p /root/workdir/iso
cp /home/build/iso/alpine-netboot-*.tar.gz /root/workdir/iso
exit
# back on the host machine
ls -ltr | tail -n 1 # latest build
# Upload (scp) and extract latest build (e.g.
# alpine-netboot-230813-x86_64.tar.gz to boot server)

