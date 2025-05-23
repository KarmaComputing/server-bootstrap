#!/bin/sh

# make sure we never run 2 rsync at the same time
lockfile="/tmp/alpine-mirror.lock"
if [ -z "$flock" ] ; then
  exec env flock=1 flock -n $lockfile "$0" "$@"
fi

src=rsync://rsync.alpinelinux.org/alpine/ 
dest=/site

exclude="--exclude v2.* --exclude v3.0 --exclude v3.1 --exclude v3.2 --exclude v3.3 --exclude v3.4 --exclude v3.5 --exclude v3.6 --exclude v3.7 --exclude v3.8 --exclude v3.9 --exclude v3.10 --exclude v3.11 --exclude v3.12 --exclude v3.13 --exclude v3.14 --exclude v3.15 --exclude v3.16 --exclude v3.17"

echo "--- Starting Sync ---"

mkdir -p "$dest"
/usr/bin/rsync \
        --archive \
        --update \
        --hard-links \
        --delete \
        --delete-after \
        --delay-updates \
        --timeout=600 \
        $exclude \
        "$src" "$dest"
        
echo "--- Finished Sync ---"