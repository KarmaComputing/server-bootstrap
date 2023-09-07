#!/bin/sh

# Purpose:
# Build netboot image with zfs kernel module included

# USAGE:
# podman run  -it --rm -v $(pwd):/root/workdir alpine sh /root/workdir/build-alpine-netboot-zfs.sh


set -x

apk add alpine-sdk build-base apk-tools alpine-conf busybox fakeroot syslinux xorriso squashfs-tools sudo git grub grub-efi


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
# Enable zfs kernel module
cat > ./scripts/mkimg.zfsnetboot.sh << 'EOFINNER'
profile_zfsnetboot() {
        profile_standard
        kernel_cmdline="unionfs_size=512M console=tty0 console=ttyS0,115200"
        syslinux_serial="0 115200"
        kernel_addons="zfs"
        apks="$apks zfs-scripts zfs zfs-utils-py
                mkinitfs
                syslinux util-linux"
        initfs_features="base network squashfs usb virtio"
        local _k _a
        for _k in $kernel_flavors; do
                apks="$apks linux-$_k"
                for _a in $kernel_addons; do
                        apks="$apks $_a-$_k"
                done
        done
        apks="$apks linux-firmware"
        output_format="netboot"
        image_ext="tar.gz"
}
EOFINNER
cat ./scripts/mkimg.zfsnetboot.sh
echo Running mkimage.sh
./scripts/mkimage.sh --outdir ~/iso --arch x86_64 --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --profile zfsnetboot
EOF


mkdir -p /root/workdir/iso
cp /home/build/iso/alpine-zfsnetboot-*.tar.gz /root/workdir/iso
exit
# back on the host machine
ls -ltr | tail -n 1 # latest build
# Upload (scp) and extract latest build (e.g.
# alpine-netboot-230813-x86_64.tar.gz to boot server)

