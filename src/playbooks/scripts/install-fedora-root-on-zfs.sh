#!/bin/sh

set -x

# Usage:
# source get-first-two-disks.sh
# echo $DISK
#
# This is an automated approach to root on OpenZFS
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html
#
# See https://stackoverflow.com/a/51312156


output=$(lsblk --json --nodeps -o name,label,size,type,model,serial | jq -r '[.blockdevices[] | select(.size | match("([0-9.]+)G"; "x") | (.captures[0].string | tonumber) >= 1.8)] | .[0:2] | .[] | .model')

function getDisks () {
  printf '%s\n' "$output" | while IFS= read -r model; do
    search=$(echo $model | tr ' ' '_')
    find /dev/disk/by-id/ | grep "$search" | grep -vE '\-part[0-9]'
  done
}

# Declare disk array
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#:~:text=page%20for%20examples.-,Declare%20disk%20array,-DISK%3D%27/dev
DISK=$(getDisks | sort | uniq | tr '\n' ' ')

# Set a mount point
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#:~:text=by%2Did/disk1%27-,Set%20a%20mount%20point,-MNT%3D%24(

MNT=$(mktemp -d)

# Set partition size:
SWAPSIZE=4
# Set how much space should be left at the end of the disk, minimum 1GB
RESERVE=1

# Install ZFS support from live media:
apk add zfs


# Install partition tool
apk add parted e2fsprogs cryptsetup util-linux

# System Installation
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#system-installation


# Partition the disks.

partition_disk () {
 local disk="${1}"
 blkdiscard -f "${disk}" || true

 parted --script --align=optimal  "${disk}" -- \
 mklabel gpt \
 mkpart EFI 2MiB 1GiB \
 mkpart bpool 1GiB 5GiB \
 mkpart rpool 5GiB -$((SWAPSIZE + RESERVE))GiB \
 mkpart swap  -$((SWAPSIZE + RESERVE))GiB -"${RESERVE}"GiB \
 mkpart BIOS 1MiB 2MiB \
 set 1 esp on \
 set 5 bios_grub on \
 set 5 legacy_boot on

 partprobe "${disk}"
}

for i in ${DISK}; do
   partition_disk "${i}"
done

# Load ZFS kernel module
modprobe zfs

# Create boot pool
# shellcheck disable=SC2046
zpool create -d \
    -o feature@async_destroy=enabled \
    -o feature@bookmarks=enabled \
    -o feature@embedded_data=enabled \
    -o feature@empty_bpobj=enabled \
    -o feature@enabled_txg=enabled \
    -o feature@extensible_dataset=enabled \
    -o feature@filesystem_limits=enabled \
    -o feature@hole_birth=enabled \
    -o feature@large_blocks=enabled \
    -o feature@lz4_compress=enabled \
    -o feature@spacemap_histogram=enabled \
    -o ashift=12 \
    -o autotrim=on \
    -O acltype=posixacl \
    -O canmount=off \
    -O compression=lz4 \
    -O devices=off \
    -O normalization=formD \
    -O relatime=on \
    -O xattr=sa \
    -O mountpoint=/boot \
    -R "${MNT}" \
    bpool \
           mirror \
    $(for i in ${DISK}; do
       printf '%s ' "${i}-part2";
      done)

# Create root pool
# shellcheck disable=SC2046
zpool create \
    -o ashift=12 \
    -o autotrim=on \
    -R "${MNT}" \
    -O acltype=posixacl \
    -O canmount=off \
    -O compression=zstd \
    -O dnodesize=auto \
    -O normalization=formD \
    -O relatime=on \
    -O xattr=sa \
    -O mountpoint=/ \
    rpool \
    mirror \
   $(for i in ${DISK}; do
      printf '%s ' "${i}-part3";
     done)

# Create root system container:
zfs create \
 -o canmount=off \
 -o mountpoint=none \
rpool/fedora

# Create system datasets, manage mountpoints with mountpoint=legacy
zfs create -o canmount=noauto -o mountpoint=/  rpool/fedora/root
zfs mount rpool/fedora/root
zfs create -o mountpoint=legacy rpool/fedora/home
mkdir "${MNT}"/home
mount -t zfs rpool/fedora/home "${MNT}"/home
zfs create -o mountpoint=legacy  rpool/fedora/var
zfs create -o mountpoint=legacy rpool/fedora/var/lib
zfs create -o mountpoint=legacy rpool/fedora/var/log
zfs create -o mountpoint=none bpool/fedora
zfs create -o mountpoint=legacy bpool/fedora/root
mkdir "${MNT}"/boot
mount -t zfs bpool/fedora/root "${MNT}"/boot
mkdir -p "${MNT}"/var/log
mkdir -p "${MNT}"/var/lib
mount -t zfs rpool/fedora/var/lib "${MNT}"/var/lib
mount -t zfs rpool/fedora/var/log "${MNT}"/var/log

# Format and mount ESP
for i in ${DISK}; do
 mkfs.vfat -n EFI "${i}"-part1
 mkdir -p "${MNT}"/boot/efis/"${i##*/}"-part1
 mount -t vfat -o iocharset=iso8859-1 "${i}"-part1 "${MNT}"/boot/efis/"${i##*/}"-part1
done

mkdir -p "${MNT}"/boot/efi
mount -t vfat -o iocharset=iso8859-1 "$(echo "${DISK}" | sed "s|^ *||"  | cut -f1 -d' '|| true)"-part1 "${MNT}"/boot/efi


# System Configuration
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#system-configuration


# Download and extract minimal Fedora root filesystem:
apk add curl
curl --fail-early --fail -L \
https://dl.fedoraproject.org/pub/fedora/linux/releases/37/Container/x86_64/images/Fedora-Container-Base-37-1.7.x86_64.tar.xz \
-o rootfs.tar.gz
curl --fail-early --fail -L \
https://dl.fedoraproject.org/pub/fedora/linux/releases/37/Container/x86_64/images/Fedora-Container-37-1.7-x86_64-CHECKSUM \
-o checksum

# BusyBox sha256sum treats all lines in the checksum file
# as checksums and requires two spaces "  "
# between filename and checksum

grep 'Container-Base' checksum \
| grep '^SHA256' \
| sed -E 's|.*= ([a-z0-9]*)$|\1  rootfs.tar.gz|' > ./sha256checksum

sha256sum -c ./sha256checksum

rootfs_tar=$(tar t -af rootfs.tar.gz | grep layer.tar)
rootfs_tar_dir=$(dirname "${rootfs_tar}")
tar x -af rootfs.tar.gz "${rootfs_tar}"
ln -s "${MNT}" "${MNT}"/"${rootfs_tar_dir}"
tar x  -C "${MNT}" -af "${rootfs_tar}"
unlink "${MNT}"/"${rootfs_tar_dir}"

# Enable community repo
sed -i '/edge/d' /etc/apk/repositories
sed -i -E 's/#(.*)community/\1community/' /etc/apk/repositories


# Generate fstab:
apk add arch-install-scripts
genfstab -t PARTUUID "${MNT}" \
| grep -v swap \
| sed "s|vfat.*rw|vfat rw,x-systemd.idle-timeout=1min,x-systemd.automount,noauto,nofail|" \
> "${MNT}"/etc/fstab

# Chroot
cp /etc/resolv.conf "${MNT}"/etc/resolv.conf
for i in /dev /proc /sys; do mkdir -p "${MNT}"/"${i}"; mount --rbind "${i}" "${MNT}"/"${i}"; done

# See https://stackoverflow.com/a/51312156
chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash <<"EOT"

# Unset all shell aliases, which can interfere with installation:
unalias -a

# Install base packages
dnf -y install @core grub2-efi-x64 \
grub2-pc grub2-pc-modules grub2-efi-x64-modules shim-x64  \
efibootmgr kernel kernel-devel

# Install ZFS packages
dnf -y install \
https://zfsonlinux.org/fedora/zfs-release-2-2"$(rpm --eval "%{dist}"||true)".noarch.rpm

dnf -y install zfs zfs-dracut

# Check whether ZFS modules are successfully built
# TODO see https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#system-installation:~:text=Check%20whether%20ZFS%20modules%20are%20successfully%20built


# Add zfs modules to dracut
echo 'add_dracutmodules+=" zfs "' >> /etc/dracut.conf.d/zfs.conf
echo 'force_drivers+=" zfs "' >> /etc/dracut.conf.d/zfs.conf

# Add other drivers to dracut:
if grep mpt3sas /proc/modules; then
  echo 'force_drivers+=" mpt3sas "'  >> /etc/dracut.conf.d/zfs.conf
fi
if grep virtio_blk /proc/modules; then
  echo 'filesystems+=" virtio_blk "' >> /etc/dracut.conf.d/fs.conf
fi

# Build initrd
find -D exec /lib/modules -maxdepth 1 \
-mindepth 1 -type d \
-exec sh -vxc \
'if test -e "$1"/modules.dep;
   then kernel=$(basename "$1");
   dracut --verbose --force --kver "${kernel}";
 fi' sh {} \;


# For SELinux, relabel filesystem on reboot:
fixfiles -F onboot

# Enable internet time synchronisation:
systemctl enable systemd-timesyncd

# Generate host id
zgenhostid -f -o /etc/hostid

# Install locale package, example for English locale:
dnf install -y glibc-minimal-langpack glibc-langpack-en

# Set locale, keymap, timezone, hostname
rm -f /etc/localtime
systemd-firstboot \
--force \
--locale=en_US.UTF-8 \
--timezone=Etc/UTC \
--hostname=testhost \
--keymap=us

# Set root passwd

printf 'root:changeme' | chpasswd

# Bootloader
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#bootloader

# Apply GRUB workaround
echo 'export ZPOOL_VDEV_NAME_PATH=YES' >> /etc/profile.d/zpool_vdev_name_path.sh
# shellcheck disable=SC1091
. /etc/profile.d/zpool_vdev_name_path.sh

# GRUB fails to detect rpool name, hard code as "rpool"
sed -i "s|rpool=.*|rpool=rpool|"  /etc/grub.d/10_linux

# Fedora and RHEL uses Boot Loader Specification module for GRUB, which does not support ZFS. Disable it:

echo 'GRUB_ENABLE_BLSCFG=false' >> /etc/default/grub

# Install GRUB:
mkdir -p /boot/efi/fedora/grub-bootdir/i386-pc/
for i in ${DISK}; do
 grub2-install --target=i386-pc --boot-directory \
     /boot/efi/fedora/grub-bootdir/i386-pc/  "${i}"
done
dnf reinstall -y grub2-efi-x64 shim-x64
cp -r /usr/lib/grub/x86_64-efi/ /boot/efi/EFI/fedora/

# Generate GRUB menu
mkdir -p /boot/grub2
grub2-mkconfig -o /boot/grub2/grub.cfg
cp /boot/grub2/grub.cfg \
 /boot/efi/efi/fedora/grub.cfg
cp /boot/grub2/grub.cfg \
 /boot/efi/fedora/grub-bootdir/i386-pc/grub2/grub.cfg

# For both legacy and EFI booting: mirror ESP content:
espdir=$(mktemp -d)
find /boot/efi/ -maxdepth 1 -mindepth 1 -type d -print0 \
| xargs -t -0I '{}' cp -r '{}' "${espdir}"
find "${espdir}" -maxdepth 1 -mindepth 1 -type d -print0 \
| xargs -t -0I '{}' sh -vxc "find /boot/efis/ -maxdepth 1 -mindepth 1 -type d -print0 | xargs -t -0I '[]' cp -r '{}' '[]'"

# Exit chroot
exit

# Unmount filesystems and create initial system snapshot You can later create a boot environment from this snapshot. See Root on ZFS maintenance page.
umount -Rl "${MNT}"
zfs snapshot -r rpool@initial-installation
zfs snapshot -r bpool@initial-installation

# Export all pools
zpool export -a

# Reboot?
EOT