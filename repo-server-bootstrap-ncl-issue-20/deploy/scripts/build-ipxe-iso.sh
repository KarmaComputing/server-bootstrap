#!/bin/bash
cd "$(dirname "$0")"

set -exu

FILE="alpinebooter.ipxe"

WWW_DIR="../serve/www"
BUILD_DIR="../build/ipxe"
PODMAN_IMAGE_NAME="ipxe_builder"
SSH_KEY_DIR="../ssh"
ISO_MAKE_THREADS=16

echo "--- Creating serve directory at ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}

echo "--- Creating ssh key directory at ${SSH_KEY_DIR} ---"
mkdir -p ${SSH_KEY_DIR}

echo "--- Generating new SSH key pair in ${SSH_KEY_DIR} ---"
ssh-keygen -t rsa -f ${SSH_KEY_DIR}/key -N ""

echo "--- Copying public SSH key to ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}/ssh
mv -f ${SSH_KEY_DIR}/key.pub ${WWW_DIR}/ssh/key.pub

echo "--- Setting correct permissions for private key ---"
chmod 600 ${SSH_KEY_DIR}/key

echo "--- Building ${PODMAN_IMAGE_NAME} ---"
podman build \
    --tag ${PODMAN_IMAGE_NAME} \
    ${BUILD_DIR}

if [ $? -neq 0 ]; then
  echo "!!! BUILD FAILED, EXITING !!!"
  exit
fi

echo "--- Building ipxe.iso with ${FILE} embedded, writing to ${WWW_DIR} (using ${ISO_MAKE_THREADS} threads) ---"
podman run \
    --rm \
    -e FILE="$FILE" \
    --volume ${BUILD_DIR}/scripts:/input:z \
    --volume ${WWW_DIR}:/output:z \
    localhost/${PODMAN_IMAGE_NAME}:latest
