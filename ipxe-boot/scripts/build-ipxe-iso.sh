#!/bin/bash

FILE="vm-test.ipxe"

WWW_DIR="../serve/www"
BUILD_DIR="../build/iso"
PODMAN_IMAGE_NAME="ipxe_builder"
ISO_MAKE_THREADS=16

echo "--- Creating serve directory at ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}

#echo "--- Copying public SSH key from ${BUILD_DIR}/ssh-key to ${WWW_DIR} ---"
#cp -f ${BUILD_DIR}/ssh-key/*.pub ${WWW_DIR}

echo "--- Building ${PODMAN_IMAGE_NAME} ---"
podman build \
    --tag ${PODMAN_IMAGE_NAME} \
    --no-cache \
    ${BUILD_DIR}

echo "--- Building ipxe.iso with ${FILE} embedded, writing to ${WWW_DIR} (using ${ISO_MAKE_THREADS} threads) ---"
podman run \
    --rm \
    -e FILE="$FILE" \
    --volume ${BUILD_DIR}/pxe:/input:z \
    --volume ${WWW_DIR}:/output:z \
    localhost/${PODMAN_IMAGE_NAME}:latest
