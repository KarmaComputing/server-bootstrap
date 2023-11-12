#!/bin/sh
set -eux -o pipefail

# The two smallest disks are always used as the boot and root pool
# as a ZFS mirror.
# This script automates:
# - Finding the first two smallest disks (excluding Floppy and virtual disks)
# - Note the use of chroot- there's no need to explicitly
#   exit from these since each function wraps the chroot entery/exit
#   by using bash heredoc syntax.
# - TODO install ing the root & boot pools onto them
# - Based on manual steps in OpenZFS docs:
# https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html#:~:text=page%20for%20examples.-,Declare%20disk%20array,-DISK%3D%27/dev

install_required_packages() {
        apk add lsblk eudev jq curl arch-install-scripts eudev sgdisk wipefs parted findmnt zfs e2fsprogs cryptsetup util-linux
}

setup_devd_udev() {
        setup-devd udev
}

declare_disk_array() {
        # For each disk found, get it's /dev/disk/by-id address by querying udevadm
        # Initilize DISK list
        DISK=""

        DISK_ADDRESSES=$(lsblk --bytes --json -S -o type,name,label,size,model,serial,wwn,uuid | jq -r 'limit(2; [.blockdevices[] | select(.type=="disk" and (.model | contains("Floppy") or contains("Flash Disk") | not))] | sort_by(.size) | .[]) | .name')

        for DISK_ADDRESS in $DISK_ADDRESSES
        do
                DISK_UDEV_PATH=/dev/$(udevadm info --query=symlink  --name=/dev/"$DISK_ADDRESS"| awk '{for(i=1; i<=NF; i++) if($i ~ /^disk\/by-id\//) {print $i; exit}}')
                # Append disk to $DISK list
                DISK="$DISK $DISK_UDEV_PATH"
        done

        echo DISK is now set to: "$DISK"
}

set_mount_point(){
        MNT=$(mktemp -d)
}

set_swap_size(){
        SWAPSIZE=4
        RESERVE=1
}


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

perform_disk_partition(){
        for i in ${DISK}; do
           partition_disk "${i}"
        done
}

load_ZFS_kernel_module(){
        modprobe zfs
}

ZFS_destroy_bpool(){
        zpool destroy -f bpool
}

ZFS_destroy_rpool(){
        zpool destroy -f rpool
}


create_mirrored_boot_pool() {
  zpool create -o compatibility=legacy  \
      -o ashift=12 \
      -o autotrim=on \
      -O acltype=posixacl \
      -O canmount=off \
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
}


create_mirrored_root_pool(){
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
}

create_root_system_container(){
        zfs create \
         -o canmount=off \
         -o mountpoint=none \
        rpool/fedora
}

create_system_datasets_and_mount_them(){
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
}


format_and_mount_ESP(){
        for i in ${DISK}; do
         mkfs.vfat -n EFI "${i}"-part1
         mkdir -p "${MNT}"/boot/efis/"${i##*/}"-part1
         mount -t vfat -o iocharset=iso8859-1 "${i}"-part1 "${MNT}"/boot/efis/"${i##*/}"-part1
        done

        mkdir -p "${MNT}"/boot/efi
        mount -t vfat -o iocharset=iso8859-1 "$(echo "${DISK}" | sed "s|^ *||"  | cut -f1 -d' '|| true)"-part1 "${MNT}"/boot/efi
}

download_extract_minimal_Fedora_root_filesystem(){
        curl --fail-early --fail -L \
        https://dl.fedoraproject.org/pub/fedora/linux/releases/38/Container/x86_64/images/Fedora-Container-Base-38-1.6.x86_64.tar.xz \
        -o rootfs.tar.gz
        curl --fail-early --fail -L \
        https://dl.fedoraproject.org/pub/fedora/linux/releases/38/Container/x86_64/images/Fedora-Container-38-1.6-x86_64-CHECKSUM \
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
}


enable_community_repo(){
        CURRENT_REPO=$(head -n 1 /etc/apk/repositories)
        NEW_REPO=$(echo $CURRENT_REPO | sed 's/\/main/\/community/')
        echo "$NEW_REPO" >> /etc/apk/repositories
}


generate_fstab(){
        genfstab -t PARTUUID "${MNT}" \
        | grep -v swap \
        | sed "s|vfat.*rw|vfat rw,x-systemd.idle-timeout=1min,x-systemd.automount,noauto,nofail|" \
        > "${MNT}"/etc/fstab
}


create_fedora_chroot(){
  cp /etc/resolv.conf "${MNT}"/etc/resolv.conf
  for i in /dev /proc /sys; do mkdir -p "${MNT}"/"${i}"; mount --rbind "${i}" "${MNT}"/"${i}"; done
}

chroot_install_fedora_base_packages(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  echo "Running in $SHELL"
  set -x
  unalias -a
  dnf -y install @core grub2-efi-x64 \
  grub2-pc grub2-pc-modules grub2-efi-x64-modules shim-x64  \
  efibootmgr kernel kernel-devel
EOL
}


chroot_install_fedora_ZFS_packages(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  echo "Running in $SHELL"
  set -x
  unalias -a

  dnf -y install \
  https://zfsonlinux.org/fedora/zfs-release-2-3"$(rpm --eval "%{dist}"||true)".noarch.rpm

  dnf -y install zfs zfs-dracut
EOL
}

chroot_fedora_add_ZFS_modules_to_dracut(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  echo 'add_dracutmodules+=" zfs "' >> /etc/dracut.conf.d/zfs.conf
  echo 'force_drivers+=" zfs "' >> /etc/dracut.conf.d/zfs.conf
EOL
}


chroot_fedora_add_mpt3sas_and_virtio_blk_drivers_to_dracut(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  if grep mpt3sas /proc/modules; then
    echo 'force_drivers+=" mpt3sas "'  >> /etc/dracut.conf.d/zfs.conf
  fi
  if grep virtio_blk /proc/modules; then
    echo 'filesystems+=" virtio_blk "' >> /etc/dracut.conf.d/fs.conf
  fi
EOL
}



chroot_fedora_build_initrd(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  find -D exec /lib/modules -maxdepth 1 \
  -mindepth 1 -type d \
  -exec sh -vxc \
  'if test -e "$1"/modules.dep;
     then kernel=$(basename "$1");
     dracut --verbose --force --kver "${kernel}";
   fi' sh {} \;
EOL
}


chroot_fedora_SELinux_relabel_filesystem_on_reboot(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  unalias -a
  set -x
  fixfiles -F onboot
EOL
}


chroot_fedora_enable_internet_time_synchronisation(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  systemctl enable systemd-timesyncd
EOL
}


chroot_fedora_ZFS_generate_host_id(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  zgenhostid -f -o /etc/hostid
EOL
}


chroot_fedora_install_locale_english(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  dnf install -y glibc-minimal-langpack glibc-langpack-en
EOL
}


# locale, keymap, timezone, hostname

chroot_fedora_set_locale_keymap_timezone_hostname(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  rm -f /etc/localtime
  rm -f /etc/hostname
  systemd-firstboot \
  --force \
  --locale=en_US.UTF-8 \
  --timezone=Etc/UTC \
  --hostname=testhost \
  --keymap=us || true
EOL
}


chroot_fedora_set_root_password(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  printf 'root:yourpassword' | chpasswd
EOL
}


chroot_fedora_apply_grub_workaround(){
  # This workaround needs to be applied for every GRUB update,
  # as the update will overwrite the changes.
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  echo 'export ZPOOL_VDEV_NAME_PATH=YES' >> /etc/profile.d/zpool_vdev_name_path.sh
  # shellcheck disable=SC1091
  . /etc/profile.d/zpool_vdev_name_path.sh

  # GRUB fails to detect rpool name, hard code as "rpool"
  sed -i "s|rpool=.*|rpool=rpool|"  /etc/grub.d/10_linux
EOL
}


chroot_fedora_grub_disable_module_boot_loader_specification(){
  # Fedora and RHEL uses Boot Loader Specification module for GRUB,
  # which does not support ZFS. Disable it
  # This means that you need to regenerate GRUB menu and mirror
  # them after every kernel update, otherwise computer will still
  # boot old kernel on reboot.
  # https://openzfs.github.io/openzfs-docs/Getting%20Started/Fedora/Root%20on%20ZFS.html
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  echo 'GRUB_ENABLE_BLSCFG=false' >> /etc/default/grub

EOL
}



chroot_fedora_install_grub(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  mkdir -p /boot/efi/fedora/grub-bootdir/i386-pc/
  for i in ${DISK}; do
   grub2-install --target=i386-pc --boot-directory \
       /boot/efi/fedora/grub-bootdir/i386-pc/  "${i}"
  done
  dnf reinstall -y grub2-efi-x64 shim-x64
  cp -r /usr/lib/grub/x86_64-efi/ /boot/efi/EFI/fedora/
EOL
}


chroot_fedora_generate_grub_menu(){
  chroot "${MNT}" /usr/bin/env ZPOOL_VDEV_NAME_PATH=1 DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  mkdir -p /boot/grub2
  grub2-mkconfig -o /boot/grub2/grub.cfg
  cp /boot/grub2/grub.cfg \
   /boot/efi/efi/fedora/grub.cfg
  cp /boot/grub2/grub.cfg \
   /boot/efi/fedora/grub-bootdir/i386-pc/grub2/grub.cfg
EOL
}


chroot_fedora_mirror_ESP_conent_legacy_and_EFI_booting(){
  chroot "${MNT}" /usr/bin/env DISK="${DISK}" bash << 'EOL'
  set -x
  unalias -a
  espdir=$(mktemp -d)
  find /boot/efi/ -maxdepth 1 -mindepth 1 -type d -print0 \
  | xargs -t -0I '{}' cp -r '{}' "${espdir}"
  find "${espdir}" -maxdepth 1 -mindepth 1 -type d -print0 \
  | xargs -t -0I '{}' sh -vxc "find /boot/efis/ -maxdepth 1 -mindepth 1 -type d -print0 | xargs -t -0I '[]' cp -r '{}' '[]'"
EOL
}


unmount_filesystems_and_create_initial_system_snapshot(){
  # Unmount filesystems and create initial system snapshot
  # You can later create a boot environment from this snapshot.
  # See Root on ZFS maintenance page.
  # https://openzfs.github.io/openzfs-docs/Getting%20Started/zfs_root_maintenance.html
  umount -Rl "${MNT}"
  zfs snapshot -r rpool@initial-installation
  zfs snapshot -r bpool@initial-installation
}



ZFS_list_snapshots(){
  zfs list -t snapshot
}

ZFS_export_all_pools(){
  zpool export -a
}

install_required_packages
enable_community_repo
setup_devd_udev
declare_disk_array
set_mount_point
set_swap_size
perform_disk_partition
load_ZFS_kernel_module
ZFS_destroy_bpool || true
ZFS_destroy_rpool || true
create_mirrored_boot_pool
create_mirrored_root_pool
zpool status
create_root_system_container
create_system_datasets_and_mount_them
format_and_mount_ESP
download_extract_minimal_Fedora_root_filesystem
generate_fstab
create_fedora_chroot
chroot_install_fedora_base_packages
chroot_install_fedora_ZFS_packages
chroot_fedora_add_ZFS_modules_to_dracut
chroot_fedora_add_mpt3sas_and_virtio_blk_drivers_to_dracut
chroot_fedora_build_initrd
chroot_fedora_SELinux_relabel_filesystem_on_reboot
chroot_fedora_enable_internet_time_synchronisation
chroot_fedora_ZFS_generate_host_id
chroot_fedora_install_locale_english
chroot_fedora_set_locale_keymap_timezone_hostname
chroot_fedora_set_root_password
chroot_fedora_apply_grub_workaround
chroot_fedora_grub_disable_module_boot_loader_specification
chroot_fedora_install_grub
chroot_fedora_generate_grub_menu #TODO fix /usr/sbin/grub2-probe: error: failed to get canonical path of /dev/<drive> (fine outside heredoc) ?? have added dnf install grub2-efi-*, and udevadm test /sys to populate /dev/disk/by-id
chroot_fedora_mirror_ESP_conent_legacy_and_EFI_booting
unmount_filesystems_and_create_initial_system_snapshot
ZFS_list_snapshots
ZFS_export_all_pools
# We're at the end, last step poweroff.
# This allows Perc controller to reset
# completely (search 'f/w initializing devices)
poweroff
# TODO poweron
