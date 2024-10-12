#!/bin/bash

set -exu

#
# Publish vpn credentials to password manager
# Example used is psono
#

# Required environment vars which must be set:
# - PSONO_CI_API_KEY_ID
# - PSONO_CI_API_SECRET_KEY_HEX
# - PSONO_CI_SERVER_URL

# Arguments
# 1. PSONO_SECRET_ID
# 2. PSONO_SECRET_NEW_VALUE
#
# Example invocation:
#
# ./save-vpn-credentials-to-password-vault.sh 42g4462j-586h-gk38-9450-321753638f3b "[Interface]
# PrivateKey = kNE8pYNCOokWSWoWO/6HcYoTglxNqYyllIFsvi6hIV8=
# Address = 10.10.11.3/32
# DNS = 8.8.8.8
# 
# [Peer]
# PublicKey = 6gx1p4CjmaNf4XphHFpwG8C7OdTlzaz/zdpb32ZDT2g=
# Endpoint = 192.0.2.1:3478
# AllowedIPs = 0.0.0.0/0
# PersistentKeepalive = 25"

PSONO_SECRET_ID=$1
PSONO_SECRET_NEW_VALUE=$2

psonoci secret set "$PSONO_SECRET_ID" notes "$PSONO_SECRET_NEW_VALUE"
