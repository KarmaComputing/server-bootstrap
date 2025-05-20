#!/bin/bash
cd "$(dirname "$0")"

FILE="vm-test.ipxe"

WWW_DIR="../serve/www"
BUILD_DIR="../build/ipxe"
PODMAN_IMAGE_NAME="ipxe_builder"
ISO_MAKE_THREADS=16

echo "--- Creating serve directory at ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}

echo "--- Generating new SSH key pair ---"
ssh-keygen -t rsa -f ../build/key -N ""

echo "--- Copying public SSH key to ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}/ssh
mv -f ../build/key.pub ${WWW_DIR}/ssh/key.pub

echo "--- Setting correct permissions for private key ---"
chmod 600 ../build/key

echo "--- Copying private SSH key to ../../internal/runner/key ---"
mv -f ../build/key ../../internal/runner/key

echo "--- Building ${PODMAN_IMAGE_NAME} ---"
podman build \
    --tag ${PODMAN_IMAGE_NAME} \
    --no-cache \
    ${BUILD_DIR}

echo "--- Building ipxe.iso with ${FILE} embedded, writing to ${WWW_DIR} (using ${ISO_MAKE_THREADS} threads) ---"
podman run \
    --rm \
    -e FILE="$FILE" \
    --volume ${BUILD_DIR}/scripts:/input:z \
    --volume ${WWW_DIR}:/output:z \
    localhost/${PODMAN_IMAGE_NAME}:latest
