#!/bin/bash

set -euo pipefail

. ../venv/bin/activate

set -x

# Required environment settings
# - IDRAC_HOST
# - IDRAC_USERNAME
# - IDRAC_PASSWORD


# Check for required environment variables
REQUIRED_VARS=("IDRAC_HOST" "IDRAC_USERNAME" "IDRAC_PASSWORD" "HOST_HEALTHCHECK_POLL_IP")
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "Error: Required environment variable $var is not set."
    exit 1
  fi
done

cd web-ui

# Get server to a netbooted state (alpine)
python3 -c "from app import execute_redfish_command; execute_redfish_command('Bootstrap')"

# Run playbook to install fedora
ansible-playbook -i src/inventory.yaml src/playbooks/servers.yaml

