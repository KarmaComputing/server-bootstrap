#!/bin/sh

# Purpose:
# Build netboot image with zfs kernel module included

# USAGE:
# podman run  -it --rm -v $(pwd):/root/workdir alpine sh /root/workdir/build-alpine-netboot-zfs.sh
# Debug container, by jumping into container shell:
# podman run -it --rm --entrypoint /bin/sh alpinebuilder


set -x

apk add alpine-sdk build-base apk-tools busybox fakeroot syslinux xorriso squashfs-tools sudo git grub grub-efi

# Note we now build alpine-conf from source (rather than doing apk add alpine-conf)
# due to issue https://github.com/KarmaComputing/server-bootstrap/issues/20

# Clone and build latest alpine-conf
git clone https://gitlab.alpinelinux.org/alpine/alpine-conf.git
cd alpine-conf
make
make install
cd -


# Start build
adduser build --disabled-password -G abuild
echo Moving aports to /home/build
mv /root/workdir/aports /home/build/
chown -R build:abuild /home/build/aports

# Set password non interactively
echo -e "password\npassword" | passwd build
echo "build ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/abuild

su - build << 'EOF'
set -x
SUDO=sudo abuild-keygen -n -i -a
# aports contains build utilities such as mkimage.sh
# No need to reclone since alpine-builder/Containerfile builds
# aports into image
#git clone --depth 1 https://gitlab.alpinelinux.org/alpine/aports

chown build:abuild /home/build/aports
cd aports

# Create & build alpine netboot profile with zfs kernel module enabled
cat > ./scripts/mkimg.zfsnetboot.sh << 'EOFINNER'

profile_zfsnetboot() {
        profile_standard
        kernel_cmdline="overlay_size=0 console=tty0 console=ttyS0,115200"
        syslinux_serial="0 115200"
        kernel_addons="zfs"
        apks="$apks zfs-scripts zfs zfs-utils-py python3 mkinitfs=3.10.1-r0 syslinux util-linux linux-firmware"
        initfs_features="base network squashfs usb virtio"
        output_format="netboot"
        image_ext="tar.gz"
}
EOFINNER
cat ./scripts/mkimg.zfsnetboot.sh
echo Running mkimage.sh
mkdir -p ~/iso
./scripts/mkimage.sh --outdir ~/iso --arch x86_64 --repository https://dl-cdn.alpinelinux.org/alpine/v3.20/main --profile zfsnetboot
EOF


ls -l /home/build/iso
mkdir -p /root/workdir/iso
cp /home/build/iso/alpine-zfsnetboot-*.tar.gz /root/workdir/iso
exit
# We're back outside the container at this point
ls -ltr | tail -n 1 # latest build
# Upload (scp) and extract latest build (e.g.
# alpine-zfsnetboot-*-x86_64.tar.gz to boot server)

