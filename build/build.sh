#!/bin/bash
    

# build ipxe.iso in ../www
podman build \
    --tag localhost:ipxe_builder \
    --no-cache \
    ./ipxe

podman run \
    -e FILE=alpinebooter.ipxe \
    --volume ./ipxe/input:/input:z \
    --volume ../www:/output:z \
    localhost:ipxe_builder