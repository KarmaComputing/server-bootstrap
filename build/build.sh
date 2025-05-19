#!/bin/bash
FILE="alpinebooter.ipxe"

# copy public SSH key into www
cp -f ssh-key/*.pub ../www

# build ipxe_buider image, grabbing the latest ipxe repo from GitHub
podman build \
    --tag localhost:ipxe_builder \
    --no-cache \
    ./ipxe

# build the ipxe.iso file, embedding the given file in input, and writing to ../www
podman run \
    -e FILE="$FILE" \
    --volume ./ipxe/input:/input:z \
    --volume ../www:/output:z \
    localhost:ipxe_builder
