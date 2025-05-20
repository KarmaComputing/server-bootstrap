#!/bin/bash

FILE="alpinebooter.ipxe"

WWW_DIR="../serve/www"
BUILD_DIR="../build"
CONTAINER_TAG="ipxe_builder"
ISO_MAKE_THREADS=16

echo "--- Creating serve directory at ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}

echo "--- Copying public SSH key from ${BUILD_DIR}/ssh-key to ${WWW_DIR} ---"
cp -f ${BUILD_DIR}/ssh-key/*.pub ${WWW_DIR}

echo "--- Building ${CONTAINER_TAG} ---"
podman build \
    --tag ${CONTAINER_TAG} \
    --no-cache \
    ${BUILD_DIR}/iso

echo "--- Building ipxe.iso with ${FILE} embedded, writing to ${WWW_DIR} (using ${ISO_MAKE_THREADS} threads) ---"
podman run \
    --rm \
    -e FILE="$FILE" \
    --volume ${BUILD_DIR}/iso/pxe:/input:z \
    --volume ${WWW_DIR}:/output:z \
    localhost/${CONTAINER_TAG}:latest
