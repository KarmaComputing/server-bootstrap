#!/bin/bash

PORT=8000
PODMAN_IMAGE_NAME="ipxe_webserver"
BUILD_DIR="../serve"

echo "--- Building ${PODMAN_IMAGE_NAME} ---"
podman build --tag ${PODMAN_IMAGE_NAME} ${BUILD_DIR}

echo "--- Running ${PODMAN_IMAGE_NAME}, visit http://localhost:${PORT} ---"
podman run --rm \
    -p 0.0.0.0:${PORT}:80 \
    -v ${BUILD_DIR}/www:/usr/local/apache2/htdocs:z \
    localhost/${PODMAN_IMAGE_NAME}:latest
