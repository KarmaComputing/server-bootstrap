#!/bin/bash

PODMAN_IMAGE_NAME="alpine_builder"
WWW_DIR="../serve/www/iso/alpine-netboot"
BUILD_DIR="../build/alpine"

echo "--- Creating directory at ${WWW_DIR} ---"
mkdir -p ${WWW_DIR}

echo "--- Building ${PODMAN_IMAGE_NAME} ---"
podman build --no-cache --tag ${PODMAN_IMAGE_NAME} ${BUILD_DIR}

echo "--- Running ${PODMAN_IMAGE_NAME} ---"
podman run --rm -v ${WWW_DIR}:/output:z \
    localhost/${PODMAN_IMAGE_NAME}:latest
