#!/bin/bash

RANDOM_STRING=$(echo -n $(date +%s%N) | sha256sum | head -c 20)
. venv/bin/activate
SECRET_KEY=$RANDOM_STRING flask run --debug
