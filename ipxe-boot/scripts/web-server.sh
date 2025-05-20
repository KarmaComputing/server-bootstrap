#!/bin/bash

PORT=8000
CONTAINER_TAG="ipxe_webserver"
BUILD_DIR="../serve"

echo "--- Building ${CONTAINER_TAG} ---"
podman build --tag ${CONTAINER_TAG} ${BUILD_DIR}

echo "--- Running ${CONTAINER_TAG}, visit http://localhost:${PORT} ---"
podman run --rm \
    -p ${PORT}:80 \
    -v ${BUILD_DIR}/www:/usr/local/apache2/htdocs:z \
    localhost/${CONTAINER_TAG}:latest
