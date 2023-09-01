#!/bin/bash

set -euxo pipefail

# Generate new client vpn configs and
# write them to file
# does not distribute them.

# Configuration parameters
# Check if $1 is set and not empty
if [[ $# -ge 1 ]]; then
    SERVER_PUBLIC_IP=$1
else
    SERVER_PUBLIC_IP=$(ip route get 8.8.8.8 | head -n 1  | awk '{print $7}')
fi

echo "$SERVER_PUBLIC_IP"

# Check if $2 is set and not empty
if [[ $# -ge 2 ]]; then
    SERVER_PORT=$2
else
    SERVER_PORT=3478
    echo Using default port
fi

# Check if $3 is set and not empty
if [[ $# -ge 3 ]]; then
    DNS=$3
else
    DNS="8.8.8.8"
    echo Using default DNS
fi

SERVER_PUBLIC_KEY=$(wg pubkey < router-private.key)
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

echo reloading wireguard without killing active connections
wg syncconf wg0 <(wg-quick strip wg0)

