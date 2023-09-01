#!/bin/bash

set -euxo pipefail

# Configuration parameters
SERVER_PUBLIC_IP=$1
SERVER_PORT=$2
SERVER_PUBLIC_KEY=$(wg pubkey < router-private.key)
DNS=$3

# Generate client keys
CLIENT_PRIVATE_KEY=$(wg genkey)
CLIENT_PUBLIC_KEY=$(wg pubkey <<< "${CLIENT_PRIVATE_KEY}")

# Assign the next available IP. This assumes you're using a /24 subnet.
# You'll have to adjust the logic if your setup is different.
LAST_IP=$(grep -oE '10\.10\.11\.[0-9]{1,3}' wg0.conf | tail -n1)
NEXT_IP_INT=$(echo "${LAST_IP}" | awk -F. '{print $4+1}')
CLIENT_IP="10.10.11.${NEXT_IP_INT}"

# Append the new client to the server configuration
cat <<EOF >> wg0.conf

[Peer]
PublicKey = ${CLIENT_PUBLIC_KEY}
AllowedIPs = ${CLIENT_IP}/32
EOF

# Generate the client configuration
cat <<EOF > "client_${CLIENT_IP}.conf"
[Interface]
PrivateKey = ${CLIENT_PRIVATE_KEY}
Address = ${CLIENT_IP}/32
DNS = ${DNS}

[Peer]
PublicKey = ${SERVER_PUBLIC_KEY}
Endpoint = ${SERVER_PUBLIC_IP}:${SERVER_PORT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
EOF

echo "Client configuration saved as client_${CLIENT_IP}.conf"

